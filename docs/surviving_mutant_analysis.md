# Surviving Mutant Analysis

## 1. Method

The surviving mutants from the manual PyTest mutation run were inspected
individually using `mutmut show`. The property-based survivors were a subset
of the same surviving mutant population, so inspecting the 17 manual
survivors covered all surviving mutations observed in the experiment.

Each mutant was classified as one of the following:

- **Genuine test weakness**: changes relevant observable behaviour that the
  suite should detect.
- **Equivalent mutant**: does not change observable behaviour under the valid
  input domain.
- **Underspecified behaviour**: changes behaviour, such as exact diagnostic
  wording, that is not constrained by the requirements.
- **Outside core scope**: affects presentation or another concern excluded
  from the financial verification scope.

## 2. Classification Table

| No. | Mutant | Behavioural change | Classification | Rationale |
|---:|---|---|---|---|
| 1 | `BankAccountType.calculate_interest_mutmut_10` | Replaces division by frequency with multiplication | Genuine test weakness | Produces incorrect interest for frequencies greater than one. Existing cases did not distinguish the operators. |
| 2 | `BankAccountType.calculate_interest_mutmut_11` | Changes percentage conversion from `r / 100` to `r * 100` | Genuine test weakness | Substantially changes financial arithmetic and should be detected by an exact expected-value assertion. |
| 3 | `BankAccountType.calculate_interest_mutmut_12` | Changes percentage divisor from 100 to 101 | Genuine test weakness | Introduces a subtle arithmetic error that survives because current values or assertions are insufficiently discriminating. |
| 4 | `BankAccountType.calculate_interest_mutmut_14` | Removes two-decimal rounding by passing `None` | Genuine test weakness | Violates the expected currency precision behaviour for fractional results. |
| 5 | `BankAccountType.calculate_interest_mutmut_16` | Removes the rounding precision argument | Genuine test weakness | Can return whole-number rounding instead of two-decimal monetary precision. |
| 6 | `UserBankAccount.get_interest_calculation_months_mutmut_4` | Changes `12 / frequency` to `13 / frequency` | Likely equivalent mutant | For the normal valid frequencies that divide 12, integer conversion produces the same interval; annual frequency also produces the same observable month list. |
| 7 | `UserBankAccount.get_interest_calculation_months_mutmut_11` | Removes the interval argument from `range` | Genuine test weakness | Changes configured periodic calculation months into every-month calculation. |
| 8 | `DepositForm.clean_amount_mutmut_7` | Replaces minimum-deposit error text with `None` | Underspecified behaviour | The deposit is still rejected. Exact diagnostic wording was not specified as a financial requirement. |
| 9 | `TransactionForm.__init___mutmut_11` | Replaces `HiddenInput` with `None` | Outside core scope | Affects form rendering and presentation, not the financial transaction rules being compared. |
| 10 | `TransactionForm.__init___mutmut_5` | Drops positional arguments passed to the parent form constructor | Genuine interface weakness | Positional form data or files would no longer be processed correctly. Existing tests construct forms using keyword arguments only. |
| 11 | `TransactionForm.save_mutmut_1` | Changes the default `commit` value from true to false | Equivalent mutant | The implementation does not use or forward the `commit` parameter, so changing its default does not affect the save behaviour. |
| 12 | `WithdrawForm.clean_amount_mutmut_10` | Replaces minimum-withdrawal error text with `None` | Underspecified behaviour | Validation still rejects the invalid amount; only the diagnostic text changes. |
| 13 | `WithdrawForm.clean_amount_mutmut_12` | Replaces maximum-withdrawal error text with `None` | Underspecified behaviour | Validation still rejects the invalid amount; only the diagnostic text changes. |
| 14 | `WithdrawForm.clean_amount_mutmut_14` | Replaces insufficient-balance error text with `None` | Underspecified behaviour | The withdrawal remains rejected and account state is preserved. |
| 15 | `WithdrawForm.clean_amount_mutmut_15` | Adds characters around an error-message sentence | Underspecified behaviour | Only presentation wording changes. |
| 16 | `WithdrawForm.clean_amount_mutmut_16` | Changes capitalization in an error message | Underspecified behaviour | Only capitalization changes; financial behaviour is identical. |
| 17 | `WithdrawForm.clean_amount_mutmut_17` | Converts an error-message sentence to uppercase | Underspecified behaviour | Only capitalization changes; financial behaviour is identical. |

## 3. Classification Summary

| Classification | Count |
|---|---:|
| Genuine test weakness | 7 |
| Equivalent mutant | 2 |
| Underspecified behaviour | 7 |
| Outside core scope | 1 |
| Total | 17 |

The two equivalent classifications include the `TransactionForm.save` default
argument mutation and the likely equivalent interest-interval mutation under
the valid frequency domain.

## 4. Interpretation

The unadjusted mutation score remains the primary experimental result because
mutation outcomes must not be changed retroactively after manual inspection.

However, survivor classification shows that not all surviving mutants
represent equally important deficiencies. Seven survivors exposed genuine
assertion or input-selection weaknesses, especially in interest arithmetic,
rounding, periodic-interest scheduling, and positional form initialization.

Seven mutants changed only validation-message text. The suites verified that
invalid operations were rejected and that financial state remained safe, but
they did not assert exact message wording. Because exact wording was not part
of the declared financial requirements, these mutants are classified as
underspecified rather than core fault-detection failures.

One mutant affected the form widget used for display and was outside the
financial scope. Two mutants were equivalent or likely equivalent under the
valid execution domain.

## 5. Implications for the Comparison

Most genuine arithmetic survivors were shared by both suites. This indicates
that both the manually designed and property-based suites could be improved
through more discriminating expected-value assertions and a broader set of
interest frequencies.

The manual suite nevertheless achieved broader behavioural reach because it
executed account helper methods that the property-based suite did not reach.
The classification therefore supports the earlier conclusion:

- the two suites had similar effectiveness within behaviours they exercised;
- the manual suite exercised a broader part of the selected subsystem; and
- both suites shared weaknesses in exact interest-calculation verification.

No tests were added after observing the mutants, because doing so would alter
the original baseline comparison. The surviving mutants are used as
diagnostic evidence and as recommendations for future test-suite improvement.
