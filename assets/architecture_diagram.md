# Architecture diagram

Two independently runnable implementations use separate synthetic inputs. Only the Snowflake deployment feeds the Power BI report.

```mermaid
flowchart LR
    A[Generated CSVs] --> B[pandas Bronze]
    B --> C[pandas Silver]
    C --> D[Gold parquet]
    C --> E[Local run telemetry]
    D --> E
    F[Committed CSV fixtures] --> G[dbt seed: raw]
    G --> H[staging]
    H --> I[intermediate: validation]
    I --> J[marts: star schema]
    J --> K[DuckDB: local and CI]
    J --> L[Snowflake: configured cloud deployment]
    M[Committed telemetry fixtures] --> N[dbt seed: observability]
    N --> L
    L --> O[Power BI Import: 11 data tables + measure table]
    O --> P[7 report pages]
```

Generated parquet and local run telemetry do not automatically update Snowflake or the report. Report operations data is seeded demonstration telemetry. See [architecture and limitations](../docs/architecture.md).
