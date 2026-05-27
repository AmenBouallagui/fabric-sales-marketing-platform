# Data Quality Rules

## Purpose

Data quality checks ensure the platform produces trustworthy reporting outputs and AI-ready data products. These rules will be implemented first as test definitions and later as automated validation steps in notebooks or pipelines.

## Completeness Rules

- Accounts must have an account identifier, account name, segment, and region.
- Opportunities must have an opportunity identifier, account identifier, stage, amount, created date, and expected close date.
- Campaign interactions must have a campaign identifier, contact or lead identifier, interaction type, and interaction timestamp.
- Revenue transactions must have an account identifier, product identifier, transaction date, and revenue amount.

## Validity Rules

- Opportunity amount must be greater than or equal to zero.
- Probability must be between 0 and 1 or between 0 and 100, depending on the chosen standard.
- Close date must not be earlier than opportunity created date.
- Campaign start date must not be later than campaign end date.
- Email addresses must follow a valid email-like pattern when present.

## Consistency Rules

- Lead status values must map to an approved lifecycle list.
- Opportunity stages must map to an approved sales stage list.
- Currency values must use a consistent ISO currency code.
- Region and country values must use standardized reference values.

## Referential Integrity Rules

- Every opportunity account identifier should exist in the account domain.
- Every campaign interaction campaign identifier should exist in the campaign domain.
- Every revenue transaction product identifier should exist in the product domain.

## Monitoring Approach

Quality checks should produce pass/fail counts, failed row samples, and run timestamps. Critical failures should block Gold table publication once orchestration is introduced.
