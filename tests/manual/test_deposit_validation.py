from decimal import Decimal

import pytest

from transactions.constants import DEPOSIT
from transactions.forms import DepositForm


@pytest.mark.django_db
def test_deposit_below_minimum_is_rejected(bank_account):
    """
    DEP-BVA-01 / FR-D01

    A deposit one cent below the configured minimum must be rejected.
    """
    form = DepositForm(
        data={
            "amount": Decimal("9.99"),
        },
        initial={
            "transaction_type": DEPOSIT
        },
        account=bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors


@pytest.mark.django_db
def test_deposit_equal_to_minimum_is_accepted(bank_account):
    """
    DEP-BVA-02 / FR-D04

    A deposit exactly equal to the configured minimum must be accepted.
    """
    form = DepositForm(
        data={
            "amount": Decimal("10.00"),
        },
        initial={
            "transaction_type": DEPOSIT
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_deposit_above_minimum_is_accepted(bank_account):
    """
    DEP-BVA-03 / FR-D01

    A deposit one cent above the configured minimum must be accepted.
    """
    form = DepositForm(
        data={
            "amount": Decimal("10.01"),
        },
        initial={
            "transaction_type": DEPOSIT
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors