# Financial Requirements Specification

The following requirements are derived from the selected upstream source
code and are used as the behavioural specification for the experiment.

## Deposit Requirements

### FR-D01 — Minimum Deposit

A deposit amount must be greater than or equal to the configured minimum
deposit amount.

### FR-D02 — Deposit Balance Update

For every accepted deposit:

`new_balance = previous_balance + deposit_amount`

### FR-D03 — Deposit Monotonicity

For every accepted positive deposit:

`new_balance > previous_balance`

### FR-D04 — Deposit Boundary Acceptance

A deposit exactly equal to the configured minimum amount must be accepted.

### FR-D05 — Invalid Deposit Preservation

A rejected deposit must not alter the account balance or create a
transaction record.

## Withdrawal Requirements

### FR-W01 — Minimum Withdrawal

A withdrawal amount must be greater than or equal to the configured
minimum withdrawal amount.

### FR-W02 — Maximum Withdrawal

A withdrawal amount must not exceed the maximum amount configured for the
account type.

### FR-W03 — Available-Balance Precondition

A withdrawal amount must not exceed the current account balance.

### FR-W04 — Withdrawal Balance Update

For every accepted withdrawal:

`new_balance = previous_balance - withdrawal_amount`

### FR-W05 — Minimum Boundary Acceptance

A withdrawal exactly equal to the configured minimum amount must be
accepted when all other conditions are satisfied.

### FR-W06 — Maximum Boundary Acceptance

A withdrawal exactly equal to the account-type maximum must be accepted
when sufficient balance is available.

### FR-W07 — Exact-Balance Withdrawal

A withdrawal exactly equal to the available account balance must be
accepted when all other conditions are satisfied.

### FR-W08 — Invalid Withdrawal Preservation

A rejected withdrawal must leave the account balance unchanged and must
not create a transaction record.

## Transaction Requirements

### FR-T01 — Account Association

Every transaction record must be associated with the account on which the
transaction was performed.

### FR-T02 — Transaction Type

Every transaction must use a valid transaction type.

### FR-T03 — Resulting-Balance Record

The transaction field `balance_after_transaction` must equal the account
balance resulting from the completed transaction.

### FR-T04 — Transaction Amount Precision

Transaction amounts are represented with two decimal places.

## Interest Requirements

### FR-I01 — Zero Interest Rate

A zero annual interest rate must produce zero calculated interest.

### FR-I02 — Nonnegative Interest

For a nonnegative principal and a nonnegative annual interest rate,
calculated interest must not be negative.

### FR-I03 — Principal Monotonicity

Under the same positive interest rate and calculation frequency, increasing
the principal must not decrease the calculated interest.

### FR-I04 — Rate Monotonicity

For the same positive principal and calculation frequency, increasing the
annual interest rate must not decrease the calculated interest.

### FR-I05 — Two-Decimal Result

Calculated interest must be rounded to two decimal places.
