# AI-Ready Sales & Marketing Data Platform

## Business Scenario

This portfolio project demonstrates how a growing B2B organization can build a Microsoft Fabric data platform that unifies sales, marketing, customer, product, and campaign activity into an analytics-ready and AI-ready foundation.

The scenario assumes fragmented operational systems for customers, products, campaigns, orders, ad spend, and support tickets. The platform is designed to help commercial teams understand revenue, campaign efficiency, customer behavior, and service quality while preparing governed data products for AI-assisted analysis.

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
- Core entity modeling for customers, products, campaigns, orders, ad spend, and support tickets.
- Initial data quality rules.
- SQL and notebook transformation examples.
- Power BI-ready metric definitions.
- Documentation for architecture, deployment, and AI readiness.

## Data Domains

- Customers and segments.
- Products and pricing.
- Campaigns and channels.
- Orders and revenue.
- Ad spend and conversions.
- Support tickets and satisfaction.

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

Repository scaffold, synthetic data generator, Bronze ingestion design, Silver transformation design, and Gold dimensional model design are in place. Generated data files are intentionally not committed.

## How To Run The Data Generator

Install the Python dependencies and generate local synthetic source files:

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
```

By default, generated CSV files are written to `data/source/`. The `data/` folder and `*.csv` files are ignored by Git.

## Run The Local Prototype

Run the local medallion prototype to validate source-to-Bronze-to-Silver-to-Gold logic before future Microsoft Fabric implementation:

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
python local_pipeline/run_local_medallion.py
pytest
```

The local prototype writes parquet outputs under `data/bronze/`, `data/silver/`, `data/gold/`, and `data/observability/`. These generated folders remain ignored by Git.

## Continuous Integration

GitHub Actions CI runs on pull requests and pushes to `main`. The workflow validates dependency installation, synthetic source data generation, local medallion execution, generated-data Git ignore behavior, and pytest.

Generated CSV and parquet outputs remain under the ignored `data/` folder and are not uploaded as CI artifacts.

## Bronze Ingestion Design

The next layer after data generation is the Bronze ingestion design. The current design documents how local synthetic CSV extracts under `data/source/` will later be landed into Microsoft Fabric Lakehouse Files and ingested into append-friendly Bronze Delta tables with metadata for lineage, validation, and future incremental loading.

See `docs/bronze_ingestion_design.md`, `notebooks/01_bronze_ingestion.md`, and `sql/bronze_validation_queries.sql`.

## Silver Transformation Design

The next layer after Bronze is Silver transformations. The Silver design documents how Bronze raw tables will later be cleaned, standardized, type-cast, deduplicated, validated, and prepared for Gold dimensional modeling.

See `docs/silver_transformation_design.md`, `notebooks/02_silver_transformations.md`, and `sql/silver_validation_queries.sql`.

## Gold Dimensional Model Design

The next layer after Silver is Gold dimensional modeling. The Gold design documents how cleaned Silver tables will later become business-ready dimensions, facts, KPI definitions, and a Power BI-ready semantic model structure.

See `docs/gold_dimensional_model_design.md`, `notebooks/03_gold_modeling.md`, `sql/gold_model_ddl.sql`, and `sql/gold_validation_queries.sql`.

## Power BI Semantic Model Design

The Gold model is intended to feed a future Power BI semantic model and dashboard. The design documents relationships, measures, report pages, and a future screenshot/demo plan without creating `.pbix`, `.pbit`, or generated image assets.

See `docs/powerbi_semantic_model_design.md`, `powerbi/semantic_model_notes.md`, `powerbi/report_design.md`, and `sql/business_metric_queries.sql`.

## Data Quality And Observability

Data quality and observability make the platform production-ready by documenting how future Fabric runs will track validation outcomes, pipeline status, dataset freshness, row count reconciliation, and operational health.

See `docs/data_quality_observability_design.md`, `notebooks/04_data_quality_checks.md`, `notebooks/05_observability_logging.md`, `sql/observability_model_ddl.sql`, and `sql/observability_validation_queries.sql`.
