# Financial Invariant Catalogue

## INV-01 — Deposit Balance Correctness

For every valid deposit:

`balance_after = balance_before + amount`

Related requirements:

- FR-D02
- FR-D03

## INV-02 — Deposit Minimum Enforcement

Deposits below the configured minimum are rejected.

Related requirements:

- FR-D01
- FR-D04

## INV-03 — Withdrawal Balance Correctness

For every valid withdrawal:

`balance_after = balance_before - amount`

Related requirements:

- FR-W04

## INV-04 — Withdrawal Minimum Enforcement

Withdrawals below the configured minimum are rejected.

Related requirements:

- FR-W01
- FR-W05

## INV-05 — Withdrawal Maximum Enforcement

Withdrawals above the account-type maximum are rejected.

Related requirements:

- FR-W02
- FR-W06

## INV-06 — Withdrawal Available-Balance Enforcement

Withdrawals above the current balance are rejected.

Related requirements:

- FR-W03
- FR-W07

## INV-07 — Failed-Operation State Preservation

For every rejected deposit or withdrawal:

`balance_after = balance_before`

No transaction record may be created.

Related requirements:

- FR-D05
- FR-W08

## INV-08 — Transaction Record Consistency

For every completed transaction:

`transaction.balance_after_transaction = account.balance`

Related requirements:

- FR-T01
- FR-T03

## INV-09 — Zero-Rate Interest

For every nonnegative principal:

`interest(principal, rate=0) = 0`

Related requirements:

- FR-I01

## INV-10 — Nonnegative Interest

For every nonnegative principal and nonnegative rate:

`calculated_interest >= 0`

Related requirements:

- FR-I02

## INV-11 — Interest Principal Monotonicity

For fixed positive rate and frequency:

If:

`principal_2 >= principal_1`

then:

`interest(principal_2) >= interest(principal_1)`

Related requirements:

- FR-I03

## INV-12 — Interest Rate Monotonicity

For fixed positive principal and frequency:

If:

`rate_2 >= rate_1`

then:

`interest(rate_2) >= interest(rate_1)`

Related requirements:

- FR-I04

## INV-13 — Interest Precision

The calculated interest result is rounded to two decimal places.

Related requirements:

- FR-I05
