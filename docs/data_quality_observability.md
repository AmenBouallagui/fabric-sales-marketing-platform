# Data quality and observability

The dbt source/intermediate/mart tests and pandas validation functions are the executable rule catalog. Both paths reject invalid orders including missing dates, non-positive quantities, and negative monetary values. Rejected records remain in Silver/intermediate with a reason; only valid records feed Gold.

Both Gold implementations include unknown dimension members for unresolved foreign keys. Unresolved product costs stay null, and report margin/cost measures return blank when an eligible order lacks cost. pandas uses integer hash keys and `fact_` parquet names; dbt uses string hash keys and `fct_` relations. These are independent implementations and cannot be joined by surrogate keys.

## Implemented monitoring

The pandas pipeline writes three parquet tables under `data/observability/`:

- `pipeline_run_log`: completed layer execution summaries.
- `data_quality_results`: check outcomes and rejected-row counts.
- `row_count_reconciliation`: cross-layer row counts and differences.

Outputs overwrite the prior run. Logging occurs after transformations complete; exceptions are not yet persisted as failed-run records. A critical check label currently records severity but does not gate Gold publication. Foreign-key non-null checks do not alone prove full referential integrity; regression tests check dimension membership.

The Power BI Operations & Data Health page is built and imports three separate, committed telemetry seeds from Snowflake's observability schema. These fixtures are demonstrations, not current pipeline or CI results.

## Planned controls and limitations

Persistent run history, failed-run capture, publication gates, dataset freshness, prior-run volume anomalies, alerts, and cloud orchestration remain planned. Email validation, date-range consistency, and comprehensive domain rules are not all implemented. pandas deduplicates by source update, ingestion time, and row hash; dbt sorts by source update timestamp and a hash of all normalized source fields. Tied conflicting rows therefore resolve deterministically, though the two implementations can choose different winners.

See the [roadmap](project_roadmap.md) and [SQL reference designs](../sql/README.md).
