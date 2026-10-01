# Sales & Marketing Analytics Platform

An end-to-end analytics engineering portfolio project: synthetic sales and marketing data modeled through a Bronze → Silver → Gold medallion pipeline, a tested dbt warehouse that runs on either DuckDB (local, zero credentials) or Snowflake (via dbt Cloud), and a Power BI semantic model authored as code — using the native Snowflake connector in Import mode, all 7 report pages built.

Built by **Amen Bouallagui** — BI Developer and Analytics Engineer with 2 years of part-time experience in Microsoft Fabric, Power BI, and data migration on real client projects.

> See [docs/real_world_context.md](docs/real_world_context.md) for the professional background this portfolio extends.

---

## Power BI Report

<video src="powerbi/report_screenshots/executive_overview.mp4" controls width="800"></video>

Executive Overview page, using Power BI's native Snowflake connector in Import mode — 7 pages total covering revenue, margin, marketing, customer segments, product performance, support quality, and operations/data health. See [powerbi/report_build_guide.md](powerbi/report_build_guide.md) for the full page-by-page breakdown.

---

## Quick Start

```bash
python -m pip install -r requirements.txt
python data_generation/generate_source_data.py
python local_pipeline/run_local_medallion.py

# Bash / zsh
export DBT_PROFILES_DIR=dbt
# PowerShell alternative: $env:DBT_PROFILES_DIR = 'dbt'
dbt deps  --project-dir dbt
dbt seed --project-dir dbt          # load committed synthetic fixtures first
dbt build --project-dir dbt         # 21 models and 38 data tests

python -m pytest
```

The pandas pipeline consumes the generated files in `data/source/`. The dbt
warehouse consumes the committed fixtures in `dbt/seeds/`, loaded into `raw`
and `observability` by `dbt seed`. These are separate synthetic datasets;
generating new CSVs does not update the dbt fixtures. See [dbt/README.md](dbt/README.md)
for the source-loading sequence.

---

## What This Demonstrates

### Analytics Engineering
- dbt warehouse on DuckDB: sources → staging → intermediate → marts, with a CI workflow for model and data-test validation
- Dimensional modeling: surrogate keys, conformed dimensions with unknown members, date dimension, 3 fact tables
- dbt tests: uniqueness, not-null, referential integrity, accepted values, and a singular business logic test

### Data Engineering
- Bronze / Silver / Gold medallion pipeline in Python (pandas)
- Bronze: raw records with ingestion metadata, row hashes, source lineage
- Silver: type casting, string normalization, deduplication by business key, data quality flags
- Gold: star schema with KPI-ready measures (net revenue, gross margin, ad conversion rates, support resolution times)
- Observability: pipeline run log, data quality results, row count reconciliation

### Power BI & BI Architecture
- Semantic model authored as code (PBIP / TMDL): 11 data tables plus a measure table, relationships, and 28 DAX measures
- Star schema optimized for Power BI consumption
- Business metric definitions for revenue, margin, marketing, customer, and support KPIs

### Engineering Practices
- GitHub Actions CI: generates data, runs local pipeline, loads dbt seeds before `dbt build` and its data tests, validates `.gitignore` hygiene
- Deterministic synthetic data generator with relational integrity validation
- No credentials or client data committed — all input data is synthetic

---

## Architecture

```
Generated CSVs → pandas Bronze → Silver → Gold parquet outputs
Committed CSV fixtures → dbt seed → staging → intermediate → marts → Power BI (Snowflake Import)
```

The layered analytics design is demonstrated in two implementations with separate inputs:
- **dbt + DuckDB** — committed seed fixtures → staging → intermediate → marts; validated by CI without a cloud account
- **Python / pandas** — generated CSVs → Bronze/Silver/Gold parquet outputs and observability tables

See [docs/architecture.md](docs/architecture.md) and [docs/medallion_design.md](docs/medallion_design.md).

---

## Current Status

**Runs today:**
- Synthetic data generation (6 CSV sources: customers, products, campaigns, orders, ad spend, support tickets)
- Local medallion pipeline (Bronze / Silver / Gold + observability parquet outputs)
- dbt warehouse: 21 models, 38 data tests — runs on DuckDB (CI, zero credentials) or Snowflake (via dbt Cloud)
- Pytest suite
- Power BI report: 7 pages built, semantic model using the native Snowflake connector in Import mode

---

## Repository Areas

| Folder | Contents |
|--------|----------|
| [`dbt/`](dbt/) | dbt + DuckDB warehouse — staging, intermediate, marts, tests, CI |
| [`data_generation/`](data_generation/) | Deterministic synthetic source data generator |
| [`local_pipeline/`](local_pipeline/) | Executable pandas medallion prototype with observability |
| [`powerbi/`](powerbi/) | Semantic model as code (PBIP / TMDL), DAX measures, design notes |
| [`docs/`](docs/) | Architecture, medallion design, data quality, business metrics, roadmap |
| [`sql/`](sql/) | Validation, observability, and business metric queries |
| [`tests/`](tests/) | Pytest test suite |

---

## Data Domain

Six source entities covering the full sales and marketing lifecycle:

| Entity | Key Fields |
|--------|-----------|
| Customers | segment, signup date, status, region |
| Products | catalog, unit price, unit cost, subscription flag |
| Campaigns | channel, start/end dates, budget targets |
| Orders | quantity, discount, tax, net revenue, payment status, refund flag |
| Ad Spend | daily spend, impressions, clicks, conversions by campaign and channel |
| Support Tickets | priority, category, resolution time, first response time, satisfaction score |

---

## Design References

- [Medallion design (Bronze → Silver → Gold)](docs/medallion_design.md)
- [Data quality and observability](docs/data_quality_observability.md)
- [Business metrics (~22 KPI definitions)](docs/business_metrics.md)
- [Power BI semantic model notes](powerbi/semantic_model_notes.md)
- [Power BI report design](powerbi/report_design.md)
- [Project roadmap](docs/project_roadmap.md)
- [Portfolio review checklist](docs/portfolio_review_checklist.md)
- [Real-world professional context](docs/real_world_context.md)
