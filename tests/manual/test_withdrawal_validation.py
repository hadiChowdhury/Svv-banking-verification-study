from decimal import Decimal

import pytest

from transactions.constants import WITHDRAWAL
from transactions.forms import WithdrawForm


@pytest.mark.django_db
def test_withdrawal_below_minimum_is_rejected(bank_account):
    """
    WIT-MIN-BVA-01 / FR-W01

    A withdrawal one cent below the minimum must be rejected.
    """
    form = WithdrawForm(
        data={
            "amount": Decimal("9.99"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors


@pytest.mark.django_db
def test_withdrawal_equal_to_minimum_is_accepted(bank_account):
    """
    WIT-MIN-BVA-02 / FR-W05

    A withdrawal exactly equal to the minimum must be accepted.
    """
    form = WithdrawForm(
        data={
            "amount": Decimal("10.00"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_withdrawal_above_minimum_is_accepted(bank_account):
    """
    WIT-MIN-BVA-03

    A withdrawal one cent above the minimum must be accepted.
    """
    form = WithdrawForm(
        data={
            "amount": Decimal("10.01"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_withdrawal_below_maximum_is_accepted(bank_account):
    """
    WIT-MAX-BVA-01

    A withdrawal one cent below the account-type maximum must be accepted
    when sufficient balance is available.
    """
    bank_account.balance = Decimal("1500.00")
    bank_account.save(update_fields=["balance"])

    form = WithdrawForm(
        data={
            "amount": Decimal("999.99"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_withdrawal_equal_to_maximum_is_accepted(bank_account):
    """
    WIT-MAX-BVA-02 / FR-W06

    A withdrawal exactly equal to the account-type maximum must be accepted
    when sufficient balance is available.
    """
    bank_account.balance = Decimal("1500.00")
    bank_account.save(update_fields=["balance"])

    form = WithdrawForm(
        data={
            "amount": Decimal("1000.00"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_withdrawal_above_maximum_is_rejected(bank_account):
    """
    WIT-MAX-BVA-03 / FR-W02

    A withdrawal one cent above the account-type maximum must be rejected.
    """
    bank_account.balance = Decimal("1500.00")
    bank_account.save(update_fields=["balance"])

    form = WithdrawForm(
        data={
            "amount": Decimal("1000.01"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors


@pytest.mark.django_db
def test_withdrawal_below_balance_is_accepted(bank_account):
    """
    WIT-BAL-BVA-01

    A withdrawal one cent below the current balance must be accepted.
    """
    form = WithdrawForm(
        data={
            "amount": Decimal("499.99"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_withdrawal_equal_to_balance_is_accepted(bank_account):
    """
    WIT-BAL-BVA-02 / FR-W07

    A withdrawal exactly equal to the available balance must be accepted.
    """
    form = WithdrawForm(
        data={
            "amount": Decimal("500.00"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_withdrawal_above_balance_is_rejected(bank_account):
    """
    WIT-BAL-BVA-03 / FR-W03

    A withdrawal one cent above the available balance must be rejected.
    """
    form = WithdrawForm(
        data={
            "amount": Decimal("500.01"),
        },
        initial={
            "transaction_type": WITHDRAWAL
        },
        account=bank_account,
    )

    assert not form.is_valid()
    assert "amount" in form.errors