from decimal import Decimal

import pytest

from accounts.models import BankAccountType


@pytest.mark.django_db
def test_zero_principal_produces_zero_interest():
    """
    INT-BVA-01

    A zero principal must produce zero interest.
    """
    account_type = BankAccountType(
        name="Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )

    result = account_type.calculate_interest(Decimal("0.00"))

    assert result == Decimal("0.00")


@pytest.mark.django_db
def test_zero_interest_rate_produces_zero_interest():
    """
    INT-BVA-02 / FR-I01

    A zero annual interest rate must produce zero interest.
    """
    account_type = BankAccountType(
        name="Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("0.00"),
        interest_calculation_per_year=12,
    )

    result = account_type.calculate_interest(Decimal("1000.00"))

    assert result == Decimal("0.00")


@pytest.mark.django_db
def test_positive_principal_and_rate_produce_positive_interest():
    """
    INT-EP-03 / FR-I02

    A positive principal and positive rate must produce positive interest.
    """
    account_type = BankAccountType(
        name="Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )

    result = account_type.calculate_interest(Decimal("1000.00"))

    assert result > Decimal("0.00")


@pytest.mark.django_db
def test_interest_increases_with_principal():
    """
    INT-EP-04 / FR-I03

    Under the same rate and frequency, a larger principal must not
    produce less interest.
    """
    account_type = BankAccountType(
        name="Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )

    smaller_interest = account_type.calculate_interest(
        Decimal("1000.00")
    )
    larger_interest = account_type.calculate_interest(
        Decimal("2000.00")
    )

    assert larger_interest >= smaller_interest


@pytest.mark.django_db
def test_interest_increases_with_rate():
    """
    INT-EP-05 / FR-I04

    Under the same principal and frequency, a larger interest rate must
    not produce less interest.
    """
    lower_rate_type = BankAccountType(
        name="Lower Rate",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )

    higher_rate_type = BankAccountType(
        name="Higher Rate",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("10.00"),
        interest_calculation_per_year=12,
    )

    lower_interest = lower_rate_type.calculate_interest(
        Decimal("1000.00")
    )
    higher_interest = higher_rate_type.calculate_interest(
        Decimal("1000.00")
    )

    assert higher_interest >= lower_interest


@pytest.mark.django_db
def test_interest_result_is_rounded_to_two_decimal_places():
    """
    FR-I05 / INV-13

    Calculated interest must be rounded to two decimal places.
    """
    account_type = BankAccountType(
        name="Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )

    result = account_type.calculate_interest(Decimal("1234.56"))

    assert result == round(result, 2)