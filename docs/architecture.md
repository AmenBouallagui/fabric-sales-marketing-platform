# Architecture

## Overview

This is a Microsoft Fabric portfolio project with a local executable prototype. It turns synthetic customers, products, campaigns, orders, ad spend, and support tickets into governed analytics outputs.

The local prototype exists today and runs with pandas and parquet files so the medallion logic can be tested before Fabric implementation. The Microsoft Fabric implementation is planned for a future phase, including OneLake / Lakehouse Files, Delta tables, notebooks, Data Factory pipelines, and Warehouse or SQL endpoint access. Power BI execution is the next planned layer; the semantic model is already defined as code.

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
6. Power BI consumes Gold and observability tables through a semantic model (PBIP / TMDL, defined as code).

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

Power BI semantic model (PBIP / TMDL, defined as code). Report visuals to be built in Power BI Desktop.

## Current Limitations

- Fabric items are not deployed yet (setup guides and PySpark notebook source are ready).
- Power BI report visuals not built yet (semantic model and DAX measures are defined).
- Local outputs are generated under ignored `data/` folders and are not committed.
