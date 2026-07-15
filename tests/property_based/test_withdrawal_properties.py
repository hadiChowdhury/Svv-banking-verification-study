from decimal import Decimal

import pytest
from hypothesis import given, HealthCheck, settings
from hypothesis import strategies as st

from transactions.constants import WITHDRAWAL
from transactions.forms import WithdrawForm


valid_withdrawal_amounts = st.decimals(
    min_value=Decimal("10.00"),
    max_value=Decimal("500.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


below_minimum_withdrawals = st.decimals(
    min_value=Decimal("0.00"),
    max_value=Decimal("9.99"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


above_balance_withdrawals = st.decimals(
    min_value=Decimal("500.01"),
    max_value=Decimal("1000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


above_maximum_withdrawals = st.decimals(
    min_value=Decimal("1000.01"),
    max_value=Decimal("1000000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(amount=valid_withdrawal_amounts)
def test_every_valid_withdrawal_is_accepted(
    property_bank_account,
    amount,
):
    """
    PROP-04

    Every generated withdrawal satisfying the minimum,
    maximum, and available-balance constraints is accepted.
    """
    form = WithdrawForm(
        data={
            "amount": amount,
        },
        initial={
            "transaction_type": WITHDRAWAL,
        },
        account=property_bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(amount=below_minimum_withdrawals)
def test_every_below_minimum_withdrawal_is_rejected(
    property_bank_account,
    amount,
):
    """
    PROP-05
    """
    form = WithdrawForm(
        data={
            "amount": amount,
        },
        initial={
            "transaction_type": WITHDRAWAL,
        },
        account=property_bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(amount=above_balance_withdrawals)
def test_every_above_balance_withdrawal_is_rejected(
    property_bank_account,
    amount,
):
    """
    PROP-07

    Generated values exceed the current 500.00 balance
    while remaining at or below the account maximum.
    """
    form = WithdrawForm(
        data={
            "amount": amount,
        },
        initial={
            "transaction_type": WITHDRAWAL,
        },
        account=property_bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(amount=above_maximum_withdrawals)
def test_every_above_maximum_withdrawal_is_rejected(
    property_bank_account,
    amount,
):
    """
    PROP-06
    """
    property_bank_account.balance = Decimal("2000000.00")

    form = WithdrawForm(
        data={
            "amount": amount,
        },
        initial={
            "transaction_type": WITHDRAWAL,
        },
        account=property_bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(amount=valid_withdrawal_amounts)
def test_valid_withdrawal_arithmetic_is_exact(
    property_bank_account,
    amount,
):
    """
    PROP-04

    Every generated valid withdrawal satisfies the exact
    financial postcondition.
    """
    balance_before = property_bank_account.balance
    balance_after = balance_before - amount

    assert balance_after == balance_before - amount
    assert balance_after >= Decimal("0.00")


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(
    balance=st.decimals(
        min_value=Decimal("10.00"),
        max_value=Decimal("1000.00"),
        places=2,
        allow_nan=False,
        allow_infinity=False,
    )
)
def test_exact_balance_withdrawal_is_accepted(
    property_bank_account,
    balance,
):
    """
    PROP-08

    Withdrawing the exact available balance must be accepted
    when all configured limits are satisfied.
    """
    property_bank_account.balance = balance

    form = WithdrawForm(
        data={
            "amount": balance,
        },
        initial={
            "transaction_type": WITHDRAWAL,
        },
        account=property_bank_account,
    )

    assert form.is_valid(), form.errors

    resulting_balance = balance - balance

    assert resulting_balance == Decimal("0.00")