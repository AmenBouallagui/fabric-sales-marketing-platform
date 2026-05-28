# Data Quality Rules

## Overview

Data quality rules ensure that Bronze, Silver, and future Gold outputs are trustworthy, explainable, and ready for reporting. The current project focuses on customers, products, campaigns, orders, ad spend, and support tickets.

Bronze rules verify source capture and lineage. Silver rules verify cleaned, typed, deduplicated, and relationship-aware records. Gold readiness rules verify that curated tables can support Power BI reporting.

## Bronze Quality Rules

- Each expected source file should produce a corresponding Bronze table.
- Bronze rows should preserve source identifiers and source values.
- Bronze rows should include `ingestion_run_id`, `source_file_name`, `source_file_path`, `source_system`, `entity_name`, `load_date`, `ingested_at`, `source_updated_at`, and `row_hash`.
- Required source identifier columns should not be null.
- `source_updated_at` should be populated from the source `updated_at` column.
- Row counts should be greater than zero for expected source extracts.
- Duplicate source identifiers should be reported by entity, load date, and ingestion run.
- Repeated loads should be identifiable through file metadata, `ingestion_run_id`, and `row_hash`.

## Silver Completeness Rules

- Customers require `customer_id`, `customer_name`, and `signup_date`.
- Products require `product_id`, `product_name`, `unit_price`, and `unit_cost`.
- Campaigns require `campaign_id`, `channel`, and `campaign_start_date`.
- Orders require `order_id`, `customer_id`, `product_id`, `order_date`, `total_amount`, and `payment_status`.
- Ad spend records require `spend_id`, `campaign_id`, `spend_date`, and `spend_amount`.
- Support tickets require `ticket_id`, `customer_id`, `created_at`, and `status`.

## Silver Validity Rules

- Product `unit_price` must be greater than zero.
- Product `unit_cost` must be greater than or equal to zero.
- Order `quantity` must be greater than zero.
- Order `unit_price`, `discount_amount`, `tax_amount`, and `total_amount` must be greater than or equal to zero.
- Ad spend `spend_amount`, `impressions`, `clicks`, and `conversions` must be greater than or equal to zero.
- Campaign start date must not be later than campaign end date when an end date is present.
- Support ticket closed timestamp must not be earlier than created timestamp when a closed timestamp is present.
- Support ticket response and resolution minute values must be greater than or equal to zero when present.
- Satisfaction score should be within the accepted scoring range when present.
- Email values should follow a valid email-like pattern when present.

## Silver Consistency Rules

- Customer status values must map to `Active`, `Inactive`, or `Churned`.
- Payment status values must map to `Paid`, `Failed`, or `Pending`.
- Campaign channel values must map to `Paid Search`, `Paid Social`, `Organic`, `Email`, `Referral`, `Partner`, or `Direct`.
- Support ticket status values must map to `Closed`, `Resolved`, `Open`, or `In Progress`.
- Boolean-like fields such as `refund_flag` and `is_subscription` should be converted to consistent boolean values.
- Monetary fields should use consistent numeric precision.
- Date and timestamp fields should use consistent typed values.
- Country, city, segment, industry, priority, and category values should use standardized reference values.

## Referential Integrity Rules

- `silver_orders.customer_id` exists in `silver_customers.customer_id`.
- `silver_orders.product_id` exists in `silver_products.product_id`.
- `silver_orders.campaign_id`, when not null, exists in `silver_campaigns.campaign_id`.
- `silver_ad_spend.campaign_id` exists in `silver_campaigns.campaign_id`.
- `silver_support_tickets.customer_id` exists in `silver_customers.customer_id`.

## Silver Deduplication Rules

- Silver should contain one current record per source business key for the MVP.
- Customers deduplicate by `customer_id`.
- Products deduplicate by `product_id`.
- Campaigns deduplicate by `campaign_id`.
- Orders deduplicate by `order_id`.
- Ad spend deduplicates by `spend_id`.
- Support tickets deduplicate by `ticket_id`.
- Latest-record selection should use highest `source_updated_at`, then highest `ingested_at`, then a stable tie-breaker using `row_hash`.
- Current Silver rows should be marked with `is_current_record = true`.
- Silver rows should include `dq_status` and `dq_issue_reason` to make quality outcomes visible before Gold modeling.

## Gold Readiness Rules

- Silver records feeding Gold should have `dq_status = 'valid'` unless a documented warning rule allows inclusion.
- Gold dimensions should have stable keys and descriptive attributes.
- Gold facts should have clearly defined grains and additive measures.
- Order, spend, and ticket date fields should be compatible with `dim_date`.
- Measures used in Power BI should have documented definitions and expected filters.
- Records rejected in Silver should not feed Gold tables without explicit review.

## Gold Validation Rules

- Gold dimension surrogate keys should be unique.
- Gold fact business keys should be unique at the documented grain.
- Gold fact foreign keys should resolve to valid dimension rows or documented unknown members.
- Unknown dimension key usage should be monitored and explainable.
- Gold fact row counts should reconcile to valid/current Silver records.
- Additive measures such as revenue, net revenue, gross margin, ad spend, impressions, clicks, conversions, response minutes, and resolution minutes should pass sanity checks.
- KPI calculations such as ROAS and gross margin percentage should avoid divide-by-zero errors.

## Monitoring Approach

- Quality checks should produce pass/fail counts by entity and rule.
- Validation outputs should include failed row counts and sample failed keys where practical.
- Runs should track row counts from Bronze to Silver and, later, from Silver to Gold.
- `dq_status` distribution should be monitored by Silver table.
- Referential integrity failures should be reported before Gold publication.
- Critical failures should block Gold publication once orchestration is introduced.

## Observability Result Tables

The rule definitions in this document should feed future observability tables:

- `data_quality_results` captures check outcomes, severity, status, expected values, actual values, failed row counts, and issue reasons.
- `pipeline_run_log` captures run status, duration, row counts, and errors.
- `dataset_freshness` captures freshness status by dataset and layer.
- `row_count_reconciliation` captures row movement between Bronze, Silver, and Gold.

These tables will support future operational reporting and make quality outcomes visible before downstream publication.
