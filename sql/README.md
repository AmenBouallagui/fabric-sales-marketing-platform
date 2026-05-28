# SQL

This folder will contain SQL scripts for curated models, validation checks, and reporting-friendly views.

## Planned Assets

- `bronze_validation_queries.sql`: validation queries for future Bronze Delta tables, including row counts, duplicate IDs, null keys, source update coverage, load dates, ingestion run IDs, and simple reconciliation.
- Gold table creation examples.
- Business metric SQL definitions.
- Data quality queries.
- Power BI support views.

## Conventions

Scripts should be idempotent where practical and should clearly state the expected input layer and output object.
