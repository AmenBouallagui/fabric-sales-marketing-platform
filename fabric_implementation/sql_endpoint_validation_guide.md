# SQL Endpoint Validation Guide

## Purpose

This guide describes how to validate Bronze tables in Microsoft Fabric after the future Bronze ingestion notebook has created them.

This is future Fabric work. These SQL validations are not run by the local pandas/parquet prototype.

## Validation Entry Point

Use the Fabric SQL endpoint or Warehouse-style query experience after Bronze tables exist.

Reference the existing validation query library:

[sql/bronze_validation_queries.sql](../sql/bronze_validation_queries.sql)

## Suggested Validation Sequence

1. Row counts by Bronze table.
2. Null primary or business keys.
3. Duplicate source IDs.
4. `source_updated_at` coverage.
5. Records by `load_date`.
6. Records by `ingestion_run_id`.
7. Simple reconciliation between expected entities and Bronze tables.

## Review Checklist

- Each expected Bronze table is visible in the SQL endpoint.
- Row counts are greater than zero after the first test load.
- Required source IDs are not null.
- Duplicate source IDs are reviewed before Silver deduplication.
- `source_updated_at` is populated for incremental-load readiness.
- Records are attributable to the expected `load_date` and `ingestion_run_id`.
- Validation results are documented for the first Fabric implementation milestone.

## Future Extension

Later phases can write validation results into the observability model described in `docs/data_quality_observability.md`, including check status, severity, failed row counts, and run identifiers.
