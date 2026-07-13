# Manual Testing vs. Automated Verification: A Comparative Adequacy Study Using Mutation Score as an Objective Evaluation Metric

**Course:** ENGI 9839 — Software Verification and Validation  
**Institution:** Memorial University of Newfoundland  
**Author:** Md Abdul Hadi Chowdhury  
**Supervisor:** Raja Abbas  

---

## Overview

This project compares two fundamentally different testing paradigms — **manual unit testing** (PyTest) and **automated property-based verification** (Hypothesis) — applied to the same Python subject system, and evaluates both using **mutation score** as a shared, objective adequacy criterion.

The central premise is that code coverage, the most widely used measure of test suite completeness, does not reliably reflect a suite's ability to detect real faults. Mutation testing provides a stronger signal: it seeds small syntactic faults into the source code and measures what fraction of them the test suite detects. By running the same mutation pipeline against two independently constructed test suites — one manual, one automated — this project produces an empirical, head-to-head comparison of fault-detection capability across the two paradigms.

---

## Research Questions

| # | Research Question |
|---|---|
| **RQ1** | Does automated property-based testing (Hypothesis) achieve a higher mutation score than manual unit testing (PyTest) on the same subject system? |
| **RQ2** | What categories of faults does each approach detect that the other systematically fails to expose? |
| **RQ3** | Does code coverage accurately predict mutation score under either testing paradigm, or does it overestimate test suite adequacy in both cases? |

---

## Subject System

The subject system is a hand-written Python financial transaction module (`src/transaction.py`) comprising the `BankAccount` class with the following operations:

| Method | Description |
|---|---|
| `deposit(amount)` | Deposits a positive amount; raises `InvalidAmountError` otherwise |
| `withdraw(amount)` | Withdraws a positive amount within balance; raises `InsufficientFundsError` on overdraft |
| `transfer(target, amount)` | Atomically moves funds between two accounts |
| `get_net_balance()` | Recomputes balance from transaction history as a consistency check |
| `get_total_deposited()` | Aggregates all inflows |
| `get_total_withdrawn()` | Aggregates all outflows |
| `get_statement()` | Returns a formatted transaction history string |

The module was designed with rich, well-defined logical invariants to give both testing approaches meaningful properties to verify:

- **P1** — Balance is always non-negative
- **P2** — Deposit strictly increases balance by the exact deposited amount
- **P3** — Withdrawal strictly decreases balance by the exact withdrawn amount
- **P4** — `deposit(x)` followed by `withdraw(x)` restores the original balance
- **P5** — Transfer conserves total money across both accounts
- **P6** — Net balance computed from transaction history always equals the stored balance
- **P7** — All invalid inputs are rejected with the correct exception type

---

## Methodology

### Approach A — Manual Unit Testing (PyTest)
A hand-crafted test suite developed using conventional unit testing techniques: equivalence partitioning, boundary value analysis, and error guessing. The engineer manually reasons about specific input–output pairs. This approach is bounded by human judgment and susceptible to blind spots at unanticipated boundary conditions.

**Test count:** 41 test cases across 7 test classes  
**File:** `tests/test_manual_pytest.py`

### Approach B — Automated Property-Based Verification (Hypothesis)
An independent test suite constructed using the Hypothesis library, in which tests are expressed as universally quantified logical properties over automatically generated inputs. Rather than enumerating specific cases, each test asserts an invariant that must hold across the entire valid input domain. Hypothesis generates hundreds of input combinations per property, actively searching for counterexamples.

**Test count:** 21 property tests covering all 7 formal properties  
**File:** `tests/test_automated_hypothesis.py`

### Evaluation — Mutation Analysis (mutmut)
Both suites are evaluated using `mutmut`, a Python mutation testing framework. Mutmut introduces small syntactic mutations into the source code (e.g., changing `>` to `>=`, `+` to `-`, `True` to `False`) and runs the test suite against each mutant. A mutant is **killed** if at least one test fails on it; it **survives** if all tests pass. The mutation score is:

```
Mutation Score = (Killed Mutants) / (Killed + Survived Mutants) × 100%
```

The same mutation pipeline is run separately against each suite under identical conditions, producing two mutation scores for direct comparison.

---

## Repository Structure

```
ENGI9839-mutation-study/
│
├── src/
│   ├── __init__.py
│   └── transaction.py                    # Subject system under test
│
├── tests/
│   ├── __init__.py
│   ├── test_manual_pytest.py             # Approach A: Manual unit tests
│   └── test_automated_hypothesis.py      # Approach B: Property-based tests
│
├── mutation/
│   ├── run_mutation.sh                   # One-command mutation runner
│   └── results/                          # Auto-generated mutation output
│       ├── mutmut_pytest_summary.txt
│       ├── mutmut_hypothesis_summary.txt
│       └── *.xml
│
├── analysis/
│   ├── compare_scores.py                 # Coverage vs mutation score charts
│   └── figures/                          # Auto-generated plots
│
├── report/                               # LaTeX project report
├── slides/                               # Presentation slides
│
├── setup.cfg                             # pytest and mutmut configuration
├── requirements.txt                      # Python dependencies
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ENGI9839-mutation-study.git
cd ENGI9839-mutation-study
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Tests

### Approach A — Manual Unit Tests

```bash
pytest tests/test_manual_pytest.py -v
```

### Approach B — Automated Property-Based Tests

```bash
pytest tests/test_automated_hypothesis.py -v
```

### Both suites with coverage report

```bash
# Coverage for Approach A
pytest tests/test_manual_pytest.py \
  --cov=src \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=html:htmlcov/pytest

# Coverage for Approach B
pytest tests/test_automated_hypothesis.py \
  --cov=src \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=html:htmlcov/hypothesis
```

Coverage HTML reports are saved to `htmlcov/pytest/` and `htmlcov/hypothesis/` respectively.

---

## Running Mutation Analysis

> ⚠️ Mutation testing is computationally intensive. Expect **15–40 minutes** per run depending on hardware.

```bash
# Against Approach A (manual PyTest suite) only
bash mutation/run_mutation.sh pytest

# Against Approach B (Hypothesis suite) only
bash mutation/run_mutation.sh hypothesis

# Against both suites sequentially
bash mutation/run_mutation.sh both
```

Results are saved to `mutation/results/`.

### Inspecting individual mutants

```bash
# Overall summary
mutmut results

# Show survived mutants only
mutmut results --suspicious
mutmut results --survived

# See the diff for a specific mutant
mutmut show <mutant_id>

# Apply a mutant to the source temporarily
mutmut apply <mutant_id>
# (restore with git checkout src/)
```

---

## Generating Analysis Charts

```bash
python analysis/compare_scores.py
```

Figures are saved to `analysis/figures/`:
- `mutation_score_comparison.png` — side-by-side mutation scores for both suites
- `coverage_vs_mutation.png` — scatter plot of coverage vs mutation score
- `survived_mutant_categories.png` — breakdown of survived mutant types per suite

---

## Branching Strategy

```
main
│
├── develop
│   ├── feature/subject-system         ← src/transaction.py
│   ├── feature/pytest-suite           ← Approach A test suite
│   ├── feature/hypothesis-suite       ← Approach B test suite
│   ├── feature/mutation-analysis      ← mutmut results and analysis scripts
│   └── feature/report-slides          ← final report and presentation
```

Each feature branch is opened as a pull request into `develop`. Final merge to `main` at submission.

---

## Key References

1. K. Claessen and J. Hughes, "QuickCheck: A lightweight tool for random testing of Haskell programs," *ACM ICFP*, 2000.
2. M. Papadakis et al., "Mutation testing advances: An analysis and survey," *Advances in Computers*, vol. 112, 2019.
3. L. Inozemtseva and R. Holmes, "Coverage is not strongly correlated with test suite effectiveness," *ICSE*, 2014.
4. K. Jain et al., "Mind the gap: The difference between coverage and mutation score can guide testing efforts," *ICSTW*, 2023.
5. G. Petrović and M. Ivanković, "Practical mutation testing at scale: A view from Google," *IEEE TSE*, 2022.
6. S. Ravi and M. Coblenz, "An empirical evaluation of property-based testing in Python," *ACM OOPSLA2*, 2025.

---

## License

This repository is submitted as academic coursework for ENGI 9839 at Memorial University of Newfoundland. Not licensed for reuse.
