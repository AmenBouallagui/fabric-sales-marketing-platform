# Bronze Notebook Setup

## Purpose

This guide prepares the first Fabric notebook implementation for Bronze ingestion. The notebook should read source CSV files from Lakehouse Files, add ingestion metadata, validate required columns, and write Bronze Delta tables.

## Notebook Item

Create a Fabric notebook named:

`nb_01_bronze_ingestion`

Attach the notebook to the Bronze Lakehouse:

`lh_sales_marketing_bronze`

Use the repo-friendly notebook source as the starting implementation:

[fabric_notebooks/nb_01_bronze_ingestion.py](../fabric_notebooks/nb_01_bronze_ingestion.py)

The source file can be copied into the Fabric notebook or used as the source of truth when implementing the notebook through Fabric Git integration. It is not an `.ipynb` artifact and does not indicate that the notebook has already run in Fabric.

## Suggested Parameters

- `source_base_path`: base Files path for landed source extracts.
- `load_date`: logical load date folder to ingest.
- `ingestion_run_id`: unique identifier for the ingestion run.
- `ingested_at`: timestamp captured at the start of the run.
- `fail_on_missing_file`: boolean flag controlling whether missing expected files fail the run.

## Expected Bronze Tables

- `bronze_customers_raw`
- `bronze_products_raw`
- `bronze_campaigns_raw`
- `bronze_orders_raw`
- `bronze_ad_spend_raw`
- `bronze_support_tickets_raw`

## Required Metadata Columns

Every Bronze table should include:

- `ingestion_run_id`
- `source_file_name`
- `source_file_path`
- `source_system`
- `entity_name`
- `load_date`
- `ingested_at`
- `source_updated_at`
- `row_hash`

## First Test Run Checklist

- Source files are present under the expected Lakehouse Files paths.
- Notebook parameters point to the correct `load_date`.
- Required source columns are validated before writing tables.
- Bronze tables are created or appended successfully.
- Row counts match the uploaded source files.
- `source_updated_at` is populated from source `updated_at`.
- `row_hash` is stable for unchanged source records.
- The notebook records enough run details to support future observability logging.

## Troubleshooting Notes

- If a file is missing, confirm the source system and entity folder names match the upload guide.
- If a table is empty, check whether the notebook is reading the intended load date folder.
- If schema validation fails, compare the generated source CSV headers with the Bronze design document.
- If duplicate loads occur, use `ingestion_run_id`, `source_file_path`, `load_date`, and `row_hash` to identify repeated records.
- If SQL validation cannot find a table, confirm the table was written to the expected Lakehouse and is visible in the SQL endpoint.
