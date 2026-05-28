# Silver Transformation Design

## Purpose

The Silver layer converts raw Bronze records into clean, standardized, typed, deduplicated entities that are ready for Gold dimensional modeling. Silver is where source-preserving records become trusted analytical entities while retaining enough lineage to trace every row back to Bronze.

This document describes the intended Microsoft Fabric implementation pattern. It is a design artifact, not a claim that the Silver notebook or pipeline has already been deployed.

## Inputs And Outputs

Silver transformations read from the expected Bronze Delta tables and write one cleaned table per business entity.

| Bronze input | Silver output | Business key | Purpose |
| --- | --- | --- | --- |
| `bronze_customers_raw` | `silver_customers` | `customer_id` | Clean customer/account profile attributes for downstream dimensions and customer analysis. |
| `bronze_products_raw` | `silver_products` | `product_id` | Standardize product catalog values, prices, costs, categories, and plan tiers. |
| `bronze_campaigns_raw` | `silver_campaigns` | `campaign_id` | Standardize marketing campaign metadata and active date ranges. |
| `bronze_orders_raw` | `silver_orders` | `order_id` | Clean sales order transactions and prepare revenue measures for Gold facts. |
| `bronze_ad_spend_raw` | `silver_ad_spend` | `spend_id` | Clean marketing spend and engagement measures linked to campaigns. |
| `bronze_support_tickets_raw` | `silver_support_tickets` | `ticket_id` | Clean customer support interactions for service quality and customer health analysis. |

## Silver Table Naming Convention

Silver table names should use business entity names without the `_raw` suffix:

- `silver_customers`
- `silver_products`
- `silver_campaigns`
- `silver_orders`
- `silver_ad_spend`
- `silver_support_tickets`

## Standardization Rules

Silver transformations should apply consistent, explainable cleanup rules across all entities:

- Trim leading and trailing whitespace from string columns.
- Normalize categorical values to approved casing, such as `Paid`, `Failed`, `Pending`, `Active`, `Inactive`, and `Churned`.
- Parse dates and timestamps into typed date or timestamp columns.
- Convert boolean-like values consistently, such as `refund_flag` and `is_subscription`.
- Convert monetary and numeric fields to decimal or numeric types.
- Preserve source business IDs from Bronze.
- Add `silver_processed_at` to record when Silver transformation logic processed the row.
- Add `is_current_record` where useful to identify the current deduplicated record.
- Add `dq_status` and `dq_issue_reason` for record-level quality status.

## Type Casting Rules

Recommended type handling:

| Field pattern | Target type |
| --- | --- |
| Business IDs | String |
| Names, categories, statuses, channels | String |
| Dates such as `signup_date`, `valid_from`, `campaign_start_date`, `order_date`, `spend_date` | Date |
| Timestamps such as `created_at`, `closed_at`, `source_updated_at`, `ingested_at` | Timestamp |
| Monetary fields such as `unit_price`, `unit_cost`, `discount_amount`, `tax_amount`, `total_amount`, `spend_amount` | Decimal or numeric with two decimal places |
| Counts such as `quantity`, `impressions`, `clicks`, `conversions`, `first_response_minutes`, `resolution_minutes` | Integer |
| Flags such as `refund_flag` and `is_subscription` | Boolean |

## Deduplication Strategy

For the MVP, Silver should contain one current record per source business key. Deduplication happens within each Bronze table before writing the current Silver entity.

Deduplicate by the entity business key:

- Customers: `customer_id`
- Products: `product_id`
- Campaigns: `campaign_id`
- Orders: `order_id`
- Ad spend: `spend_id`
- Support tickets: `ticket_id`

## Latest-Record Logic

When more than one Bronze record exists for the same business key, keep the latest record using this ordering:

1. Highest `source_updated_at`.
2. Then highest `ingested_at`.
3. Then stable tie-breaker using `row_hash`.

The selected row should be marked with `is_current_record = true`. Non-current versions can remain in Bronze for auditability. The MVP Silver design writes only current records to the main Silver tables.

## Business Validation Rules

Silver validation should classify records as valid, warning, or rejected using `dq_status` and `dq_issue_reason`.

Suggested statuses:

- `valid`: record passes required Silver checks.
- `warning`: record is usable but has a non-blocking issue.
- `rejected`: record fails a critical business or referential check and should not feed Gold.

Example business rules:

- Customers require non-null `customer_id`, `customer_name`, and `signup_date`.
- Products require non-null `product_id`, positive `unit_price`, and non-negative `unit_cost`.
- Campaigns require non-null `campaign_id`, `channel`, and `campaign_start_date`.
- Orders require non-null `order_id`, valid `customer_id`, valid `product_id`, non-negative `total_amount`, and valid `payment_status`.
- Ad spend requires non-null `spend_id`, valid `campaign_id`, non-negative `spend_amount`, and non-negative `impressions`, `clicks`, and `conversions`.
- Support tickets require non-null `ticket_id`, valid `customer_id`, valid `created_at`, and valid `status`.

## Referential Integrity Checks

Silver should validate key relationships after each entity is standardized and deduplicated:

- `silver_orders.customer_id` exists in `silver_customers.customer_id`.
- `silver_orders.product_id` exists in `silver_products.product_id`.
- `silver_orders.campaign_id`, when not null, exists in `silver_campaigns.campaign_id`.
- `silver_ad_spend.campaign_id` exists in `silver_campaigns.campaign_id`.
- `silver_support_tickets.customer_id` exists in `silver_customers.customer_id`.

Records that fail referential integrity should be marked with `dq_status = 'rejected'` or routed to a rejected-records table in a later implementation.

## Error Handling Strategy

Silver transformation should separate structural failures from record-level quality failures:

- Missing Bronze table: fail the run.
- Missing required Bronze column: fail the entity transformation before writing Silver.
- Invalid data type conversion: set the converted field to null, mark record-level `dq_status`, and capture the reason.
- Critical validation failure: mark the record as rejected or write it to a future rejected-records table.
- Referential integrity failure: mark the dependent record as rejected and log the failed relationship.

## Idempotency Strategy

The MVP Silver process should be rerunnable for the same Bronze state.

Recommended approach:

- Build Silver outputs from deterministic Bronze inputs and deterministic ordering.
- Use business-key deduplication with `source_updated_at`, `ingested_at`, and `row_hash`.
- Write current Silver tables with overwrite or replace-table semantics during development.
- Preserve Bronze append history for replay and auditability.
- Add `silver_processed_at` for operational visibility while avoiding it as a deduplication key.

## Future Fabric Implementation Notes

The future Microsoft Fabric implementation can use:

- Fabric notebooks with PySpark for transformations and window-based deduplication.
- Delta tables for Silver outputs.
- Data Factory pipelines to orchestrate Bronze-to-Silver runs after Bronze ingestion.
- SQL endpoint validation queries for reviewer-friendly checks.
- Optional rejected-records Delta tables for failed records.
- Optional load audit tables for run metrics, row counts, and quality status summaries.

The first implementation should favor readable transformation logic and transparent quality outcomes.

## Success Criteria

The Silver design is successful when:

- All six Bronze tables have documented Silver targets.
- Silver rules standardize strings, categories, dates, booleans, and numeric fields.
- Each Silver table has one current record per business key for the MVP.
- Deduplication logic is deterministic and based on `source_updated_at`, `ingested_at`, and `row_hash`.
- Record-level `dq_status` and `dq_issue_reason` are available for quality review.
- Referential integrity checks are documented and testable.
- A reviewer can understand how Bronze data becomes cleaned Silver data ready for Gold modeling.
