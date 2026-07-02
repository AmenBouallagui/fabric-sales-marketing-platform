# Project Roadmap

## Project Vision

A portfolio analytics platform showing end-to-end data engineering and BI skills: medallion architecture, dbt modeling, dimensional design, Power BI semantic modeling, and Microsoft Fabric patterns. Built on a foundation of real professional experience (see [real_world_context.md](real_world_context.md)).

## Completed

- Synthetic data generator (6 sources, deterministic, relational integrity validated)
- Local medallion prototype in Python (Bronze / Silver / Gold + observability outputs)
- dbt + DuckDB warehouse: 21 models, ~38 tests, all passing
- Staging → intermediate → marts layering with surrogate keys and unknown members
- Power BI semantic model as code (PBIP / TMDL): 8 tables, ~22 DAX measures, relationships
- GitHub Actions CI (data generation → local pipeline → dbt build + tests → pytest)
- Medallion design, data quality and observability design, business metrics definitions
- Fabric setup guides (workspace, Lakehouse, source upload, Bronze setup, SQL endpoint)
- PySpark notebook source for Bronze, Silver, and Gold layers

## Priority: Power BI Report

The semantic model is defined. Next step is building the actual report pages in Power BI Desktop:

1. Connect Desktop to the exported Gold parquet files (`powerbi/export_gold.py`)
2. Build report pages per [powerbi/report_build_guide.md](../powerbi/report_build_guide.md):
   - Executive Summary (revenue trend, gross margin, campaign ROI, top products)
   - Revenue & Orders (order volume, discount analysis, payment status breakdown)
   - Marketing Performance (spend vs. conversions, cost per acquisition by channel)
   - Customer Analytics (segment breakdown, churn indicators, lifetime value proxy)
   - Support Operations (ticket volume, resolution time, satisfaction trends)
3. Capture screenshots for portfolio presentation
4. Publish to Power BI Service for public embed (optional)

## Fabric Execution (Next After Power BI)

- Create Fabric workspace and Lakehouses (Bronze, Silver, Gold separation)
- Land source CSVs into OneLake / Lakehouse Files
- Execute Bronze notebook (`fabric_notebooks/nb_01_bronze_ingestion.py`)
- Validate Bronze tables via SQL endpoint
- Execute Silver and Gold notebooks
- Add Data Factory pipeline for orchestration
- Connect Power BI semantic model to Fabric SQL endpoint instead of local parquet

## Ongoing

- Learn dbt well enough to extend the existing models and explain design decisions in interviews
- Add German localization to README once German improves (broadens visibility on local job boards)
