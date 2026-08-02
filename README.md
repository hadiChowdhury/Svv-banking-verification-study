# Manual Testing vs. Automated Verification

## A Comparative Adequacy Study Using Mutation Score

**Course:** ENGI-9839 — Software Verification and Validation
**Institution:** Memorial University of Newfoundland
**Student:** MD Abdul Hadi Chowdhury
**Instructor:** Raja Abbas

---

## Overview

This project compares two different ways of designing automated software tests for the financial transaction subsystem of an open-source Django banking application:

1. A manually designed test suite based on **Equivalence Partitioning (EP)** and **Boundary Value Analysis (BVA)**.
2. A property-based test suite implemented using **Hypothesis**.

The term **manual suite** refers to manual test-case design, not manual test execution. Both suites are executed automatically using `pytest`.

The project evaluates the two suites using:

- statement and branch coverage with `pytest-cov`;
- mutation testing with `mutmut`;
- manual analysis of surviving mutants; and
- comparison of behavioural reach and fault-detection strength.

The main purpose is to investigate whether differences in mutation score are caused by stronger test assertions, broader code reach, or an incomplete property catalogue.

---

## Research Question

The primary research question is:

> For the selected financial transaction subsystem, how does the mutation adequacy of a manually designed equivalence-partitioning and boundary-value test suite compare with that of a Hypothesis property-based test suite?

The project also examines:

1. Which suite achieves higher structural coverage?
2. Which suite reaches a broader range of financial behaviours?
3. Which categories of mutants survive?
4. What relationship exists between code coverage and mutation adequacy?

---

## Main Finding

The manually designed EP/BVA suite achieved broader behavioural reach and a higher controlled mutation score.

However, when only mutants reached by each suite were considered, the mutation scores were very close:

| Metric                      | Manual EP/BVA | Property-Based |
| --------------------------- | ------------: | -------------: |
| Test functions              |            29 |             16 |
| Overall structural coverage |           84% |            77% |
| Controlled mutation score   |        75.71% |         60.00% |
| Reached-mutant score        |        75.71% |         73.68% |

This suggests that the main difference came from **behavioural reach**, rather than a large difference in fault-detection strength within executed code.

The study therefore supports using EP/BVA and property-based testing as complementary techniques.

---

## Subject System

The subject system is the open-source Django banking application:

```text
saadmk11/banking-system
```

Original repository:

```text
https://github.com/saadmk11/banking-system
```

The evaluated upstream revision was pinned to:

```text
9c3ee3eea75030280405506c62d968d646981c05
```

The imported subject system is stored under:

```text
subject_system/banking_system/
```

Upstream repository details and the pinned commit are documented in:

```text
subject_system/UPSTREAM.md
```

---

## Selected Verification Scope

The study focuses on the following production modules:

```text
accounts/models.py
transactions/forms.py
transactions/models.py
transactions/views.py
```

These modules are represented in the repository under the controlled source copy used for testing.

The selected behaviours include:

- deposit validation;
- minimum deposit boundaries;
- withdrawal validation;
- minimum withdrawal boundaries;
- maximum withdrawal boundaries;
- rejection of withdrawals above the available balance;
- account balance increases after accepted deposits;
- account balance decreases after accepted withdrawals;
- preservation of state after rejected operations;
- transaction-record creation;
- correct transaction-account association;
- storage of the resulting account balance;
- interest calculation;
- monetary rounding;
- interest-calculation scheduling; and
- selected account-model helper behaviour.

---

## Excluded Functionality

The following areas were excluded from the experimental scope:

- authentication and authorization;
- account registration;
- administrative interfaces;
- HTML templates and visual presentation;
- Celery background tasks;
- Redis integration;
- email notifications;
- transaction report rendering;
- transaction date-range filtering; and
- deployment infrastructure.

The excluded date-range filtering functionality remained present in the source code. Therefore, `mutmut` still generated mutants for it. Since neither suite tested that feature, those mutants were classified as `no tests` and excluded symmetrically from the controlled comparison.

---

## Requirements and Invariants

The selected open-source project did not contain a complete formal requirements document for the financial subsystem.

The relevant requirements were therefore reconstructed from:

- form validation logic;
- Django model configuration;
- view-processing behaviour;
- database state changes; and
- observable transaction outcomes.

The project documents:

- **22 behavioural requirements**
- **13 financial invariants**

These are stored in:

```text
docs/requirements_specification.md
docs/invariants.md
```

Examples include:

```text
Accepted deposit:
balance_after = balance_before + deposit_amount
```

```text
Accepted withdrawal:
balance_after = balance_before - withdrawal_amount
```

```text
Rejected operation:
balance_after = balance_before
```

```text
Transaction record:
stored balance = actual resulting account balance
```

---

## Testing Approaches

### Manual EP/BVA Suite

Location:

```text
tests/manual/
```

The manual suite contains:

```text
29 pytest test functions
```

The suite was designed using:

- Equivalence Partitioning;
- Boundary Value Analysis;
- fixed expected-value assertions;
- validation checks;
- state-preservation checks;
- database persistence checks; and
- direct requirements-to-test traceability.

Example EP/BVA thinking:

If a minimum transaction value is required, the manual suite selects values:

- below the minimum;
- exactly at the minimum; and
- above the minimum.

The term `manual` means the test cases were manually selected and designed. The tests were still executed automatically using `pytest`.

---

### Property-Based Suite

Location:

```text
tests/property_based/
```

The property-based suite contains:

```text
16 Hypothesis property test functions
```

The suite uses automatically generated values for:

- deposits;
- withdrawals;
- account balances;
- interest rates;
- calculation frequencies; and
- transaction relationships.

Examples of tested properties include:

- every accepted deposit increases the balance by the exact deposited amount;
- every accepted withdrawal decreases the balance by the exact withdrawal amount;
- rejected operations preserve the original balance;
- withdrawals above the available balance are rejected;
- interest is non-negative for valid positive values;
- increasing the principal does not reduce interest when other values stay fixed; and
- interest results follow the implemented arithmetic relationship.

One property test function may be executed many times by Hypothesis using different generated inputs. Therefore, 16 property test functions do not mean that only 16 input values were tested.

---

## Tools and Technologies

| Tool          | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Programming language            |
| Django        | Subject-system framework        |
| pytest        | Test execution                  |
| Hypothesis    | Property-based input generation |
| pytest-django | Django integration for pytest   |
| pytest-cov    | Statement and branch coverage   |
| mutmut        | Mutation testing                |
| Git           | Version control                 |
| GitHub        | Repository hosting              |

---

## Verified Environment

The experiment was completed using:

| Component     | Version |
| ------------- | ------: |
| Python        | 3.10.20 |
| Django        |   3.2.9 |
| pytest        |   9.1.1 |
| pytest-django |  4.12.0 |
| pytest-cov    |   7.1.0 |
| Hypothesis    | 6.156.6 |
| mutmut        |   3.6.0 |

The project was executed in a Python virtual environment on macOS.

---

## Repository Structure

```text
Svv-banking-verification-study/
│
├── docs/
│   ├── requirements_specification.md
│   ├── invariants.md
│   ├── results_analysis.md
│   └── surviving_mutant_analysis.md
│
├── experiments/
│
├── presentation/
│
├── report/
│
├── results/
│   ├── coverage/
│   │   ├── manual_coverage.txt
│   │   ├── manual_coverage.json
│   │   ├── property_coverage.txt
│   │   └── property_coverage.json
│   │
│   └── mutation/
│       ├── manual/
│       ├── property_based/
│       ├── survivor_details/
│       └── comparison_summary.txt
│
├── scripts/
│   ├── prepare_mutation_workspace.sh
│   └── export_surviving_mutants.sh
│
├── src/
│   ├── accounts/
│   └── transactions/
│
├── subject_system/
│   ├── UPSTREAM.md
│   └── banking_system/
│
├── tests/
│   ├── manual/
│   │   ├── test_account_model_behavior.py
│   │   ├── test_deposit_validation.py
│   │   ├── test_interest_calculation.py
│   │   ├── test_transaction_processing.py
│   │   └── test_withdrawal_validation.py
│   │
│   └── property_based/
│       ├── test_deposit_properties.py
│       ├── test_transaction_properties.py
│       ├── test_withdrawal_properties.py
│       └── test_interest_properties.py
│
├── .gitignore
├── LICENSE
├── mutmut_pytest.ini
├── pytest.ini
├── README.md
├── requirements-baseline.txt
├── requirements-dev.txt
├── requirements.txt
└── setup.cfg
```

Generated folders such as `.venv`, `.pytest_cache`, `.hypothesis`, `mutants`, `__pycache__`, and coverage cache files are not required for reproduction or submission.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/hadiChowdhury/Svv-banking-verification-study.git
cd Svv-banking-verification-study
```

### 2. Create a virtual environment

Python 3.10 is recommended.

```bash
python3.10 -m venv .venv
```

### 3. Activate the virtual environment

macOS or Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running the Tests

### Manual EP/BVA suite

```bash
pytest -c mutmut_pytest.ini tests/manual -q
```

Expected result:

```text
29 passed
```

### Property-based suite

```bash
pytest -c mutmut_pytest.ini tests/property_based -q
```

Expected result:

```text
16 passed
```

---

## Collecting Structural Coverage

Coverage is measured only for the selected production modules.

### Manual suite coverage

```bash
pytest -c mutmut_pytest.ini tests/manual \
  --cov=accounts.models \
  --cov=transactions.forms \
  --cov=transactions.models \
  --cov=transactions.views \
  --cov-branch \
  --cov-report=term-missing
```

### Property-based suite coverage

```bash
pytest -c mutmut_pytest.ini tests/property_based \
  --cov=accounts.models \
  --cov=transactions.forms \
  --cov=transactions.models \
  --cov=transactions.views \
  --cov-branch \
  --cov-report=term-missing
```

---

## Generating HTML Coverage Reports

### Manual suite

```bash
pytest -c mutmut_pytest.ini tests/manual \
  --cov=accounts.models \
  --cov=transactions.forms \
  --cov=transactions.models \
  --cov=transactions.views \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=html:htmlcov/manual
```

Open:

```text
htmlcov/manual/index.html
```

### Property-based suite

```bash
pytest -c mutmut_pytest.ini tests/property_based \
  --cov=accounts.models \
  --cov=transactions.forms \
  --cov=transactions.models \
  --cov=transactions.views \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=html:htmlcov/property
```

Open:

```text
htmlcov/property/index.html
```

---

## Coverage Results

| Production module        | Manual EP/BVA | Property-Based |
| ------------------------ | ------------: | -------------: |
| `accounts/models.py`     |           96% |            79% |
| `transactions/forms.py`  |           75% |            75% |
| `transactions/models.py` |          100% |            92% |
| `transactions/views.py`  |           79% |            75% |
| **Overall**              |       **84%** |        **77%** |

The manual suite achieved seven percentage points more overall structural coverage.

The largest difference occurred in the account and interest calculation module.

Coverage reports are preserved under:

```text
results/coverage/
```

---

## Mutation Testing

Mutation testing was performed using `mutmut`.

A mutation is a small automatic change made to the production code.

For example:

```python
if amount > balance:
```

may be changed to:

```python
if amount >= balance:
```

Each changed program version is called a mutant.

Mutation outcomes are classified as:

- **Killed** — at least one test detected the change and failed.
- **Survived** — the tests ran, but all tests still passed.
- **No tests** — the mutated code was not executed by the selected suite.
- **Timeout** — the test execution took longer than the allowed time.

---

## Preparing the Mutation Workspace

The project includes a preparation script:

```bash
bash scripts/prepare_mutation_workspace.sh
```

Before a new complete mutation run, remove the existing generated workspace:

```bash
rm -rf mutants
```

---

## Running the Manual Mutation Experiment

Restore the manual mutation configuration:

```bash
cp results/mutation/manual/setup.cfg setup.cfg
```

Remove the existing mutation workspace:

```bash
rm -rf mutants
```

Run mutation testing:

```bash
mutmut run
```

Display the results:

```bash
mutmut results
```

Observed result:

```text
Generated: 96
Killed: 53
Survived: 17
No tests: 26
Timeout: 0
```

---

## Running the Property-Based Mutation Experiment

Restore the property-based mutation configuration:

```bash
cp results/mutation/property_based/setup.cfg setup.cfg
```

Remove the previous mutation workspace:

```bash
rm -rf mutants
```

Run mutation testing:

```bash
mutmut run
```

Display the results:

```bash
mutmut results
```

Observed result:

```text
Generated: 96
Killed: 42
Survived: 15
No tests: 39
Timeout: 0
```

---

## Inspecting Mutants

List mutation results:

```bash
mutmut results
```

Inspect a specific mutant:

```bash
mutmut show <mutant-id>
```

Example:

```bash
mutmut show transactions.forms.xǁTransactionFormǁ__init____mutmut_5
```

Exported survivor details are stored under:

```text
results/mutation/survivor_details/
```

The complete classification is documented in:

```text
docs/surviving_mutant_analysis.md
```

---

## Mutation Results

| Test suite     | Generated | Killed | Survived | No tests | Timeout |
| -------------- | --------: | -----: | -------: | -------: | ------: |
| Manual EP/BVA  |        96 |     53 |       17 |       26 |       0 |
| Property-Based |        96 |     42 |       15 |       39 |       0 |

---

## Controlled Relevant Mutant Population

Twenty-six mutants belonged to:

```text
TransactionDateRangeForm.clean_daterange
```

Transaction date-range filtering was declared outside the selected verification scope.

The same 26 mutants were classified as `no tests` in both runs and were excluded symmetrically from the controlled comparison.

```text
Relevant mutant population = 96 - 26 = 70
```

---

## Controlled Mutation Scores

The controlled mutation score is calculated as:

```text
Controlled mutation score =
Killed relevant mutants / Relevant mutant population × 100
```

### Manual EP/BVA suite

```text
53 / 70 × 100 = 75.71%
```

### Property-based suite

```text
42 / 70 × 100 = 60.00%
```

Difference:

```text
15.71 percentage points
```

---

## Reached-Mutant Scores

The reached-mutant score includes only killed and surviving mutants:

```text
Reached-mutant score =
Killed / (Killed + Survived) × 100
```

### Manual EP/BVA suite

```text
53 / (53 + 17) × 100 = 75.71%
```

### Property-based suite

```text
42 / (42 + 15) × 100 = 73.68%
```

Difference:

```text
2.03 percentage points
```

The much smaller reached-mutant difference shows that the main controlled-score difference was caused by behavioural reach.

---

## Survivor Analysis

The 17 manual-suite survivors were classified as:

| Category                                 |  Count |
| ---------------------------------------- | -----: |
| Genuine test weaknesses                  |      7 |
| Underspecified diagnostic-text behaviour |      7 |
| Equivalent or likely equivalent mutants  |      2 |
| Outside the core scope                   |      1 |
| **Total**                                | **17** |

The genuine test weaknesses involved:

- interest arithmetic;
- monetary rounding;
- interest-calculation scheduling; and
- positional form initialization.

Some surviving mutants changed only error-message wording without changing the financial decision.

Two mutants appeared equivalent or likely equivalent because the code changed without a clear observable behavioural difference.

---

## Key Results

### Test execution

| Suite          |    Result |
| -------------- | --------: |
| Manual EP/BVA  | 29 passed |
| Property-Based | 16 passed |

### Coverage

| Suite          | Overall coverage |
| -------------- | ---------------: |
| Manual EP/BVA  |              84% |
| Property-Based |              77% |

### Controlled mutation score

| Suite          |  Score |
| -------------- | -----: |
| Manual EP/BVA  | 75.71% |
| Property-Based | 60.00% |

### Reached-mutant score

| Suite          |  Score |
| -------------- | -----: |
| Manual EP/BVA  | 75.71% |
| Property-Based | 73.68% |

---

## Main Conclusions

The main conclusions are:

1. The manual EP/BVA suite achieved broader behavioural reach.
2. The manual suite achieved higher overall structural coverage.
3. The manual suite reached all 70 relevant mutants.
4. The property-based suite left 13 relevant mutants unexecuted.
5. The controlled mutation scores differed by 15.71 percentage points.
6. The reached-mutant scores differed by only 2.03 percentage points.
7. The major difference was behavioural reach, not a large difference in fault-detection strength within reached code.
8. Coverage alone did not fully explain test effectiveness.
9. Mutation testing revealed weaknesses that coverage percentages did not clearly show.
10. EP/BVA and property-based testing should be used together rather than treated as direct replacements.

This study does not claim that manually designed testing is universally better than property-based testing.

For this case study, the manual suite represented a broader set of selected behaviours, while both suites showed similar effectiveness within the code they reached.

---

## Reproducibility Artifacts

The repository preserves the following result files:

```text
results/coverage/manual_coverage.txt
results/coverage/manual_coverage.json
results/coverage/property_coverage.txt
results/coverage/property_coverage.json
```

```text
results/mutation/manual/
results/mutation/property_based/
results/mutation/comparison_summary.txt
results/mutation/survivor_details/
```

These files contain the outputs used in the final analysis and report.

---

## Report and Presentation

The complete report is stored under:

```text
report/
```

The presentation materials are stored under:

```text
presentation/
```

The report includes:

- background and related work;
- selected subject-system scope;
- reconstructed requirements;
- financial invariants;
- manual test design;
- property-based test design;
- coverage analysis;
- mutation analysis;
- survivor classification;
- threats to validity;
- reproduction instructions;
- recommendations; and
- execution evidence.

---

## Academic References

1. J. Hughes, "Software Testing with QuickCheck," in _Central European Functional Programming School: Third Summer School, CEFP 2009, Revised Selected Lectures_, LNCS 6299. Springer, 2010, pp. 183–223.

2. Y. Jia and M. Harman, "An Analysis and Survey of the Development of Mutation Testing," _IEEE Transactions on Software Engineering_, vol. 37, no. 5, pp. 649–678, 2011.

3. M. Papadakis, S. Yoo, D. Shin, and D.-H. Bae, "Are Mutation Scores Correlated with Real Fault Detection? A Large-Scale Empirical Study on the Relationship Between Mutants and Real Faults," in _Proceedings of the 40th International Conference on Software Engineering_, 2018, pp. 537–548.

4. S. Ravi and M. Coblenz, "An Empirical Evaluation of Property-Based Testing in Python," _Proceedings of the ACM on Programming Languages_, vol. 9, no. OOPSLA2, pp. 3897–3923, 2025.

5. saadmk11, "Banking System," GitHub repository. Evaluated revision `9c3ee3eea75030280405506c62d968d646981c05`.

---

## Attribution

The subject application used in this study was created by `saadmk11`.

Original repository:

```text
https://github.com/saadmk11/banking-system
```

The subject source was used as an open-source case study for software verification and testing.

---

## License

This repository was prepared as academic coursework for ENGI-9839, Software Verification and Validation, at Memorial University of Newfoundland.

The imported subject system remains subject to its original upstream licence.

See:

```text
LICENSE
subject_system/banking_system/LICENSE
```

for applicable licensing information.
