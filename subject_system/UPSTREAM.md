# Upstream Subject System

## Project

Online Banking System

## Original Repository

https://github.com/saadmk11/banking-system

## Original Author

Saad Ali Khan (`saadmk11`)

## Upstream Branch

`master`

## Pinned Upstream Commit

`9c3ee3eea75030280405506c62d968d646981c05`

The experiment uses the exact upstream revision identified above. Pinning the
commit ensures that the subject system remains reproducible even if the original
repository changes after the experiment is completed.

## License

MIT License

The original upstream license is preserved inside:

`subject_system/banking_system/LICENSE`

## Subject-System Description

The upstream project is an online banking application implemented using Python
and the Django web framework. Its functionality includes account creation,
deposits, withdrawals, current and savings account types, transaction records,
balance tracking, transaction amount restrictions, and interest calculations.

## Experimental Scope

The study does not attempt to verify the complete web application. The
experimental scope is restricted to the financial transaction subsystem and its
direct dependencies.

The initial candidate functionality includes:

- deposit processing;
- withdrawal processing;
- account balance updates;
- minimum and maximum transaction restrictions;
- insufficient-balance behavior;
- transaction-record consistency;
- selected interest-related behavior, if feasible.

User-interface templates, styling, authentication pages, administrative
features, and unrelated infrastructure are excluded unless required by the
selected transaction logic.

## Local Modifications

Any compatibility changes or experimental instrumentation applied to the
upstream source will be documented separately. Changes will not be made merely
to improve coverage or mutation scores.
