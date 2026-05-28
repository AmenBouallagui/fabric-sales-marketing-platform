# Data Quality And Observability Design

## Purpose

This design defines how the platform will track data quality checks, pipeline run outcomes, dataset freshness, row count reconciliation, and operational health across Bronze, Silver, and Gold layers.

It is a design and implementation plan for a future Microsoft Fabric build. It does not claim that the observability tables, notebooks, alerts, or Power BI dashboard already run in Fabric.

## Scope

The design covers the current project domains:

- Customers
- Products
- Campaigns
- Orders
- Ad spend
- Support tickets

It applies to future Bronze raw tables, Silver cleaned tables, Gold dimensions, Gold facts, Data Factory orchestration, Fabric notebooks, SQL validation queries, and Power BI operations reporting.

## Why Observability Matters

Data quality and observability make the platform easier to trust, operate, and review. A production-style platform should show whether data arrived, whether checks passed, how many rows moved between layers, how fresh each dataset is, and whether failures should block downstream publication.

Observability also creates a reusable audit trail for troubleshooting and portfolio demonstration.

## Quality Check Categories

- Completeness: required fields, expected tables, expected files, and non-empty datasets.
- Validity: data types, date ranges, non-negative numeric values, accepted status values, and valid metrics.
- Consistency: standardized categorical values, boolean handling, numeric precision, and date formatting.
- Uniqueness: one current record per business key in Silver and unique keys in Gold dimensions and facts.
- Referential integrity: child records link to valid parent entities.
- Freshness: datasets are loaded within the expected time window.
- Volume anomaly checks: row counts stay within expected tolerance compared with prior successful runs.
- Business metric sanity checks: measures such as revenue, ad spend, ROAS, gross margin, and satisfaction score remain within reasonable ranges.

## Observability Table Design

The observability model should include four core tables:

### `pipeline_run_log`

Tracks one orchestration or notebook execution.

- `run_id`
- `pipeline_name`
- `layer_name`
- `status`
- `start_time`
- `end_time`
- `duration_seconds`
- `rows_read`
- `rows_written`
- `error_message`
- `triggered_by`
- `created_at`

### `data_quality_results`

Tracks one quality check result.

- `check_id`
- `run_id`
- `layer_name`
- `table_name`
- `check_name`
- `check_category`
- `severity`
- `status`
- `expected_value`
- `actual_value`
- `failed_row_count`
- `dq_issue_reason`
- `checked_at`

### `dataset_freshness`

Tracks freshness status by dataset and layer.

- `dataset_name`
- `layer_name`
- `source_system`
- `expected_frequency`
- `last_successful_load`
- `freshness_status`
- `delay_minutes`
- `checked_at`

### `row_count_reconciliation`

Tracks row count movement between layers.

- `reconciliation_id`
- `run_id`
- `source_layer`
- `target_layer`
- `source_table`
- `target_table`
- `source_row_count`
- `target_row_count`
- `row_count_difference`
- `reconciliation_status`
- `checked_at`

## Pipeline Run Logging Strategy

Each orchestrated run should create one row in `pipeline_run_log` at start and update it at completion.

Recommended statuses:

- `running`
- `succeeded`
- `failed`
- `completed_with_warnings`

The run log should capture row counts when practical and should include concise error messages for failed runs. Detailed logs can remain in Fabric execution history.

## Dataset Freshness Strategy

Freshness checks should compare the most recent successful load timestamp to the expected frequency for each dataset.

Example expectations:

- Daily source extracts should be fresh within 24 hours plus a tolerance window.
- Silver and Gold tables should be fresh after their upstream layer completes.
- Freshness status values should include `fresh`, `delayed`, `stale`, and `unknown`.

## Validation Result Strategy

Quality checks should write one result row per check to `data_quality_results`.

Each result should include:

- Check category.
- Severity.
- Pass, fail, or warning status.
- Expected and actual values where useful.
- Failed row count where practical.
- Human-readable issue reason.
- Run identifier and check timestamp.

This pattern allows Power BI to show quality trends over time by table, layer, check, and severity.

## Severity Levels

- `critical`: blocks downstream publication.
- `warning`: visible issue but pipeline can continue.
- `info`: monitoring-only signal.

Severity should be configured per check so the same check pattern can have different behavior across layers.

## Failure Handling Strategy

- Critical failures block Gold publication.
- Warning failures are logged and shown in the dashboard.
- Info checks are used for trend monitoring.
- Rejected records should be captured or counted where practical.
- Pipeline run status should reflect the highest severity outcome for the run.
- Failed checks should include enough context to support investigation without exposing secrets.

## Alerting Strategy

Initial alerting can be based on SQL queries or Power BI subscriptions. Future Fabric implementation can add pipeline notifications or Data Activator rules.

Recommended alert conditions:

- Failed critical checks.
- Failed pipeline runs.
- Stale Gold datasets.
- Large row count differences between layers.
- Repeated failures for the same table and check.

## Power BI Monitoring Dashboard Design

A future Operations / Data Health dashboard should include:

- Pipeline success rate.
- Latest pipeline runs.
- Failed checks by severity.
- Freshness status by dataset.
- Failed critical checks.
- Warning checks.
- Row count reconciliation.
- Latest successful load by layer and dataset.
- Tables with repeated failures.
- Quality check pass rate by layer and table.
- Average pipeline duration by pipeline.

## Future Fabric Implementation Notes

The future implementation can use:

- Fabric notebooks to run quality checks and write observability rows.
- Data Factory pipelines to pass `run_id`, layer, and pipeline parameters.
- Fabric Warehouse or SQL endpoint tables for observability storage.
- Power BI for operational monitoring.
- Optional alerting with Data Activator or pipeline notifications.

The first implementation should prioritize reliable logging, understandable check definitions, and clear failure behavior.

## Success Criteria

The design is successful when:

- Quality check categories are documented and mapped to observability results.
- Pipeline runs can be reviewed by status, duration, row counts, and errors.
- Dataset freshness is visible by layer and dataset.
- Row count reconciliation is recorded between layers.
- Critical failures can block Gold publication.
- A future Power BI dashboard can show platform health without reading raw execution logs.
