# Sales and marketing business case

## Business question

This synthetic reference project brings sales, campaign spend, customer profiles, product costs, and support tickets into one analytical model. It supports questions about paid sales trends, campaign efficiency, product margin, customer composition, and support quality. No client data or measured client business outcome is claimed.

## Design decisions

- A star schema separates orders, daily ad spend, and support tickets at their own grains, with shared dimensions for filtering.
- dbt and DuckDB make the warehouse reproducible without a cloud subscription. The independent pandas pipeline demonstrates ingestion metadata, validation, and parquet outputs using separately generated data.
- Sales KPIs include only Paid, non-refunded orders. Campaign ROAS aggregates each fact before joining campaigns, preventing inflated totals from many-to-many fact joins.
- Unknown dimension members retain unresolved source records. Missing costs stay null; report cost and margin definitions avoid presenting incomplete totals as complete.
- Source flags, dbt tests, Python regressions, and row-count reconciliation make data defects visible. Monitoring fixtures are separated from current execution evidence.

## What the demo establishes

The [verification record](local_verification.md) reports executed tests and synthetic warehouse totals. It demonstrates reproducible analytics engineering and metric definitions. Synthetic campaign rankings are examples, not evidence of real marketing effectiveness or causal effects.

## What remains to validate

Power BI source is included for review, including seven pages and 28 DAX measures. Current rendering, DAX results, Snowflake refresh, security, and cloud orchestration remain unverified. Earlier media is historical. The [roadmap](project_roadmap.md) tracks operational improvements.
