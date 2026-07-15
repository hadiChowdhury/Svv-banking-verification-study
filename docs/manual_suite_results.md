# Manual PyTest Suite Results

## Test Suite

The manually designed suite applies:

- equivalence partitioning;
- boundary value analysis;
- explicit valid and invalid cases;
- state-transition verification;
- transaction-record consistency checks;
- selected account and interest-model checks.

## Execution Result

- Tests collected: 29
- Tests passed: 29
- Tests failed: 0
- Non-blocking warnings: 1

The warning originates from the upstream `django-celery-beat` dependency and
is unrelated to the selected financial transaction behaviour.

## Coverage Result

| Module | Coverage |
|---|---:|
| `accounts/models.py` | 96% |
| `transactions/forms.py` | 75% |
| `transactions/models.py` | 100% |
| `transactions/views.py` | 79% |
| **Overall** | **84%** |

The coverage run used branch measurement.

## Scope Interpretation

The remaining uncovered statements primarily belong to functionality excluded
from the experimental scope:

- transaction-report date-range validation;
- transaction-report filtering and presentation;
- unrelated user and address string representations.

No tests were added solely to increase coverage for behaviour outside the
declared financial verification scope.
