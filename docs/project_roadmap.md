# Project roadmap

## Implemented

- Synthetic source generator and pandas Bronze/Silver/Gold pipeline.
- dbt warehouse with a credential-free DuckDB target and CI validation.
- Star schema, unknown members, source quality flags, and business-rule tests.
- One Power BI project with seven pages, Snowflake Import partitions, and parameterized connection settings.
- Local quality/reconciliation outputs and separate seeded report operations data.

## Next engineering milestones

1. Persist failed runs and telemetry history; implement publication gates for critical failures.
2. Add dataset freshness and volume anomaly checks with alerting.
3. Add incremental loading and explicit change-history retention.
4. Validate a deployed Snowflake refresh and DAX results against the SQL metric queries.
5. Implement and validate report access controls and row-level security.
6. Automate cloud orchestration and deployment; benchmark larger datasets.

AI features remain a future extension. No AI service or Fabric notebook is implemented in this repository.
