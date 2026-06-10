# Demo Walkthrough

## Purpose

This walkthrough gives reviewers a concise path through the AI-Ready Sales & Marketing Data Platform portfolio project. It focuses on what works locally today and how the design prepares for future Microsoft Fabric and Power BI implementation.

## Business Problem

A growing commercial organization needs trusted reporting across customers, products, campaigns, orders, ad spend, and support tickets. The project demonstrates how fragmented operational-style extracts can be shaped into governed analytics outputs for revenue analysis, marketing performance, customer segmentation, product reporting, support quality, and data health.

## Architecture

The project follows a medallion architecture:

- Source CSV extracts simulate operational system data.
- Bronze preserves raw source records with ingestion metadata.
- Silver standardizes, type-casts, deduplicates, and validates records.
- Gold creates business-ready dimensions, facts, and KPI-ready fields.
- Observability captures run logs, quality checks, and row count reconciliation.
- Power BI and AI/Data Agent layers are planned consumption paths.

See `assets/architecture_diagram.md` for the visual architecture.

## Local Pipeline

The local prototype runs today with Python, pandas, and parquet files. It is intended to validate the medallion logic before any Fabric workspace is deployed.

Run the local demo:

- `pip install -r requirements.txt`
- `python data_generation/generate_source_data.py`
- `python local_pipeline/run_local_medallion.py`
- `python -m pytest`

The pipeline writes ignored local outputs under `data/source/`, `data/bronze/`, `data/silver/`, `data/gold/`, and `data/observability/`.

## Gold Model

The Gold layer is designed for business-ready analytics and Power BI consumption.

Planned dimensions:

- `dim_customer`
- `dim_product`
- `dim_campaign`
- `dim_date`
- `dim_customer_segment`
- `dim_channel`

Planned facts:

- `fact_orders`
- `fact_ad_spend`
- `fact_support_tickets`

The model supports KPIs such as revenue, net revenue, gross margin, average order value, ad spend, ROAS, conversion rate, ticket count, average resolution time, and customer satisfaction score.

## Observability

The project includes a production-style observability design for:

- Pipeline run logs.
- Data quality results.
- Dataset freshness.
- Row count reconciliation.
- Critical, warning, and informational quality outcomes.

The local prototype writes basic observability outputs. Future Fabric implementation can persist these concepts into observability Delta tables or Warehouse objects.

## Power BI Plan

The Power BI work is currently a design and implementation plan, not a completed report. The repository includes semantic model notes, report page planning, and business metric definitions for future Power BI development.

Planned report pages include:

- Executive Overview.
- Revenue & Margin.
- Marketing Performance.
- Customer & Segment Analysis.
- Product Performance.
- Support Quality.
- Operations / Data Health.

## Fabric Roadmap

Fabric execution is planned but not claimed as complete. The repository prepares for implementation with:

- Workspace and Lakehouse setup guides.
- Source file upload guide.
- Bronze notebook setup guide.
- SQL endpoint validation guide.
- Repo-friendly PySpark source for Bronze, Silver, and Gold notebooks.

The next Fabric milestone is to create the workspace and Lakehouses, upload generated CSV files to Lakehouse Files, execute the Bronze notebook, and validate Bronze tables through the SQL endpoint.

## Reviewer Takeaway

This project demonstrates the full analytics delivery path: business problem framing, source data generation, medallion processing, dimensional modeling, data quality, observability, CI, BI planning, and Fabric implementation readiness. The local prototype runs today; Fabric and Power BI execution remain planned future work unless documented later.
