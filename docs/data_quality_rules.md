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

## Silver Quality Rules

Silver quality rules focus on producing trusted current records from Bronze:

- Customers require non-null `customer_id`, `customer_name`, and `signup_date`.
- Products require non-null `product_id`, positive `unit_price`, and non-negative `unit_cost`.
- Campaigns require non-null `campaign_id`, `channel`, and `campaign_start_date`.
- Orders require non-null `order_id`, valid `customer_id`, valid `product_id`, non-negative `total_amount`, and valid `payment_status`.
- Ad spend requires non-null `spend_id`, valid `campaign_id`, non-negative `spend_amount`, and non-negative `impressions`, `clicks`, and `conversions`.
- Support tickets require non-null `ticket_id`, valid `customer_id`, valid `created_at`, and valid `status`.
- Silver deduplication keeps one current record per source business key using `source_updated_at`, then `ingested_at`, then `row_hash`.
- Silver records should include `dq_status` and `dq_issue_reason` so rejected or warning records are visible before Gold modeling.
- Referential checks should confirm orders, ad spend, and support tickets link to valid Silver parent entities.

## Monitoring Approach

Quality checks should produce pass/fail counts, failed row samples, and run timestamps. Critical failures should block Gold table publication once orchestration is introduced.
