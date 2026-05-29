# Project Roadmap

## Project Vision

The AI-Ready Sales & Marketing Data Platform demonstrates how customers, products, campaigns, orders, ad spend, and support tickets can be shaped into a governed Microsoft Fabric-style analytics platform.

The project is designed to be understandable to reviewers while still showing production-oriented thinking: medallion architecture, local validation, data quality, observability, Gold dimensional modeling, and future Power BI reporting.

## Completed Milestones

- Initial repository scaffold.
- Synthetic data generator.
- Local medallion prototype.
- Bronze ingestion design.
- Silver transformation design.
- Gold dimensional model design.
- Data quality and observability design.
- Power BI semantic model and report design.
- GitHub Actions CI.

## Current Capabilities

- Generate deterministic synthetic source CSV files under `data/source/`.
- Run a local pandas-based medallion prototype.
- Produce local Bronze, Silver, Gold, and observability parquet outputs under ignored `data/` folders.
- Validate the local prototype with pytest.
- Run GitHub Actions CI on pull requests and pushes to `main`.
- Review design documentation for future Fabric implementation.

## Planned Fabric Implementation Milestones

- Create Fabric workspace and Lakehouse.
- Land generated source CSVs into Lakehouse Files.
- Implement Bronze ingestion notebook or Data Factory pipeline.
- Implement Silver transformation notebook with validation and deduplication.
- Implement Gold dimensional modeling notebook or Warehouse objects.
- Add observability tables and validation result logging.
- Orchestrate layer execution with Data Factory pipelines.

## Planned Power BI Milestones

- Build Power BI semantic model over Gold tables.
- Configure relationships, date table, formatting, and measure table.
- Implement KPI measures from documented definitions.
- Build report pages for executive, revenue, marketing, customer, product, support, and operations views.
- Capture portfolio screenshots in `powerbi/report_screenshots/`.

## Planned AI/Data Agent Extension

- Document table and column metadata for AI grounding.
- Add curated business glossary terms.
- Add sample prompts for revenue, marketing, support, and data health questions.
- Explore a future data agent that answers questions from Gold and observability outputs.
- Keep synthetic data and governance notes clear so AI usage remains safe for portfolio demonstration.

## Suggested Next Engineering Tasks

- Add local data quality result detail exports for failed Silver records.
- Add a small local semantic model validation script for KPI queries.
- Add Makefile or task runner commands for common workflows.
- Add schema contracts for source, Bronze, Silver, and Gold tables.
- Expand tests for deduplication, unknown keys, and quality failures.

## Suggested Portfolio/Demo Tasks

- Record a short walkthrough of source generation and local medallion execution.
- Add screenshots after Power BI report pages are built.
- Add a one-page architecture summary for hiring managers.
- Add sample business questions answered by the Gold model.
- Add a demo narrative connecting data engineering, analytics, and AI readiness.
