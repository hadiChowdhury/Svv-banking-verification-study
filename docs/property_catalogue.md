# Property-Based Verification Catalogue

## Purpose

The Hypothesis suite will express general properties over generated input
domains rather than relying on a fixed list of manually selected examples.

The property-based suite will be developed independently from the manual
PyTest suite while targeting the same production code and behavioural
requirements.

---

## PROP-01 — Valid Deposit Balance Correctness

For every valid deposit amount `A` and starting balance `B`:

`balance_after = B + A`

Constraints:

- `A >= minimum_deposit`;
- values remain within the model's supported decimal range.

Related invariants:

- INV-01

---

## PROP-02 — Deposit Monotonicity

For every valid positive deposit:

`balance_after > balance_before`

Related invariants:

- INV-01

---

## PROP-03 — Invalid Deposit Preservation

For every generated deposit below the configured minimum:

- the form is invalid;
- the balance remains unchanged;
- no transaction record is created.

Related invariants:

- INV-02
- INV-07

---

## PROP-04 — Valid Withdrawal Balance Correctness

For every valid withdrawal amount `A` and balance `B`:

`balance_after = B - A`

Constraints:

- `A >= minimum_withdrawal`;
- `A <= maximum_withdrawal`;
- `A <= B`.

Related invariants:

- INV-03

---

## PROP-05 — Withdrawal Minimum Enforcement

For every generated amount below the minimum withdrawal:

- the operation is rejected;
- the balance is unchanged.

Related invariants:

- INV-04
- INV-07

---

## PROP-06 — Withdrawal Maximum Enforcement

For every generated amount above the account-type maximum:

- the operation is rejected;
- the balance is unchanged.

Related invariants:

- INV-05
- INV-07

---

## PROP-07 — Withdrawal Available-Balance Enforcement

For every generated withdrawal greater than the account balance:

- the operation is rejected;
- the balance is unchanged.

Related invariants:

- INV-06
- INV-07

---

## PROP-08 — Exact-Balance Withdrawal

For every generated valid account state where the current balance satisfies
all configured withdrawal limits:

Withdrawing exactly the current balance must be accepted and produce:

`balance_after = 0`

Related invariants:

- INV-03
- INV-06

---

## PROP-09 — Transaction Record Consistency

For every successfully completed generated transaction:

`transaction.balance_after_transaction = account.balance`

Related invariants:

- INV-08

---

## PROP-10 — Zero-Rate Interest

For every generated nonnegative principal:

`calculate_interest(principal, rate=0) = 0`

Related invariants:

- INV-09

---

## PROP-11 — Nonnegative Interest

For every generated nonnegative principal and valid nonnegative rate:

`calculated_interest >= 0`

Related invariants:

- INV-10

---

## PROP-12 — Interest Principal Monotonicity

For generated principals where:

`P2 >= P1 >= 0`

and fixed valid positive rate and frequency:

`interest(P2) >= interest(P1)`

Related invariants:

- INV-11

---

## PROP-13 — Interest Rate Monotonicity

For generated rates where:

`R2 >= R1 >= 0`

and fixed positive principal and valid frequency:

`interest(R2) >= interest(R1)`

Related invariants:

- INV-12

---

## PROP-14 — Interest Precision

For every generated valid interest input:

The returned result must not contain more than two decimal places.

Related invariants:

- INV-13

---

# Input Strategy Guidelines

Hypothesis strategies will:

- use `Decimal` values rather than binary floating-point values;
- generate values with at most two decimal places for transaction amounts;
- respect the maximum range supported by Django model fields;
- generate valid and invalid domains separately;
- avoid excessive filtering with `assume`;
- use explicit lower and upper bounds;
- keep database-dependent examples deterministic and isolated.

---

# Independence Rule

The property-based suite must not simply parameterize the manually selected
EP/BVA examples.

Its primary assertions must be expressed as general invariants over generated
input domains.
