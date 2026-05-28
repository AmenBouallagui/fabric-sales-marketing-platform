# AI-Ready Sales & Marketing Data Platform

## Business Scenario

This portfolio project demonstrates how a growing B2B organization can build a Microsoft Fabric data platform that unifies sales, marketing, customer, product, and campaign activity into an analytics-ready and AI-ready foundation.

The scenario assumes fragmented operational systems: CRM opportunities, marketing campaign engagement, website lead capture, customer accounts, products, and revenue transactions. The platform is designed to help commercial teams understand pipeline health, campaign performance, customer conversion, and revenue trends while preparing governed data products for AI-assisted analysis.

## Architecture Summary

The target architecture follows a medallion-style lakehouse pattern in Microsoft Fabric:

- Bronze layer for raw ingested source data.
- Silver layer for cleaned, standardized, and quality-checked entities.
- Gold layer for business-friendly star-schema tables and curated metrics.
- Semantic model and Power BI reports for executive and operational analytics.
- Data quality tests and documentation to support trust, repeatability, and AI readiness.

## MVP Scope

The MVP focuses on creating a realistic synthetic dataset and a clean analytics foundation for sales and marketing reporting. It will include:

- Synthetic source data generation.
- Core entity modeling for accounts, contacts, leads, opportunities, products, campaigns, and activities.
- Initial data quality rules.
- SQL and notebook transformation examples.
- Power BI-ready metric definitions.
- Documentation for architecture, deployment, and AI readiness.

## Data Domains

- Sales pipeline and opportunities.
- Marketing campaigns and engagement.
- Customer accounts and contacts.
- Products and revenue.
- Lead lifecycle and conversion.
- Commercial activity history.

## Planned Microsoft Fabric Components

- OneLake for centralized storage.
- Fabric Lakehouse for raw and curated tables.
- Data Factory pipelines for orchestration.
- Fabric notebooks for transformation and validation logic.
- Warehouse or SQL endpoint for serving curated relational models.
- Power BI semantic model and reports.
- Optional Data Activator or AI experiences in later phases.

## Build Phases

1. Repository scaffold and documentation foundation.
2. Synthetic data generator for realistic source tables.
3. Bronze ingestion layout and raw file conventions.
4. Silver transformations and data quality checks.
5. Gold dimensional model and metric layer.
6. Power BI semantic model and report screenshots.
7. AI readiness enhancements, metadata, and governance notes.

## Current Status

Initial repository scaffold created. Documentation and project structure are in place. Generated data files have not been created yet.

## How To Run The Data Generator

Install the Python dependencies and generate local synthetic source files:

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
```

By default, generated CSV files are written to `data/source/`. The `data/` folder and `*.csv` files are ignored by Git.

## Bronze Ingestion Design

The next layer after data generation is the Bronze ingestion design. The current design documents how local synthetic CSV extracts under `data/source/` will later be landed into Microsoft Fabric Lakehouse Files and ingested into append-friendly Bronze Delta tables with metadata for lineage, validation, and future incremental loading.

See `docs/bronze_ingestion_design.md`, `notebooks/01_bronze_ingestion.md`, and `sql/bronze_validation_queries.sql`.
