# Manual Test Design

## Test Design Approach

The manual PyTest suite will be designed using specification-based techniques:

- equivalence partitioning;
- boundary value analysis;
- valid and invalid input classes;
- state-transition assertions;
- expected exception and rejection behaviour.

The manual suite will contain explicitly selected test cases. It will not use
Hypothesis-generated inputs.

---

# Deposit Test Design

Assume:

- minimum deposit amount = `M`;
- initial balance = `B`;
- deposit amount = `A`.

## Deposit Equivalence Partitions

| Partition ID | Input Condition | Classification | Expected Behaviour  |
| ------------ | --------------- | -------------- | ------------------- |
| DEP-EP-01    | `A < M`         | Invalid        | Deposit is rejected |
| DEP-EP-02    | `A = M`         | Valid          | Deposit is accepted |
| DEP-EP-03    | `A > M`         | Valid          | Deposit is accepted |

## Deposit Boundary Values

| Test ID    | Test Value | Expected Result |
| ---------- | ---------- | --------------- |
| DEP-BVA-01 | `M - 0.01` | Rejected        |
| DEP-BVA-02 | `M`        | Accepted        |
| DEP-BVA-03 | `M + 0.01` | Accepted        |

## Deposit State Assertions

For an accepted deposit:

`balance_after = balance_before + amount`

For a rejected deposit:

`balance_after = balance_before`

No transaction record should be created for a rejected deposit.

---

# Withdrawal Test Design

Assume:

- minimum withdrawal amount = `MIN`;
- maximum withdrawal amount = `MAX`;
- current account balance = `B`;
- requested withdrawal amount = `A`.

## Withdrawal Equivalence Partitions

| Partition ID | Input Condition                                    | Classification | Expected Behaviour     |
| ------------ | -------------------------------------------------- | -------------- | ---------------------- |
| WIT-EP-01    | `A < MIN`                                          | Invalid        | Withdrawal is rejected |
| WIT-EP-02    | `MIN <= A <= MAX` and `A <= B`                     | Valid          | Withdrawal is accepted |
| WIT-EP-03    | `A > MAX`                                          | Invalid        | Withdrawal is rejected |
| WIT-EP-04    | `A > B`                                            | Invalid        | Withdrawal is rejected |
| WIT-EP-05    | `A = B`, while all configured limits are satisfied | Valid          | Withdrawal is accepted |

## Minimum Withdrawal Boundary Values

| Test ID        | Test Value   | Expected Result |
| -------------- | ------------ | --------------- |
| WIT-MIN-BVA-01 | `MIN - 0.01` | Rejected        |
| WIT-MIN-BVA-02 | `MIN`        | Accepted        |
| WIT-MIN-BVA-03 | `MIN + 0.01` | Accepted        |

## Maximum Withdrawal Boundary Values

| Test ID        | Test Value   | Expected Result |
| -------------- | ------------ | --------------- |
| WIT-MAX-BVA-01 | `MAX - 0.01` | Accepted        |
| WIT-MAX-BVA-02 | `MAX`        | Accepted        |
| WIT-MAX-BVA-03 | `MAX + 0.01` | Rejected        |

## Available-Balance Boundary Values

| Test ID        | Test Value | Expected Result |
| -------------- | ---------- | --------------- |
| WIT-BAL-BVA-01 | `B - 0.01` | Accepted        |
| WIT-BAL-BVA-02 | `B`        | Accepted        |
| WIT-BAL-BVA-03 | `B + 0.01` | Rejected        |

## Withdrawal State Assertions

For an accepted withdrawal:

`balance_after = balance_before - amount`

For a rejected withdrawal:

`balance_after = balance_before`

No transaction record should be created for a rejected withdrawal.

---

# Transaction Record Test Design

| Test ID | Condition                     | Expected Result                               |
| ------- | ----------------------------- | --------------------------------------------- |
| TRN-01  | Valid deposit completed       | Transaction references the correct account    |
| TRN-02  | Valid withdrawal completed    | Transaction references the correct account    |
| TRN-03  | Valid transaction completed   | Stored transaction type is correct            |
| TRN-04  | Valid transaction completed   | Recorded balance equals final account balance |
| TRN-05  | Invalid transaction submitted | No transaction record is created              |

---

# Interest Calculation Test Design

Assume:

- principal = `P`;
- annual interest rate = `R`;
- calculation frequency = `N`.

## Interest Equivalence Partitions

| Partition ID | Input Condition                               | Expected Behaviour         |
| ------------ | --------------------------------------------- | -------------------------- |
| INT-EP-01    | `P = 0`                                       | Interest equals zero       |
| INT-EP-02    | `P > 0`, `R = 0`                              | Interest equals zero       |
| INT-EP-03    | `P > 0`, `R > 0`                              | Interest is positive       |
| INT-EP-04    | Larger valid principal with fixed `R` and `N` | Interest does not decrease |
| INT-EP-05    | Larger valid rate with fixed `P` and `N`      | Interest does not decrease |

## Interest Boundary Values

| Test ID    | Input     | Expected Result                |
| ---------- | --------- | ------------------------------ |
| INT-BVA-01 | `P = 0`   | Interest equals `0.00`         |
| INT-BVA-02 | `R = 0`   | Interest equals `0.00`         |
| INT-BVA-03 | `R = 100` | Valid upper model boundary     |
| INT-BVA-04 | `N = 1`   | Valid lower frequency boundary |
| INT-BVA-05 | `N = 12`  | Valid upper frequency boundary |

---

# Traceability

| Requirement | Manual Test Design Coverage          |
| ----------- | ------------------------------------ |
| FR-D01      | DEP-EP-01, DEP-BVA-01                |
| FR-D02      | Deposit state assertions             |
| FR-D03      | DEP-EP-02, DEP-EP-03                 |
| FR-D04      | DEP-BVA-02                           |
| FR-D05      | Rejected deposit state assertion     |
| FR-W01      | WIT-EP-01, WIT-MIN-BVA-01            |
| FR-W02      | WIT-EP-03, WIT-MAX-BVA-03            |
| FR-W03      | WIT-EP-04, WIT-BAL-BVA-03            |
| FR-W04      | Withdrawal state assertions          |
| FR-W05      | WIT-MIN-BVA-02                       |
| FR-W06      | WIT-MAX-BVA-02                       |
| FR-W07      | WIT-BAL-BVA-02                       |
| FR-W08      | Rejected withdrawal state assertion  |
| FR-T01      | TRN-01, TRN-02                       |
| FR-T02      | TRN-03                               |
| FR-T03      | TRN-04                               |
| FR-I01      | INT-EP-02                            |
| FR-I02      | INT-EP-03                            |
| FR-I03      | INT-EP-04                            |
| FR-I04      | INT-EP-05                            |
| FR-I05      | Interest result precision assertions |
