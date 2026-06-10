# AI-Ready Sales & Marketing Data Platform

This project demonstrates an end-to-end Microsoft Fabric-style analytics platform for sales, marketing, customer, product, and support data. It includes a synthetic data generator, a local executable medallion pipeline, Bronze/Silver/Gold modeling, data quality and observability design, Power BI semantic model planning, CI validation, and repo-friendly Fabric notebook source.

The repository is built as a portfolio project for Analytics Engineering, BI Engineering, and Microsoft Fabric review. The local prototype runs today with Python, pandas, and parquet; the Fabric workspace, Lakehouse items, Power BI report, and AI/Data Agent extension are planned future implementation steps.

## For Hiring Managers

This repository is designed to be reviewed quickly as a portfolio checkpoint. It shows that the project owner can connect business requirements, data engineering patterns, analytics modeling, BI planning, documentation, testing, and CI into one coherent delivery story.

The strongest signal is that the project is not only a set of diagrams: it includes a local prototype that generates data, runs a medallion pipeline, writes parquet outputs, and validates behavior with tests. Microsoft Fabric and Power BI execution are intentionally described as planned next steps unless a later update documents real deployment.

## Why This Project Matters

This project shows how analytics work moves from raw operational extracts to trusted, business-facing data products. It demonstrates analytics engineering, Power BI semantic modeling, Microsoft Fabric lakehouse architecture, data quality and observability, production-style thinking, and business-facing KPI design.

## Portfolio Demo

The demo proves that the repository can turn synthetic business source data into reviewable analytics outputs using a local Bronze/Silver/Gold pipeline. It also shows how that working local pattern maps to planned Microsoft Fabric Lakehouse notebooks, SQL validation, observability, and a future Power BI semantic model.

Demo entry points:

- [Architecture overview diagram](assets/demo/architecture_overview.md)
- [Gold model diagram](assets/demo/gold_model.md)
- [Demo walkthrough](docs/demo_walkthrough.md)
- [Planned demo assets](assets/demo/README.md)

## What This Demonstrates

- Python data generation.
- Local medallion pipeline with parquet outputs.
- Bronze ingestion metadata.
- Silver standardization, deduplication, and validation.
- Gold dimensional modeling.
- Data quality and observability design.
- Power BI semantic model and report design.
- GitHub Actions CI.
- Fabric-ready notebook source for Bronze, Silver, and Gold.

## Reviewer Quick Start

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
python local_pipeline/run_local_medallion.py
python -m pytest
```

These commands generate synthetic source CSVs, run the local Bronze/Silver/Gold prototype, create local observability outputs, and run tests. Generated CSV and parquet outputs are written under ignored `data/` folders and are intentionally not committed.

## Architecture At A Glance

- Source: synthetic CSV extracts for customers, products, campaigns, orders, ad spend, and support tickets.
- Bronze: raw records plus ingestion metadata.
- Silver: cleaned, typed, deduplicated, validated current records.
- Gold: dimensions, facts, KPI-ready fields, and Power BI-friendly structures.
- Observability: run logs, quality results, freshness concepts, and row count reconciliation.
- Consumption: planned Power BI semantic model, reports, and future AI/Data Agent extension.

See the [architecture diagram](assets/architecture_diagram.md), [architecture overview](docs/architecture.md), and [project roadmap](docs/project_roadmap.md).

## Current Status

Implemented locally:

- Synthetic source data generator.
- Local executable medallion pipeline.
- Local Bronze, Silver, Gold, and observability parquet outputs.
- Pytest coverage for the local prototype.
- GitHub Actions CI.
- Repo-friendly Fabric notebook source for Bronze, Silver, and Gold.

Designed for future Fabric and Power BI implementation:

- Bronze ingestion design.
- Silver transformation design.
- Gold dimensional model design.
- Data quality and observability design.
- Power BI semantic model and report design.
- Fabric workspace, Lakehouse, source upload, notebook, and SQL endpoint setup guides.

Not deployed yet:

- Microsoft Fabric workspace items.
- Fabric Lakehouse Delta tables.
- Data Factory pipeline orchestration.
- Power BI `.pbix` or `.pbit` report.
- AI/Data Agent extension.

## Data Domains

- Customers and segments.
- Products and pricing.
- Campaigns and channels.
- Orders and revenue.
- Ad spend and conversions.
- Support tickets and satisfaction.

## Key Repository Areas

- [data_generation](data_generation/): deterministic synthetic source data generator.
- [local_pipeline](local_pipeline/): executable local medallion prototype.
- [fabric_notebooks](fabric_notebooks/): repo-friendly PySpark source for planned Fabric notebooks.
- [fabric_implementation](fabric_implementation/): practical Fabric setup guides.
- [docs](docs/): architecture, data model, quality, metrics, roadmap, and implementation designs.
- [sql](sql/): representative DDL, validation, observability, and metric queries.
- [powerbi](powerbi/): semantic model and report design notes.
- [tests](tests/): local prototype tests.

## Local Outputs

Running the local prototype writes generated outputs under ignored `data/` folders:

- `data/source/`: source CSV extracts.
- `data/bronze/`: local Bronze parquet outputs.
- `data/silver/`: local Silver parquet outputs.
- `data/gold/`: local Gold parquet outputs.
- `data/observability/`: local run log, quality result, and row count reconciliation outputs.

## Microsoft Fabric Implementation Guides

The repository includes setup guides under [fabric_implementation](fabric_implementation/) for moving from the local prototype toward a real Microsoft Fabric workspace. The guides cover workspace setup, Lakehouse setup, source file upload, Bronze notebook setup, and SQL endpoint validation.

## Fabric Notebook Source

The repository includes version-controlled source for planned Fabric notebooks:

- [nb_01_bronze_ingestion.py](fabric_notebooks/nb_01_bronze_ingestion.py): Bronze ingestion.
- [nb_02_silver_transformations.py](fabric_notebooks/nb_02_silver_transformations.py): Silver transformations.
- [nb_03_gold_modeling.py](fabric_notebooks/nb_03_gold_modeling.py): Gold dimensional modeling.

These files can be copied into future Fabric notebooks or used as implementation references when Fabric notebook assets are created. They have not been executed in Fabric unless documented later.

## Design References

- [Bronze ingestion design](docs/bronze_ingestion_design.md)
- [Silver transformation design](docs/silver_transformation_design.md)
- [Gold dimensional model design](docs/gold_dimensional_model_design.md)
- [Data quality and observability design](docs/data_quality_observability_design.md)
- [Power BI semantic model design](docs/powerbi_semantic_model_design.md)
- [Business metrics](docs/business_metrics.md)
- [Portfolio review checklist](docs/portfolio_review_checklist.md)
- [Demo walkthrough](docs/demo_walkthrough.md)

## Continuous Integration

GitHub Actions CI runs on pull requests and pushes to `main`. The workflow validates dependency installation, synthetic source data generation, local medallion execution, generated-data Git ignore behavior, and pytest.

Generated CSV and parquet outputs remain under the ignored `data/` folder and are not uploaded as CI artifacts.
