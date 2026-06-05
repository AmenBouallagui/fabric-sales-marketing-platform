# Portfolio Review Checklist

## What To Look At First

Start with `README.md` for the portfolio summary, skills demonstrated, and local run commands. Then review `assets/architecture_diagram.md` for the end-to-end view of the local prototype and planned Microsoft Fabric path.

The most useful technical entry points are `local_pipeline/README.md` for the executable local medallion prototype, `fabric_notebooks/README.md` for repo-friendly Fabric notebook source, `docs/powerbi_semantic_model_design.md` for BI and semantic model planning, and `docs/project_roadmap.md` for completed milestones and planned work.

## How To Run The Project Locally

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
python local_pipeline/run_local_medallion.py
python -m pytest
```

These commands generate synthetic source data, run the local Bronze/Silver/Gold medallion prototype, create local observability outputs, and execute tests. Generated CSV and parquet outputs are written under ignored `data/` folders and are intentionally not committed.

## 10-Minute Reviewer Walkthrough

1. Read the README summary and current status.
2. Open the architecture diagram.
3. Review the local pipeline README.
4. Skim the Fabric notebook source README.
5. Review the Power BI semantic model and report design.
6. Skim the Bronze, Silver, Gold, data quality, and observability design docs.
7. Run the local commands if time allows.
8. Check the roadmap for future Fabric, Power BI, and AI/Data Agent milestones.

## Skills Demonstrated

### Analytics Engineering

- Medallion architecture from source extracts through Bronze, Silver, and Gold.
- Silver standardization, type casting, deduplication, and validation design.
- Gold dimensional modeling with dimensions, facts, surrogate keys, unknown members, and KPI-ready fields.
- Business metric definitions aligned to reporting and semantic model needs.

### BI / Power BI

- Power BI semantic model design with relationship strategy and measure planning.
- Business-facing report page design for executive, revenue, marketing, customer, product, support, and operations views.
- KPI definitions for revenue, margin, marketing performance, customer analysis, support quality, and data health.

### Data Engineering Foundations

- Deterministic Python source data generation.
- Local pandas/parquet medallion pipeline.
- Data quality checks, row count reconciliation, and observability outputs.
- Pytest coverage and GitHub Actions CI.

### Microsoft Fabric Readiness

- Fabric setup guides for workspace, Lakehouse, source upload, Bronze notebook setup, and SQL endpoint validation.
- Repo-friendly PySpark notebook source for planned Bronze, Silver, and Gold Fabric notebooks.
- SQL validation and DDL artifacts for Bronze, Silver, Gold, business metrics, and observability.

### Production Readiness

- Clear separation between implemented local prototype and planned Fabric deployment.
- Generated data excluded from Git.
- No secrets, credentials, tenant IDs, workspace IDs, `.pbix`, `.pbit`, or `.ipynb` files included.
- Documentation for validation, observability, idempotency, unknown members, and future operational monitoring.

## What Demonstrates Business Value

- Unified sales, marketing, customer, product, ad spend, and support domains.
- Gold facts and dimensions designed for business-ready analytics.
- KPI planning for revenue, net revenue, margin, campaign performance, support quality, and data health.
- Power BI report design aimed at executive and operational decision-making.
- AI-readiness framing through governed data, documented metrics, and quality metadata.

## What Is Not Implemented Yet

- Deployed Microsoft Fabric workspace.
- Fabric Lakehouse Delta tables.
- Data Factory pipeline orchestration.
- Power BI `.pbix` or `.pbit` file.
- Report screenshots.
- AI/Data Agent extension.
