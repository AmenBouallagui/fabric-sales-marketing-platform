# Fabric Implementation Guides

## Purpose

This folder contains practical setup guides for moving the AI-Ready Sales & Marketing Data Platform from the local executable prototype toward a real Microsoft Fabric workspace.

The repository already includes a local pandas/parquet medallion prototype, synthetic source data generation, design docs for Bronze, Silver, Gold, observability, and Power BI, plus GitHub Actions CI. The guides in this folder prepare the next implementation milestone: building the Fabric Bronze ingestion notebook.

These documents are setup and implementation planning guides only. They do not indicate that Fabric items have already been deployed.

## What Runs Locally Today

- Synthetic CSV generation under `data/source/`.
- Local Bronze, Silver, Gold, and observability outputs under ignored `data/` folders.
- Pytest validation for the local medallion prototype.
- CI validation on pull requests and pushes to `main`.

## What Is Planned For Fabric

- A Fabric workspace for development.
- Lakehouse Files landing paths for source CSV extracts.
- Bronze Delta tables created by a Fabric notebook or pipeline.
- Silver Delta tables created by a Fabric notebook after Bronze validation.
- SQL endpoint validation using the Bronze validation query library.
- Later Silver execution, Gold, observability, and Power BI implementation.

Repo-friendly notebook source is available under [fabric_notebooks](../fabric_notebooks/) for the planned Bronze and Silver Fabric notebooks. These files are implementation starting points and do not indicate that Fabric execution has already happened.

## Recommended Setup Sequence

1. Review [workspace_setup.md](workspace_setup.md).
2. Create Lakehouse items using [lakehouse_setup.md](lakehouse_setup.md).
3. Generate and upload source files using [source_file_upload_guide.md](source_file_upload_guide.md).
4. Create the Bronze notebook using [bronze_notebook_setup.md](bronze_notebook_setup.md).
5. Validate Bronze tables using [sql_endpoint_validation_guide.md](sql_endpoint_validation_guide.md).

## Guide Index

- [Workspace Setup](workspace_setup.md)
- [Lakehouse Setup](lakehouse_setup.md)
- [Source File Upload Guide](source_file_upload_guide.md)
- [Bronze Notebook Setup](bronze_notebook_setup.md)
- [SQL Endpoint Validation Guide](sql_endpoint_validation_guide.md)
