from decimal import Decimal

import pytest
from django.urls import reverse

from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.models import Transaction


@pytest.mark.django_db
def test_valid_deposit_updates_balance_and_records_transaction(
    client,
    user,
    bank_account,
):
    """
    FR-D02, FR-D03, FR-T01, FR-T02, FR-T03
    INV-01, INV-08
    """
    client.force_login(user)

    initial_balance = bank_account.balance
    amount = Decimal("100.00")

    response = client.post(
        reverse("transactions:deposit_money"),
        data={
            "amount": str(amount),
            "transaction_type": DEPOSIT,
        },
    )

    assert response.status_code == 302

    bank_account.refresh_from_db()

    assert bank_account.balance == initial_balance + amount

    transaction = Transaction.objects.get(
        account=bank_account,
        transaction_type=DEPOSIT,
    )

    assert transaction.amount == amount
    assert transaction.balance_after_transaction == bank_account.balance


@pytest.mark.django_db
def test_valid_withdrawal_updates_balance_and_records_transaction(
    client,
    user,
    bank_account,
):
    """
    FR-W04, FR-T01, FR-T02, FR-T03
    INV-03, INV-08
    """
    client.force_login(user)

    initial_balance = bank_account.balance
    amount = Decimal("100.00")

    response = client.post(
        reverse("transactions:withdraw_money"),
        data={
            "amount": str(amount),
            "transaction_type": WITHDRAWAL,
        },
    )

    assert response.status_code == 302

    bank_account.refresh_from_db()

    assert bank_account.balance == initial_balance - amount

    transaction = Transaction.objects.get(
        account=bank_account,
        transaction_type=WITHDRAWAL,
    )

    assert transaction.amount == amount
    assert transaction.balance_after_transaction == bank_account.balance


@pytest.mark.django_db
def test_rejected_deposit_preserves_balance_and_creates_no_transaction(
    client,
    user,
    bank_account,
):
    """
    FR-D05
    INV-02, INV-07
    """
    client.force_login(user)

    initial_balance = bank_account.balance

    response = client.post(
        reverse("transactions:deposit_money"),
        data={
            "amount": "9.99",
            "transaction_type": DEPOSIT,
        },
    )

    assert response.status_code == 200

    bank_account.refresh_from_db()

    assert bank_account.balance == initial_balance
    assert Transaction.objects.filter(account=bank_account).count() == 0


@pytest.mark.django_db
def test_rejected_withdrawal_preserves_balance_and_creates_no_transaction(
    client,
    user,
    bank_account,
):
    """
    FR-W08
    INV-06, INV-07
    """
    client.force_login(user)

    initial_balance = bank_account.balance

    response = client.post(
        reverse("transactions:withdraw_money"),
        data={
            "amount": "500.01",
            "transaction_type": WITHDRAWAL,
        },
    )

    assert response.status_code == 200

    bank_account.refresh_from_db()

    assert bank_account.balance == initial_balance
    assert Transaction.objects.filter(account=bank_account).count() == 0

@pytest.mark.django_db
def test_subsequent_deposit_preserves_existing_interest_dates(
    client,
    user,
    bank_account,
):
    """
    Exercise the deposit path for an account that already has
    initialized interest dates.
    """
    from datetime import date

    client.force_login(user)

    original_initial_date = date(2026, 1, 1)
    original_interest_start = date(2026, 2, 1)

    bank_account.initial_deposit_date = original_initial_date
    bank_account.interest_start_date = original_interest_start
    bank_account.save(
        update_fields=[
            "initial_deposit_date",
            "interest_start_date",
        ]
    )

    response = client.post(
        reverse("transactions:deposit_money"),
        data={
            "amount": "100.00",
            "transaction_type": DEPOSIT,
        },
    )

    assert response.status_code == 302

    bank_account.refresh_from_db()

    assert bank_account.initial_deposit_date == original_initial_date
    assert bank_account.interest_start_date == original_interest_start