# Project Roadmap

## Project Vision

The AI-Ready Sales & Marketing Data Platform is a portfolio project that demonstrates how sales, marketing, customer, product, ad spend, and support data can be transformed into governed analytics outputs.

The project is designed to show Analytics Engineering, BI Engineering, and Microsoft Fabric readiness through an executable local prototype, practical implementation designs, repo-friendly Fabric notebook source, and Power BI semantic model planning.

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
- Fabric implementation setup guides.
- Fabric Bronze notebook source prepared.
- Fabric Silver notebook source prepared.
- Fabric Gold notebook source prepared.
- Portfolio review checklist and architecture diagram.

## Current Capabilities

- Generate deterministic synthetic source CSV files under `data/source/`.
- Run a local pandas-based medallion prototype.
- Produce local Bronze, Silver, Gold, and observability parquet outputs under ignored `data/` folders.
- Validate the local prototype with pytest.
- Run GitHub Actions CI on pull requests and pushes to `main`.
- Review business metric definitions and Power BI report planning.
- Review future Microsoft Fabric implementation guides.
- Review repo-friendly PySpark source for planned Bronze, Silver, and Gold Fabric notebooks.

## Planned Fabric Implementation Milestones

- Create Fabric workspace and Lakehouses.
- Land generated source CSVs into Lakehouse Files.
- Implement and execute Fabric Bronze ingestion notebook.
- Validate Bronze tables using the SQL endpoint and `sql/bronze_validation_queries.sql`.
- Evaluate Data Factory orchestration for repeatable Bronze ingestion.
- Implement and execute Fabric Silver transformation notebook with validation and deduplication.
- Implement and execute Fabric Gold dimensional modeling notebook or Warehouse objects.
- Add observability tables and validation result logging.
- Orchestrate layer execution with Data Factory pipelines.

The Fabric setup guides prepare this milestone by documenting workspace setup, Lakehouse conventions, source file upload paths, Bronze notebook configuration, and SQL endpoint validation.

Actual Fabric execution remains future/planned unless documented later.

## Planned Power BI Milestones

- Build a Power BI semantic model over Gold tables.
- Configure relationships, date table behavior, formatting, and measure organization.
- Implement KPI measures from documented metric definitions.
- Build report pages for executive, revenue, marketing, customer, product, support, and operations views.
- Capture portfolio screenshots in `powerbi/report_screenshots/` after report pages exist.

## Planned AI/Data Agent Extension

- Document table and column metadata for AI grounding.
- Add curated business glossary terms.
- Add sample prompts for revenue, marketing, support, and data health questions.
- Explore a future AI/Data Agent grounded on Gold and observability outputs.
- Keep synthetic data and governance notes clear so AI usage remains safe for portfolio demonstration.

## Suggested Next Engineering Tasks

- Add local data quality result detail exports for failed Silver records.
- Add a local semantic model validation script for KPI queries.
- Add task runner commands for common local workflows.
- Add schema contracts for source, Bronze, Silver, and Gold tables.
- Expand tests for deduplication, unknown keys, referential integrity, and quality failures.

## Suggested Portfolio/Demo Tasks

- Record a short walkthrough of source generation and local medallion execution.
- Add screenshots after Power BI report pages are built.
- Add a one-page architecture summary for hiring managers.
- Add sample business questions answered by the Gold model.
- Add a demo narrative connecting data engineering, analytics, BI, Fabric readiness, and AI readiness.
- Add README badges or deployment links only after future Fabric or Power BI assets are actually deployed.
