from datetime import date
from decimal import Decimal

import pytest

from accounts.models import (
    BankAccountType,
    User,
    UserBankAccount,
)


@pytest.fixture
def account_type(db):
    """
    Create a reusable bank account type for manual tests.

    The maximum withdrawal amount is fixed at 1,000.00 so that
    minimum, maximum, and available-balance boundaries can be
    tested independently.
    """
    return BankAccountType.objects.create(
        name="Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )


@pytest.fixture
def user(db):
    """Create a user for the test bank account."""
    return User.objects.create_user(
        email="manual.test@example.com",
        password="StrongPassword123!",
    )


@pytest.fixture
def bank_account(db, user, account_type):
    """
    Create a bank account with a predictable starting balance.
    """
    return UserBankAccount.objects.create(
        user=user,
        account_type=account_type,
        account_no=10000001,
        gender="M",
        birth_date=date(1995, 1, 1),
        balance=Decimal("500.00"),
    )