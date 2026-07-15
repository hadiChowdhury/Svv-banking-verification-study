from datetime import date
from decimal import Decimal

import pytest

from accounts.models import (
    BankAccountType,
    User,
    UserBankAccount,
)


@pytest.fixture
def property_account_type(db):
    return BankAccountType.objects.create(
        name="Property Savings",
        maximum_withdrawal_amount=Decimal("1000.00"),
        annual_interest_rate=Decimal("5.00"),
        interest_calculation_per_year=12,
    )


@pytest.fixture
def property_user(db):
    return User.objects.create_user(
        email="property.test@example.com",
        password="StrongPassword123!",
    )


@pytest.fixture
def property_bank_account(
    db,
    property_user,
    property_account_type,
):
    return UserBankAccount.objects.create(
        user=property_user,
        account_type=property_account_type,
        account_no=20000001,
        gender="M",
        birth_date=date(1995, 1, 1),
        balance=Decimal("500.00"),
    )