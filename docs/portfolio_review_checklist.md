# Portfolio Review Checklist

## What To Look At First

1. `README.md` for the portfolio summary, skills demonstrated, and run commands.
2. `assets/architecture_diagram.md` for the end-to-end local and planned Fabric architecture.
3. `local_pipeline/README.md` for the executable local medallion prototype.
4. `fabric_notebooks/README.md` for repo-friendly Fabric notebook source.
5. `docs/powerbi_semantic_model_design.md` for the future reporting and semantic model layer.
6. `docs/project_roadmap.md` for completed milestones and planned Fabric work.

## How To Run The Project Locally

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
python local_pipeline/run_local_medallion.py
python -m pytest
```

These commands generate synthetic source data, run the local medallion prototype, and execute tests.

## What Outputs Are Generated

Generated outputs are written under ignored `data/` folders:

- `data/source/`: source CSV extracts.
- `data/bronze/`: local Bronze parquet outputs.
- `data/silver/`: local Silver parquet outputs.
- `data/gold/`: local Gold parquet outputs.
- `data/observability/`: local run log, quality result, and row count reconciliation outputs.

Generated data is intentionally not committed.

## What Demonstrates Analytics Engineering Skill

- Deterministic source data generation.
- Local executable medallion pipeline.
- Bronze metadata and lineage fields.
- Silver standardization, type casting, deduplication, and validation.
- Gold dimensional model with dimensions, facts, and KPI-ready calculations.
- Tests and CI validation.

## What Demonstrates BI And Power BI Skill

- Business metric definitions for revenue, margin, marketing, customer, support, and data health.
- Gold star schema designed for Power BI relationships.
- Semantic model notes with field visibility, formatting, measure organization, and relationship strategy.
- Report design plan for executive, revenue, marketing, customer, product, support, and operations pages.

## What Demonstrates Microsoft Fabric Readiness

- Fabric setup guides for workspace, Lakehouse, source upload, Bronze notebook setup, and SQL endpoint validation.
- Repo-friendly PySpark source for planned Bronze, Silver, and Gold Fabric notebooks.
- SQL validation queries for Bronze, Silver, Gold, business metrics, and observability.
- Clear distinction between local executable prototype and future Fabric deployment.

## What Demonstrates Production-Style Thinking

- Data quality rules and validation strategy.
- Observability model for pipeline run logs, quality results, freshness, and reconciliation.
- Unknown member handling in Gold design.
- CI workflow that validates generation, local pipeline execution, Git ignore behavior, and tests.
- Documentation that separates implemented local behavior from planned Fabric and Power BI work.

## What Is Not Implemented Yet

- Deployed Microsoft Fabric workspace.
- Fabric Lakehouse Delta tables.
- Data Factory pipeline orchestration.
- Power BI `.pbix` or `.pbit` file.
- Report screenshots.
- AI/Data Agent extension.

## Suggested 10-Minute Reviewer Walkthrough

1. Read the README summary and current status.
2. Open the architecture diagram.
3. Review the local prototype README.
4. Skim the Fabric notebook source README.
5. Skim the Bronze, Silver, and Gold design docs.
6. Review the Power BI semantic model and report design.
7. Review data quality and observability design.
8. Run the local prototype commands if time allows.
9. Check the roadmap for planned Fabric, Power BI, and AI/Data Agent milestones.
