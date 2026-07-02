# Data Quality & Observability

This document defines the data-quality rule catalog and the observability model
that tracks pipeline health across Bronze, Silver, and Gold. Quality rules make
outputs trustworthy and explainable; observability makes runs reviewable.

A subset of these rules is **implemented today** as dbt tests
([`dbt/`](../dbt/)) and as the local pipeline's observability outputs
([`local_pipeline/`](../local_pipeline/)). The full Fabric observability tables,
alerting, and operations dashboard are planned.

## Check Categories

- **Completeness** — required fields, expected tables/files, non-empty datasets.
- **Validity** — data types, date ranges, non-negative numerics, accepted status values.
- **Consistency** — standardized categorical values, boolean handling, numeric precision.
- **Uniqueness** — one current record per business key (Silver); unique keys (Gold).
- **Referential integrity** — child records link to valid parents.
- **Freshness** — datasets load within the expected window.
- **Volume anomaly** — row counts stay within tolerance vs. prior runs.
- **Business-metric sanity** — revenue, spend, ROAS, margin, satisfaction stay in reasonable ranges.

## Rule Catalog

### Bronze (capture & lineage)
- Each expected source file produces a Bronze table that preserves source values.
- Ingestion metadata columns are populated (`ingestion_run_id`, file metadata, `load_date`, `ingested_at`, `source_updated_at`, `row_hash`).
- Required ID columns are present and non-null; row counts are non-zero.
- Duplicate source IDs and repeated loads are identifiable via metadata + `row_hash`.

### Silver — completeness
- Customers require `customer_id`, `customer_name`, `signup_date`.
- Products require `product_id`, `product_name`, `unit_price`, `unit_cost`.
- Campaigns require `campaign_id`, `channel`, `campaign_start_date`.
- Orders require `order_id`, `customer_id`, `product_id`, `order_date`, `total_amount`, `payment_status`.
- Ad spend requires `spend_id`, `campaign_id`, `spend_date`, `spend_amount`.
- Support tickets require `ticket_id`, `customer_id`, `created_at`, `status`.

### Silver — validity
- `unit_price > 0`; `unit_cost >= 0`; order `quantity > 0`.
- Order `unit_price`, `discount_amount`, `tax_amount`, `total_amount` all `>= 0`.
- Ad spend `spend_amount`, `impressions`, `clicks`, `conversions` all `>= 0`.
- Campaign start ≤ end (when end present); ticket created ≤ closed (when closed present).
- Satisfaction score within range; email matches an email-like pattern when present.

### Silver — consistency (accepted values)
- Customer status ∈ {Active, Inactive, Churned}.
- Payment status ∈ {Paid, Failed, Pending}.
- Campaign channel ∈ {Paid Search, Paid Social, Organic, Email, Referral, Partner, Direct}.
- Ticket status ∈ {Closed, Resolved, Open, In Progress}.

### Silver — deduplication
- One current record per business key; latest selected by `source_updated_at` →
  `ingested_at` → `row_hash`; marked `is_current_record = true` with `dq_status` /
  `dq_issue_reason` recorded.

### Referential integrity
- `orders.customer_id` → `customers`; `orders.product_id` → `products`;
  `orders.campaign_id` (when set) → `campaigns`.
- `ad_spend.campaign_id` → `campaigns`; `support_tickets.customer_id` → `customers`.

### Gold readiness & validation
- Only `dq_status = 'valid'` Silver records feed Gold.
- Dimension surrogate keys unique; fact keys unique at grain.
- Fact foreign keys resolve to a dimension row or a documented unknown member.
- Silver→Gold row counts reconcile; additive measures pass sanity checks; ratio
  measures (ROAS, gross margin %) avoid divide-by-zero.

## Observability Model

Four tables capture operational health (produced locally under
`data/observability/`; planned as Fabric Warehouse tables):

- **`pipeline_run_log`** — one row per run: `run_id`, `pipeline_name`, `layer_name`,
  `status`, start/end, `duration_seconds`, `rows_read`, `rows_written`, `error_message`, `triggered_by`.
- **`data_quality_results`** — one row per check: `check_id`, `run_id`, `layer_name`,
  `table_name`, `check_name`, `check_category`, `severity`, `status`, expected/actual,
  `failed_row_count`, `dq_issue_reason`.
- **`dataset_freshness`** — `dataset_name`, `layer_name`, `expected_frequency`,
  `last_successful_load`, `freshness_status`, `delay_minutes`.
- **`row_count_reconciliation`** — `source_layer`/`target_layer`, source/target tables,
  row counts, `row_count_difference`, `reconciliation_status`.

## Severity & Failure Handling

- **critical** blocks downstream (Gold) publication; **warning** is logged and shown;
  **info** is monitoring-only.
- Pipeline run status reflects the highest-severity outcome.
- Rejected records are captured/counted; failed checks include investigation context (no secrets).

## Alerting & Monitoring (planned)

Initial alerting via SQL queries or Power BI subscriptions; future Fabric adds
Data Activator / pipeline notifications. Alert on: failed critical checks, failed
runs, stale Gold datasets, large cross-layer row-count gaps, and repeated failures
for the same table/check.

A future **Operations / Data Health** Power BI page surfaces pipeline success rate,
failed checks by severity, freshness by dataset, and reconciliation — see
[`powerbi/report_design.md`](../powerbi/report_design.md).
