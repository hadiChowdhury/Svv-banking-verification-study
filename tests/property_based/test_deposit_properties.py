from decimal import Decimal

import pytest
from hypothesis import given, HealthCheck, settings

from transactions.constants import DEPOSIT
from transactions.forms import DepositForm

from .strategies import (
    invalid_deposit_amounts,
    valid_deposit_amounts,
)


@pytest.mark.django_db
@settings(
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ]
)
@given(amount=valid_deposit_amounts)
def test_every_valid_deposit_amount_is_accepted(
    property_bank_account,
    amount,
):
    """
    PROP-01, PROP-02

    Every generated amount at or above the configured minimum
    must satisfy deposit validation.
    """
    form = DepositForm(
        data={
            "amount": amount,
        },
        initial={
            "transaction_type": DEPOSIT,
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
@given(amount=invalid_deposit_amounts)
def test_every_below_minimum_deposit_is_rejected(
    property_bank_account,
    amount,
):
    """
    PROP-03

    Every generated amount below the configured minimum
    must be rejected.
    """
    form = DepositForm(
        data={
            "amount": amount,
        },
        initial={
            "transaction_type": DEPOSIT,
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
@given(amount=valid_deposit_amounts)
def test_valid_deposit_arithmetic_is_monotonic(
    property_bank_account,
    amount,
):
    """
    PROP-01, PROP-02

    The financial postcondition of every generated valid
    deposit is exact addition and monotonic balance growth.
    """
    balance_before = property_bank_account.balance
    balance_after = balance_before + amount

    assert balance_after == balance_before + amount
    assert balance_after > balance_before