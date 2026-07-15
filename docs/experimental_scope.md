# Experimental Scope

## Subject System

The subject system is the open-source `saadmk11/banking-system`
application pinned at commit:

`9c3ee3eea75030280405506c62d968d646981c05`

The system is implemented using Python and Django and provides banking
functionality including deposits, withdrawals, balance management,
transaction records, account types, transaction limits, and interest
calculation.

## Selected Subsystem

The experiment is restricted to the financial transaction subsystem and
the account-domain logic directly required by that subsystem.

The primary production files are:

- `transactions/forms.py`
- `transactions/models.py`
- `transactions/views.py`
- `accounts/models.py`

The initial mutation target will prioritize:

- transaction validation in `transactions/forms.py`;
- financial calculations in `accounts/models.py`.

Transaction state updates in `transactions/views.py` may be included after
the test harness is validated and mutation runtime is measured.

## Included Behaviour

The following behaviour is included:

- minimum deposit validation;
- deposit balance updates;
- minimum withdrawal validation;
- maximum withdrawal validation;
- insufficient-balance validation;
- withdrawal balance updates;
- transaction balance recording;
- interest calculation;
- selected interest scheduling behaviour where directly relevant.

## Excluded Behaviour

The following behaviour is outside the primary experiment:

- authentication;
- user registration;
- administrative functionality;
- HTML templates;
- CSS and presentation logic;
- URL routing;
- transaction-report filtering;
- Celery worker execution;
- Redis communication;
- unrelated account-profile behaviour.

These components are excluded because they do not directly contribute to
the financial invariants evaluated by the research question.

## Experimental Units

Two independently developed test suites will evaluate the same selected
production code:

1. a manually designed PyTest suite using equivalence partitioning and
   boundary value analysis;
2. a Hypothesis property-based suite using generated input domains and
   invariant-based assertions.

The suites will be executed separately during coverage and mutation
analysis.

## Controlled Conditions

The comparison will use:

- the same pinned upstream source revision;
- the same Python environment;
- the same dependency versions;
- the same production-code scope;
- the same mutation tool;
- the same mutation operators;
- separate execution of each test suite;
- no use of upstream tests in the primary comparison.

No production behaviour will be modified merely to improve coverage or
mutation score.
