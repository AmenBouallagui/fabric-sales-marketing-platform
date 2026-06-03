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

## Expected Fabric Setup

- Fabric workspace created.
- Bronze Lakehouse created.
- Source CSV files uploaded to Lakehouse Files.
- Notebook attached to the Bronze Lakehouse.
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

## Execution Status

This notebook source has not been executed in Fabric unless a later implementation note or pull request explicitly documents that run.
