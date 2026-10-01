# Architecture

## Overview

This is an analytics engineering portfolio project. It turns synthetic customers, products, campaigns, orders, ad spend, and support tickets into governed analytics outputs, implemented two ways: a local pandas prototype and a dbt warehouse (DuckDB locally, Snowflake via dbt Cloud), with the Snowflake warehouse feeding a Power BI semantic model in Import mode.

## Architecture Diagram

See the Mermaid architecture diagram in [architecture_diagram.md](../assets/architecture_diagram.md).

## Current Local Prototype Flow

1. Synthetic source CSVs are generated locally.
2. The local medallion pipeline reads source CSVs.
3. Bronze parquet outputs preserve source records and ingestion metadata.
4. Silver parquet outputs clean, type-cast, deduplicate, and validate records.
5. Gold parquet outputs build dimensions, facts, and KPI-ready fields.
6. Observability outputs capture run logs, quality results, and row count reconciliation.
7. GitHub Actions validates generation, local pipeline execution, and tests.

## dbt Warehouse Flow

1. Committed CSV fixtures are loaded into raw tables with `dbt seed` before `dbt build`.
2. Staging models type-cast and normalize.
3. Intermediate models dedupe to latest record per business key and flag data quality.
4. Marts build conformed dimensions and fact tables with derived measures.
5. Power BI consumes Gold via a semantic model (PBIP / TMDL, defined as code), connected to Snowflake in Import mode.

## Layer Responsibilities

### Source

Synthetic CSV extracts for customers, products, campaigns, orders, ad spend, and support tickets.

### Bronze

Raw records plus ingestion metadata.

### Silver

Cleaned, typed, deduplicated, validated current records.

### Gold

Business-ready dimensions, facts, KPI-ready fields, and Power BI-friendly structures.

### Observability

Pipeline run logs, data quality results, dataset freshness, and row count reconciliation.

### Consumption

Power BI semantic model (PBIP / TMDL, defined as code), connected to Snowflake in Import mode — 7 report pages built.

## Current Limitations

- Local outputs are generated under ignored `data/` folders and are not committed.
- The dbt project's cloud target (Snowflake) requires credentials; the DuckDB target runs with none.
- The pandas pipeline consumes generated CSVs; dbt consumes committed fixtures. These are separate datasets.
- Power BI reads the Snowflake warehouse; local parquet outputs are not its current data source.
- Power BI operations tables use seeded demonstration telemetry.
