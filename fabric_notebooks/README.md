# Fabric Notebook Source

## Purpose

This folder contains version-controlled source files for future Microsoft Fabric notebooks. The files are intended to make notebook logic reviewable in Git before it is copied into, synchronized with, or implemented as Fabric notebook assets.

## Repo-Friendly Source Vs Fabric Notebooks

The files in this folder are plain `.py` source files. They are not `.ipynb` notebook exports and do not prove that code has already executed in Microsoft Fabric.

Actual Fabric notebooks should be created in a Fabric workspace and attached to the appropriate Lakehouse. The source files here provide the implementation starting point for those notebooks.

## Bronze Notebook Source

`nb_01_bronze_ingestion.py` is source code for a future Fabric notebook named `nb_01_bronze_ingestion`.

To use it:

1. Create the Fabric notebook described in [bronze_notebook_setup.md](../fabric_implementation/bronze_notebook_setup.md).
2. Attach the notebook to the Bronze Lakehouse.
3. Copy the contents of `nb_01_bronze_ingestion.py` into the Fabric notebook, or use it as the source when implementing the notebook through Fabric Git integration.
4. Set the notebook parameters for the target `load_date`, `source_base_path`, and `ingestion_run_id`.
5. Run the notebook after source files have been uploaded to Lakehouse Files.

## Silver Notebook Source

`nb_02_silver_transformations.py` is source code for a future Fabric notebook named `nb_02_silver_transformations`.

To use it:

1. Confirm Bronze Delta tables have been created.
2. Create a Fabric notebook named `nb_02_silver_transformations`.
3. Attach the notebook to the Lakehouse or workspace context that can read Bronze tables and write Silver tables.
4. Copy the contents of `nb_02_silver_transformations.py` into the Fabric notebook, or use it as the source when implementing the notebook through Fabric Git integration.
5. Set the notebook parameters for `silver_processed_at`, `write_mode`, and `fail_on_critical`.
6. Run the notebook after Bronze validation has passed.

## Expected Fabric Setup

- Fabric workspace created.
- Bronze and Silver Lakehouses created, or a single Lakehouse with clear layer conventions.
- Source CSV files uploaded to Lakehouse Files.
- Bronze Delta tables created before running the Silver notebook source.
- Notebook attached to the appropriate Lakehouse context.
- No secrets, workspace IDs, tenant IDs, or credentials stored in this repository.

## Source File Path Convention

```text
Files/source/{source_system}/{entity}/load_date=YYYY-MM-DD/file.csv
```

Example:

```text
Files/source/synthetic_crm/customers/load_date=2026-01-01/customers.csv
```

## Expected Bronze Outputs

- `bronze_customers_raw`
- `bronze_products_raw`
- `bronze_campaigns_raw`
- `bronze_orders_raw`
- `bronze_ad_spend_raw`
- `bronze_support_tickets_raw`

## Expected Silver Outputs

- `silver_customers`
- `silver_products`
- `silver_campaigns`
- `silver_orders`
- `silver_ad_spend`
- `silver_support_tickets`

## Execution Status

These notebook sources have not been executed in Fabric unless a later implementation note or pull request explicitly documents that run.
