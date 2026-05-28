# SQL

This folder will contain SQL scripts for curated models, validation checks, and reporting-friendly views.

## Planned Assets

- `bronze_validation_queries.sql`: validation queries for future Bronze Delta tables, including row counts, duplicate IDs, null keys, source update coverage, load dates, ingestion run IDs, and simple reconciliation.
- `silver_validation_queries.sql`: validation queries for future Silver Delta tables, including row counts, duplicate business keys, required fields, invalid values, referential integrity, quality status, and Bronze-to-Silver comparison.
- `gold_model_ddl.sql`: representative DDL for future Gold dimensions and facts.
- `gold_validation_queries.sql`: validation queries for future Gold tables, including key uniqueness, referential checks, row reconciliation, unknown key usage, date coverage, and KPI sanity checks.
- Future business metric SQL definitions.
- Future data quality queries.
- Future Power BI support views.

## Conventions

Scripts should be idempotent where practical and should clearly state the expected input layer and output object.
