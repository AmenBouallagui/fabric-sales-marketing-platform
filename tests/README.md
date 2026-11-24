# Tests

Run `python -m pytest` from the repository root after the README's dbt seed/build sequence.

- Local integration: generates synthetic CSVs, runs medallion transformations, checks parquet outputs and dimension membership, and verifies an orphan order resolves to unknown members without invented cost.
- Quality rules: rejects zero/negative quantities and missing order dates.
- Metrics: checks campaign ROAS without fact fanout, payment/refund exclusions, duplicate campaign names, unknown campaigns, and zero spend.
- Warehouse regressions: inserts invalid orders and tied updates inside a rolled-back DuckDB transaction, checking rejection and deterministic deduplication. These tests skip if the warehouse has not been built. Set `DBT_DUCKDB_PATH` to test another local database.

CI builds the warehouse first and exercises all five tests. dbt build also runs 39 data tests. Power BI Desktop/DAX and Snowflake refresh need separate validation in their target environments.
