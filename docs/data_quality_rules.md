# Data Quality Rules

## Purpose

Data quality checks ensure the platform produces trustworthy reporting outputs and AI-ready data products. These rules will be implemented first as test definitions and later as automated validation steps in notebooks or pipelines.

## Completeness Rules

- Customers must have `customer_id`, `customer_name`, and `signup_date`.
- Products must have `product_id`, `product_name`, `unit_price`, and `unit_cost`.
- Campaigns must have `campaign_id`, `channel`, and `campaign_start_date`.
- Orders must have `order_id`, `customer_id`, `product_id`, `order_date`, `total_amount`, and `payment_status`.
- Ad spend records must have `spend_id`, `campaign_id`, `spend_date`, and `spend_amount`.
- Support tickets must have `ticket_id`, `customer_id`, `created_at`, and `status`.

## Validity Rules

- Product `unit_price` must be greater than zero.
- Product `unit_cost` must be greater than or equal to zero.
- Order `total_amount`, `unit_price`, `discount_amount`, and `tax_amount` must be greater than or equal to zero.
- Ad spend `spend_amount`, `impressions`, `clicks`, and `conversions` must be greater than or equal to zero.
- Campaign start date must not be later than campaign end date when an end date is present.
- Support ticket closed timestamp must not be earlier than created timestamp when a closed timestamp is present.
- Email addresses must follow a valid email-like pattern when present.

## Consistency Rules

- Customer status values must map to `Active`, `Inactive`, or `Churned`.
- Payment status values must map to `Paid`, `Failed`, or `Pending`.
- Campaign channel values must map to `Paid Search`, `Paid Social`, `Organic`, `Email`, `Referral`, `Partner`, or `Direct`.
- Support ticket status values must map to `Closed`, `Resolved`, `Open`, or `In Progress`.
- Country, city, segment, industry, priority, and category values should use standardized reference values.

## Referential Integrity Rules

- `silver_orders.customer_id` exists in `silver_customers.customer_id`.
- `silver_orders.product_id` exists in `silver_products.product_id`.
- `silver_orders.campaign_id`, when not null, exists in `silver_campaigns.campaign_id`.
- `silver_ad_spend.campaign_id` exists in `silver_campaigns.campaign_id`.
- `silver_support_tickets.customer_id` exists in `silver_customers.customer_id`.

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
