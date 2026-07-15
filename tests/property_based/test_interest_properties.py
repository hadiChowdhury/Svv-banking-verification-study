from decimal import Decimal

from hypothesis import given

from accounts.models import BankAccountType

from .strategies import (
    interest_frequencies,
    money,
    positive_interest_rates,
    valid_interest_rates,
)


def make_account_type(
    rate: Decimal,
    frequency: int,
) -> BankAccountType:
    return BankAccountType(
        name="Generated Account Type",
        maximum_withdrawal_amount=Decimal("1000000.00"),
        annual_interest_rate=rate,
        interest_calculation_per_year=frequency,
    )


@given(
    principal=money,
    frequency=interest_frequencies,
)
def test_zero_rate_always_produces_zero_interest(
    principal,
    frequency,
):
    """
    PROP-10 / INV-09

    For every generated nonnegative principal, a zero rate must
    produce zero interest.
    """
    account_type = make_account_type(
        rate=Decimal("0.00"),
        frequency=frequency,
    )

    result = account_type.calculate_interest(principal)

    assert result == Decimal("0.00")


@given(
    principal=money,
    rate=valid_interest_rates,
    frequency=interest_frequencies,
)
def test_interest_is_never_negative(
    principal,
    rate,
    frequency,
):
    """
    PROP-11 / INV-10

    Nonnegative principal and rate must never produce
    negative interest.
    """
    account_type = make_account_type(
        rate=rate,
        frequency=frequency,
    )

    result = account_type.calculate_interest(principal)

    assert result >= Decimal("0.00")


@given(
    smaller_principal=money,
    additional_principal=money,
    rate=positive_interest_rates,
    frequency=interest_frequencies,
)
def test_interest_is_monotonic_with_principal(
    smaller_principal,
    additional_principal,
    rate,
    frequency,
):
    """
    PROP-12 / INV-11

    Increasing the principal must not decrease calculated interest.
    """
    larger_principal = (
        smaller_principal + additional_principal
    )

    account_type = make_account_type(
        rate=rate,
        frequency=frequency,
    )

    smaller_interest = account_type.calculate_interest(
        smaller_principal
    )
    larger_interest = account_type.calculate_interest(
        larger_principal
    )

    assert larger_interest >= smaller_interest


@given(
    principal=money,
    lower_rate=valid_interest_rates,
    additional_rate=valid_interest_rates,
    frequency=interest_frequencies,
)
def test_interest_is_monotonic_with_rate(
    principal,
    lower_rate,
    additional_rate,
    frequency,
):
    """
    PROP-13 / INV-12

    Increasing the interest rate must not decrease calculated interest.
    """
    higher_rate = min(
        lower_rate + additional_rate,
        Decimal("100.00"),
    )

    lower_rate_type = make_account_type(
        rate=lower_rate,
        frequency=frequency,
    )

    higher_rate_type = make_account_type(
        rate=higher_rate,
        frequency=frequency,
    )

    lower_interest = lower_rate_type.calculate_interest(
        principal
    )
    higher_interest = higher_rate_type.calculate_interest(
        principal
    )

    assert higher_interest >= lower_interest


@given(
    principal=money,
    rate=valid_interest_rates,
    frequency=interest_frequencies,
)
def test_interest_result_has_at_most_two_decimal_places(
    principal,
    rate,
    frequency,
):
    """
    PROP-14 / INV-13

    Every generated valid interest result must be rounded
    to at most two decimal places.
    """
    account_type = make_account_type(
        rate=rate,
        frequency=frequency,
    )

    result = account_type.calculate_interest(principal)

    assert result == round(result, 2)