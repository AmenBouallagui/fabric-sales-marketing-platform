# Architecture

## Overview

This is a Microsoft Fabric portfolio project with a local executable prototype. It turns synthetic customers, products, campaigns, orders, ad spend, and support tickets into governed analytics outputs.

The local prototype exists today and runs with pandas and parquet files so the medallion logic can be tested before Fabric implementation. The Microsoft Fabric implementation is planned for a future phase, including OneLake / Lakehouse Files, Delta tables, notebooks, Data Factory pipelines, and Warehouse or SQL endpoint access. Power BI and AI/Data Agent extensions are also planned future layers, not currently deployed assets.

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

## Planned Microsoft Fabric Flow

1. Source extracts are uploaded to OneLake / Lakehouse Files.
2. Fabric notebooks or Data Factory pipelines ingest files to Bronze Delta tables.
3. Silver transformations standardize, validate, and deduplicate records.
4. Gold tables or Warehouse objects expose dimensions and facts.
5. Observability tables track pipeline runs, quality results, freshness, and reconciliation.
6. Power BI consumes Gold and observability tables through a semantic model.
7. A future AI/Data Agent can be grounded on curated Gold data, metric definitions, and quality metadata.

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

Future Power BI semantic model, reports, and AI/Data Agent extension.

## Current Limitations

- Fabric items are not deployed yet.
- Power BI report is not created yet.
- AI/Data Agent extension is planned but not implemented.
- Local outputs are generated under ignored `data/` folders and are not committed.
