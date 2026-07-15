from datetime import date
from decimal import Decimal

import pytest

from accounts.models import BankAccountType, User
from transactions.constants import DEPOSIT
from transactions.models import Transaction


@pytest.mark.django_db
def test_user_balance_returns_account_balance(user, bank_account):
    """
    Verify that User.balance exposes the associated account balance.
    """
    assert user.balance == Decimal("500.00")


@pytest.mark.django_db
def test_user_without_account_has_zero_balance():
    """
    Verify the fallback balance for a user without a bank account.
    """
    user = User(
        email="no.account@example.com",
    )

    assert user.balance == 0


@pytest.mark.django_db
def test_bank_account_type_string_representation(account_type):
    assert str(account_type) == "Savings"


@pytest.mark.django_db
def test_bank_account_string_representation(bank_account):
    assert str(bank_account) == "10000001"


@pytest.mark.django_db
def test_transaction_string_representation(bank_account):
    transaction = Transaction.objects.create(
        account=bank_account,
        amount=Decimal("50.00"),
        balance_after_transaction=Decimal("550.00"),
        transaction_type=DEPOSIT,
    )

    assert str(transaction) == "10000001"


@pytest.mark.django_db
def test_interest_calculation_months(bank_account):
    """
    Verify the generated interest schedule for monthly calculation.
    """
    bank_account.interest_start_date = date(2026, 2, 1)

    assert bank_account.get_interest_calculation_months() == [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
    ]