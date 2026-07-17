# Results Analysis

## 1. Experimental Overview

This experiment compared two test suites against the same financial transaction subsystem:

1. a manually designed PyTest suite based on Equivalence Partitioning and Boundary Value Analysis; and
2. a Hypothesis property-based testing suite based on financial invariants and generated inputs.

Both suites were executed against the same pinned subject-system version and the same mutation scope. Mutmut generated 96 mutants in each run. Twenty-six mutants belonged to `TransactionDateRangeForm.clean_daterange`, which was outside the declared financial-transaction scope. These mutants were excluded consistently from the primary controlled comparison, leaving 70 relevant mutants.

## 2. Test Execution Results

| Test suite | Test functions | Result | Execution time |
|---|---:|---:|---:|
| Manual PyTest | 29 | 29 passed | 0.78 s |
| Hypothesis property-based | 16 | 16 passed | 1.35 s |

The property-based test count refers to test functions rather than individual generated examples. Each Hypothesis test may execute many generated inputs.

## 3. Coverage Comparison

| Test suite | Statement/branch coverage |
|---|---:|
| Manual PyTest | 84% |
| Hypothesis property-based | 77% |

The manual suite achieved seven percentage points more coverage across the selected modules. This indicates that it exercised a broader range of implementation behaviours, including account-model helper methods not reached by the property-based suite.

Coverage alone does not establish fault-detection effectiveness. Mutation testing was therefore used as the primary adequacy metric.

## 4. Mutation Testing Results

### 4.1 Complete Mutmut Results

| Test suite | Total | Killed | Survived | No tests | Timeout |
|---|---:|---:|---:|---:|---:|
| Manual PyTest | 96 | 53 | 17 | 26 | 0 |
| Hypothesis property-based | 96 | 42 | 15 | 39 | 0 |

The 26 date-range mutants were outside the financial scope and were not exercised by either test suite.

The property-based suite had 13 additional in-scope mutants classified as having no tests:

- one mutant in `UserBankAccount.__str__`; and
- twelve mutants in `UserBankAccount.get_interest_calculation_months`.

These mutants were retained in the controlled comparison because they belong to the selected account-model scope and reveal a genuine difference in behavioural reach between the suites.

### 4.2 Controlled Mutation Scores

The controlled mutation score used the same 70 relevant mutants for both suites.

\[
\text{Mutation Score} =
\frac{\text{Killed Relevant Mutants}}
{\text{Total Relevant Mutants}}
\times 100
\]

| Test suite | Killed relevant mutants | Relevant mutants | Controlled score |
|---|---:|---:|---:|
| Manual PyTest | 53 | 70 | 75.71% |
| Hypothesis property-based | 42 | 70 | 60.00% |

The manual suite outperformed the property-based suite by:

\[
75.71\% - 60.00\% = 15.71
\]

percentage points.

### 4.3 Reached-Mutant Effectiveness

A secondary metric considers only mutants reached by each suite:

| Test suite | Killed | Survived | Reached-mutant score |
|---|---:|---:|---:|
| Manual PyTest | 53 | 17 | 75.71% |
| Hypothesis property-based | 42 | 15 | 73.68% |

The difference among reached mutants was only 2.03 percentage points. This suggests that the two techniques had similar fault-detection strength within the behaviours they exercised. The larger controlled-score difference was primarily caused by the broader behavioural reach of the manual suite.

## 5. Surviving-Mutant Analysis

The surviving mutants were concentrated in the following areas:

- transaction-form initialization;
- transaction-record saving;
- deposit minimum validation;
- withdrawal boundary and balance validation;
- interest calculation; and
- interest-calculation month handling.

Several survivors were shared by both suites. Shared survivors indicate either:

1. an assertion weakness common to both suites;
2. behaviour not sufficiently constrained by the requirements;
3. a semantically equivalent mutation; or
4. a mutation whose effect is not externally observable through the tested interface.

The manual suite additionally killed mutants in account helper behaviour that the property-based suite did not reach. This accounts for much of the final mutation-score difference.

Manual inspection of the 17 surviving mutants classified seven as genuine test weaknesses, two as equivalent or likely equivalent, seven as changes to underspecified diagnostic text, and one as outside the core financial scope. The genuine weaknesses were concentrated in interest arithmetic, currency rounding, interest-period scheduling, and positional form initialization. Full details are recorded in `docs/surviving_mutant_analysis.md`.

## 6. Coverage and Mutation Adequacy

The experiment produced the following relationship:

| Test suite | Coverage | Controlled mutation score |
|---|---:|---:|
| Manual PyTest | 84% | 75.71% |
| Hypothesis property-based | 77% | 60.00% |

The suite with higher coverage also achieved the higher controlled mutation score. However, the relationship was not proportional. The coverage difference was seven percentage points, while the mutation-score difference was 15.71 percentage points.

This supports the view that structural coverage and mutation adequacy measure different qualities. Coverage identifies whether code was executed, whereas mutation testing evaluates whether the test assertions can detect behavioural changes.

## 7. Answer to the Research Question

For the selected Django financial subsystem, the manually designed EP/BVA suite achieved greater overall mutation adequacy than the Hypothesis property-based suite.

The manual suite achieved a controlled mutation score of 75.71%, compared with 60.00% for the property-based suite. The result was primarily caused by the manual suite exercising a broader range of account and transaction behaviours.

Within code reached by each suite, their mutation scores were similar: 75.71% for the manual suite and 73.68% for the property-based suite. Therefore, the evidence does not show that property-based testing was substantially weaker at detecting faults in exercised behaviour. Instead, it shows that the current property catalogue had narrower behavioural coverage.

The findings support using both techniques together:

- manually designed tests provide explicit specification and boundary coverage; and
- property-based tests provide broad input variation for selected invariants.

## 8. Threats to Validity

### Internal Validity

The experiment used the same source version, environment, mutation tool, target files, and generated mutant population. Only the selected test suite changed between mutation runs.

A copied `src/` workspace was required because Mutmut could not correctly map the subject system's nonstandard nested import path. The workspace was generated directly from the pinned source through a reproducible script and was checked for source equivalence before execution.

### Construct Validity

Mutation score was used as the primary proxy for fault-detection adequacy. Mutants are artificial faults and may not perfectly represent real defects.

Some surviving mutants may be equivalent, meaning that they do not produce an observable behavioural difference. Until all survivors are manually classified, the reported scores should be interpreted as conservative adequacy estimates.

### External Validity

The experiment concerns one Django banking system and a limited financial subsystem. The results should not be generalized to all systems, domains, or property-based testing approaches.

The quality of the result depends on the selected manual test cases and property catalogue. A broader property suite might produce a different outcome.

### Conclusion Validity

The study compares two concrete test suites rather than proving that one testing technique is universally superior. Test-function counts are also not directly comparable because one Hypothesis function executes multiple generated examples.

No mutation timeouts or suspicious outcomes occurred, reducing the risk that infrastructure instability distorted the comparison.
