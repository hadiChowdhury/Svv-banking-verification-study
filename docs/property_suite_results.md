# Hypothesis Property-Based Suite Results

## Test Suite

The property-based suite expresses general financial invariants over generated
input domains using Hypothesis.

The suite includes generated properties for:

- valid and invalid deposits;
- deposit monotonicity;
- valid and invalid withdrawals;
- minimum, maximum, and available-balance enforcement;
- exact-balance withdrawals;
- end-to-end account balance updates;
- transaction-record consistency;
- zero-rate interest;
- nonnegative interest;
- principal monotonicity;
- interest-rate monotonicity;
- two-decimal interest precision.

## Execution Result

- Property test functions collected: 16
- Property test functions passed: 16
- Property test functions failed: 0
- Non-blocking warnings: 1

Each property test executes multiple generated examples. The end-to-end deposit
and withdrawal properties are configured to execute up to 50 generated examples
each.

The warning originates from the upstream `django-celery-beat` dependency and is
unrelated to the selected financial transaction behaviour.

## Coverage Result

| Module | Coverage |
|---|---:|
| `accounts/models.py` | 79% |
| `transactions/forms.py` | 75% |
| `transactions/models.py` | 92% |
| `transactions/views.py` | 75% |
| **Overall** | **77%** |

The coverage run used branch measurement.

## Initial Comparison

The manual PyTest suite achieved 84% overall coverage, while the property-based
suite achieved 77%.

This difference will not be treated as a direct measure of fault-detection
effectiveness. The primary adequacy criterion for the experiment is mutation
score. Coverage is retained as a secondary metric so that its relationship with
mutation effectiveness can be examined.
