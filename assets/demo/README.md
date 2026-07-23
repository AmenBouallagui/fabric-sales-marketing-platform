# Demo Assets

## Purpose

This folder is reserved for future portfolio demo screenshots and presentation assets. It documents what should be captured once the local prototype or Power BI report views are ready to show visually.

## Current Demo Assets

- [Architecture overview](architecture_overview.md): Mermaid diagram showing the local prototype and dbt warehouse (DuckDB/Snowflake) feeding the live-connected Power BI report.
- [Gold model](gold_model.md): Mermaid diagram showing Gold dimensions, facts, and reporting relationships.

## Planned Screenshots

- README and architecture overview.
- Local data generation command output.
- Local medallion pipeline command output.
- Local output folder structure for `data/source/`, `data/bronze/`, `data/silver/`, `data/gold/`, and `data/observability/`.
- Pytest or CI success output.
- Power BI semantic model relationships.
- Power BI report pages.

## Current Status

No screenshots, images, or generated data assets are included yet. Demo assets should be added once they represent real local output or the live Power BI report.

## Guidelines

- Do not include secrets, tenant IDs, workspace IDs, connection strings, or credentials.
- Do not commit generated data extracts.
- Use screenshots only for portfolio-safe synthetic data.
