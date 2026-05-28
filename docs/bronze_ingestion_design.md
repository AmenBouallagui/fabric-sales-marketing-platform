# Bronze Ingestion Design

## Purpose

The Bronze layer is the first governed landing point for source-system data in the AI-Ready Sales & Marketing Data Platform. Its purpose is to preserve source records as closely as practical while adding ingestion metadata that supports lineage, auditability, replay, validation, and future incremental loading.

This document describes the intended Microsoft Fabric implementation pattern. It is a design artifact, not a claim that the Fabric notebook or pipeline has already been deployed.

## Source Files And Expected Schemas

Synthetic source CSV files are generated locally under `data/source/` and are intended to be uploaded to Microsoft Fabric OneLake or Lakehouse Files.

| Entity | Source file | Primary key | Expected source columns |
| --- | --- | --- | --- |
| Customers | `customers.csv` | `customer_id` | `customer_id`, `account_id`, `customer_name`, `email`, `country`, `city`, `signup_date`, `acquisition_channel`, `customer_segment`, `company_size`, `industry`, `status`, `updated_at` |
| Products | `products.csv` | `product_id` | `product_id`, `product_name`, `category`, `plan_tier`, `unit_price`, `unit_cost`, `is_subscription`, `valid_from`, `valid_to`, `updated_at` |
| Campaigns | `campaigns.csv` | `campaign_id` | `campaign_id`, `campaign_name`, `channel`, `campaign_start_date`, `campaign_end_date`, `target_segment`, `objective`, `updated_at` |
| Orders | `orders.csv` | `order_id` | `order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `unit_price`, `discount_amount`, `tax_amount`, `total_amount`, `payment_status`, `refund_flag`, `campaign_id`, `updated_at` |
| Ad spend | `ad_spend.csv` | `spend_id` | `spend_id`, `campaign_id`, `spend_date`, `channel`, `impressions`, `clicks`, `conversions`, `spend_amount`, `updated_at` |
| Support tickets | `support_tickets.csv` | `ticket_id` | `ticket_id`, `customer_id`, `created_at`, `closed_at`, `priority`, `category`, `status`, `satisfaction_score`, `first_response_minutes`, `resolution_minutes`, `updated_at` |

## Landing Path Convention

Source files should be landed in Lakehouse Files using a partitioned folder convention:

```text
Files/source/{source_system}/{entity}/load_date=YYYY-MM-DD/file.csv
```

Example:

```text
Files/source/synthetic_crm/customers/load_date=2026-01-01/customers.csv
```

Recommended source system values:

- `synthetic_crm` for customers, orders, products, and support tickets.
- `synthetic_marketing` for campaigns and ad spend.

The exact source system names can be refined later, but they should remain stable once downstream processing depends on them.

## Bronze Table Naming Convention

Bronze Delta tables should use the `_raw` suffix to signal that records are preserved with minimal business transformation:

- `bronze_customers_raw`
- `bronze_products_raw`
- `bronze_campaigns_raw`
- `bronze_orders_raw`
- `bronze_ad_spend_raw`
- `bronze_support_tickets_raw`

## Ingestion Metadata Columns

Every Bronze table should include these metadata columns in addition to the source columns:

| Column | Purpose |
| --- | --- |
| `ingestion_run_id` | Unique identifier for a notebook or pipeline execution. |
| `source_file_name` | File name that produced the record. |
| `source_file_path` | Full Lakehouse Files path used during ingestion. |
| `source_system` | Logical system or extract family, such as `synthetic_crm`. |
| `entity_name` | Entity being ingested, such as `customers`. |
| `load_date` | Partition date from the landing path. |
| `ingested_at` | Timestamp when the Bronze row was written. |
| `source_updated_at` | Parsed value from the source `updated_at` column. |
| `row_hash` | Hash across source business columns used for duplicate detection and replay checks. |

## Full-Load Vs Incremental-Load Assumptions

The MVP source CSVs are treated as extract files that can be loaded fully during early development. Each file contains an `updated_at` field that supports future incremental patterns.

Initial assumptions:

- Bronze preserves source records plus ingestion metadata.
- Full loads can append records for auditability during early implementation.
- Future incremental logic can use `updated_at`, file `load_date`, or both.
- Repeated loads should be identifiable through `ingestion_run_id`, file metadata, and `row_hash`.
- Silver processing will decide whether to deduplicate, version, or apply latest-record logic.

## Error Handling Strategy

Bronze ingestion should fail fast for structural problems and isolate row-level problems when practical.

Recommended behavior:

- Missing required files: fail the ingestion run and log the missing entity.
- Missing required columns: fail the entity load before writing to Bronze.
- Parse errors: capture malformed rows in a rejected-records location when Fabric implementation begins.
- Unexpected extra columns: allow ingestion, but log the schema drift for review.
- Duplicate files for the same entity and load date: allow only when `ingestion_run_id` makes the replay intentional and traceable.

## Data Validation Strategy

Bronze validation should focus on source completeness, traceability, and load integrity rather than business-level cleansing.

Minimum checks:

- Required ID columns are present.
- Required ID columns are not null.
- `updated_at` exists and can be parsed as `source_updated_at`.
- Row counts are greater than zero for expected entities.
- Duplicate source IDs are reported by entity and load.
- Records can be grouped by `load_date` and `ingestion_run_id`.
- Source file metadata columns are populated.

Business conformance checks, such as referential integrity between customers and orders, should be introduced in Silver or in validation notebooks that compare Bronze entities after ingestion.

## Idempotency Strategy

Bronze should be append-friendly, but repeated ingestion should be easy to identify and manage.

Recommended approach:

- Generate one `ingestion_run_id` per run.
- Include `source_file_path`, `source_file_name`, `load_date`, and `row_hash` on every row.
- Use `row_hash` to identify identical source rows across repeated loads.
- Optionally enforce a control table later with one row per entity, file path, row count, and run status.
- Avoid destructive overwrite of Bronze tables unless a development reset is explicitly intended.

## Future Fabric Implementation Notes

The future Microsoft Fabric implementation can use:

- Lakehouse Files for landed CSV extracts.
- Fabric notebooks with PySpark for schema validation, metadata enrichment, and Delta writes.
- Delta tables for Bronze storage.
- Data Factory pipelines for orchestration, parameter passing, and scheduling.
- A load audit table for operational monitoring.
- SQL endpoint validation queries for reviewer-friendly load checks.

The first implementation should prioritize clarity and repeatability over complex orchestration.

## Success Criteria

The Bronze ingestion design is successful when:

- All six expected source files have a documented landing path and Bronze table target.
- Each Bronze table preserves source columns and adds required ingestion metadata.
- Required source schemas are documented.
- Validation queries can confirm row counts, duplicates, null keys, load dates, run IDs, and `source_updated_at` coverage.
- Repeated loads can be identified through metadata without relying on manual inspection.
- A reviewer can understand how local synthetic CSVs become Fabric Bronze Delta tables.
