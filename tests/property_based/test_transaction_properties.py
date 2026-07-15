from decimal import Decimal

import pytest
from django.urls import reverse
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.models import Transaction


generated_deposits = st.decimals(
    min_value=Decimal("10.00"),
    max_value=Decimal("10000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


generated_withdrawals = st.decimals(
    min_value=Decimal("10.00"),
    max_value=Decimal("500.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


@pytest.mark.django_db
@settings(
    max_examples=50,
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ],
)
@given(amount=generated_deposits)
def test_generated_deposit_updates_real_account_and_transaction(
    client,
    property_user,
    property_bank_account,
    amount,
):
    """
    PROP-01, PROP-02, PROP-09

    Every generated valid deposit must update the real account
    balance by exactly the deposited amount and record the same
    resulting balance in the transaction.
    """
    initial_balance = Decimal("500.00")

    Transaction.objects.filter(
        account=property_bank_account,
    ).delete()

    property_bank_account.balance = initial_balance
    property_bank_account.save(update_fields=["balance"])

    client.force_login(property_user)

    response = client.post(
        reverse("transactions:deposit_money"),
        data={
            "amount": str(amount),
            "transaction_type": DEPOSIT,
        },
    )

    assert response.status_code == 302

    property_bank_account.refresh_from_db()

    expected_balance = initial_balance + amount

    assert property_bank_account.balance == expected_balance
    assert property_bank_account.balance > initial_balance

    transaction = Transaction.objects.get(
        account=property_bank_account,
        transaction_type=DEPOSIT,
    )

    assert transaction.amount == amount
    assert (
        transaction.balance_after_transaction
        == property_bank_account.balance
    )


@pytest.mark.django_db
@settings(
    max_examples=50,
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
    ],
)
@given(amount=generated_withdrawals)
def test_generated_withdrawal_updates_real_account_and_transaction(
    client,
    property_user,
    property_bank_account,
    amount,
):
    """
    PROP-04, PROP-09

    Every generated valid withdrawal must decrease the real account
    balance by exactly the requested amount and record the resulting
    balance consistently.
    """
    initial_balance = Decimal("500.00")

    Transaction.objects.filter(
        account=property_bank_account,
    ).delete()

    property_bank_account.balance = initial_balance
    property_bank_account.save(update_fields=["balance"])

    client.force_login(property_user)

    response = client.post(
        reverse("transactions:withdraw_money"),
        data={
            "amount": str(amount),
            "transaction_type": WITHDRAWAL,
        },
    )

    assert response.status_code == 302

    property_bank_account.refresh_from_db()

    expected_balance = initial_balance - amount

    assert property_bank_account.balance == expected_balance
    assert property_bank_account.balance >= Decimal("0.00")

    transaction = Transaction.objects.get(
        account=property_bank_account,
        transaction_type=WITHDRAWAL,
    )

    assert transaction.amount == amount
    assert (
        transaction.balance_after_transaction
        == property_bank_account.balance
    )