# Demo Walkthrough

## Purpose

This walkthrough gives reviewers a concise path through the Sales & Marketing Analytics Platform portfolio project — what runs locally, what runs in the cloud, and how Power BI consumes it.

## Business Problem

A growing commercial organization needs trusted reporting across customers, products, campaigns, orders, ad spend, and support tickets. The project demonstrates how fragmented operational-style extracts can be shaped into governed analytics outputs for revenue analysis, marketing performance, customer segmentation, product reporting, support quality, and data health.

## Architecture

The project follows a medallion architecture:

- Source CSV extracts simulate operational system data.
- Bronze preserves raw source records with ingestion metadata.
- Silver standardizes, type-casts, deduplicates, and validates records.
- Gold creates business-ready dimensions, facts, and KPI-ready fields.
- Observability captures run logs, quality checks, and row count reconciliation.
- Power BI connects live to the Gold layer.

See `assets/architecture_diagram.md` for the full architecture.

## Local Pipeline

The local prototype runs today with Python, pandas, and parquet files.

Run the local demo:

- `pip install -r requirements.txt`
- `python data_generation/generate_source_data.py`
- `python local_pipeline/run_local_medallion.py`
- `python -m pytest`

The pipeline writes ignored local outputs under `data/source/`, `data/bronze/`, `data/silver/`, `data/gold/`, and `data/observability/`.

## dbt Warehouse

The same medallion logic also runs as a dbt project against DuckDB (local, zero credentials) or Snowflake (via dbt Cloud):

- `dbt build --project-dir dbt` — 21 models, ~38 tests

## Gold Model

Dimensions: `dim_customer`, `dim_product`, `dim_campaign`, `dim_date`, `dim_customer_segment`, `dim_channel`.

Facts: `fact_orders`, `fact_ad_spend`, `fact_support_tickets`.

The model supports KPIs such as revenue, net revenue, gross margin, average order value, ad spend, ROAS, conversion rate, ticket count, average resolution time, and customer satisfaction score.

See `assets/demo/gold_model.md` for a visual summary.

## Observability

- Pipeline run logs.
- Data quality results.
- Dataset freshness.
- Row count reconciliation.

## Power BI

The report is fully built and connects live to Snowflake via Power BI's native connector — no file export, no ODBC driver. 6 pages: Executive Overview, Revenue & Margin, Marketing Performance, Customer & Segment Analysis, Product Performance, Support Quality.

## Reviewer Takeaway

This project demonstrates the full analytics delivery path: business problem framing, source data generation, medallion processing, dimensional modeling, data quality, observability, CI, and a live-connected BI layer — running on two interchangeable warehouse targets (DuckDB and Snowflake) from the same dbt codebase.