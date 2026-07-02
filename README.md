# Sales & Marketing Analytics Platform

An end-to-end analytics engineering portfolio project: synthetic sales and marketing data modeled through a Bronze → Silver → Gold medallion pipeline, a tested dbt + DuckDB warehouse, and a Power BI semantic model authored as code. Everything core runs locally with no cloud account.

Built by **Amen Bouallagui** — BI Developer and Analytics Engineer with 2 years of hands-on experience in Microsoft Fabric, Power BI, and data migration on real client projects.

> See [docs/real_world_context.md](docs/real_world_context.md) for the professional background this portfolio extends.

---

## Quick Start

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py

# PowerShell
$env:DBT_PROFILES_DIR = 'dbt'
dbt deps  --project-dir dbt
dbt build --project-dir dbt          # 21 models, ~38 tests — DuckDB, no cloud needed

python local_pipeline/run_local_medallion.py
python -m pytest
```

---

## What This Demonstrates

### Analytics Engineering
- dbt warehouse on DuckDB: sources → staging → intermediate → marts, all tested in CI
- Dimensional modeling: surrogate keys, conformed dimensions with unknown members, date dimension, 3 fact tables
- dbt tests: uniqueness, not-null, referential integrity, accepted values, and a singular business logic test

### Data Engineering
- Bronze / Silver / Gold medallion pipeline in Python (pandas)
- Bronze: raw records with ingestion metadata, row hashes, source lineage
- Silver: type casting, string normalization, deduplication by business key, data quality flags
- Gold: star schema with KPI-ready measures (net revenue, gross margin, ad conversion rates, support resolution times)
- Observability: pipeline run log, data quality results, row count reconciliation

### Power BI & BI Architecture
- Semantic model authored as code (PBIP / TMDL): 8 tables, relationships, ~22 DAX measures
- Star schema optimized for Power BI consumption
- Business metric definitions for revenue, margin, marketing, customer, and support KPIs

### Microsoft Fabric
- Medallion architecture mapped to Fabric Lakehouse (OneLake, Delta tables, notebooks)
- PySpark notebook source for Bronze, Silver, and Gold layers — ready to import into Fabric
- Setup guides for workspace, Lakehouse, source upload, notebook configuration, SQL endpoint validation

### Engineering Practices
- GitHub Actions CI: generates data, runs local pipeline, runs `dbt build` with all tests, validates `.gitignore` hygiene
- Deterministic synthetic data generator with relational integrity validation
- No credentials, no client data — all data is synthetic and seeded

---

## Architecture

```
Source CSVs → Bronze (raw + metadata) → Silver (clean + validated) → Gold (star schema) → Power BI
```

The same medallion logic is implemented twice:
- **dbt + DuckDB** — runs in CI on every push, no cloud account required
- **Python / pandas** — local prototype with parquet outputs and observability tables

See [docs/architecture.md](docs/architecture.md) and [docs/medallion_design.md](docs/medallion_design.md).

---

## Current Status

**Runs in CI today:**
- Synthetic data generation (6 CSV sources: customers, products, campaigns, orders, ad spend, support tickets)
- Local medallion pipeline (Bronze / Silver / Gold + observability parquet outputs)
- dbt warehouse: 21 models, ~38 tests, all passing
- Pytest suite

**Defined, not yet executed in Fabric / Power BI Desktop:**
- Power BI report visuals — semantic model and ~22 DAX measures are defined as code; pages are designed and ready to build
- Microsoft Fabric workspace — setup guides and PySpark notebook source are ready; execution pending

---

## Repository Areas

| Folder | Contents |
|--------|----------|
| [`dbt/`](dbt/) | dbt + DuckDB warehouse — staging, intermediate, marts, tests, CI |
| [`data_generation/`](data_generation/) | Deterministic synthetic source data generator |
| [`local_pipeline/`](local_pipeline/) | Executable pandas medallion prototype with observability |
| [`fabric_notebooks/`](fabric_notebooks/) | PySpark source for Fabric Bronze, Silver, and Gold notebooks |
| [`fabric_implementation/`](fabric_implementation/) | Fabric workspace and Lakehouse setup guides |
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
