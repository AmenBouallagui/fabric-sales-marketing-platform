# Portfolio Review Checklist

## What To Look At First

1. `README.md` for the project overview and run commands.
2. `assets/architecture_diagram.md` for the end-to-end architecture.
3. `local_pipeline/README.md` for the executable local prototype.
4. `docs/project_roadmap.md` for completed and planned milestones.
5. `docs/powerbi_semantic_model_design.md` for the future reporting layer.

## How To Run The Project Locally

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
python local_pipeline/run_local_medallion.py
pytest
```

The commands generate synthetic source data, run the local medallion prototype, and execute tests.

## What Outputs Are Generated

Generated outputs are written under ignored `data/` folders:

- `data/source/`: source CSV extracts.
- `data/bronze/`: local Bronze parquet outputs.
- `data/silver/`: local Silver parquet outputs.
- `data/gold/`: local Gold parquet outputs.
- `data/observability/`: local run log, quality result, and row count reconciliation outputs.

Generated data is intentionally not committed.

## Fabric Implementation Design Docs

- `docs/bronze_ingestion_design.md`
- `docs/silver_transformation_design.md`
- `docs/gold_dimensional_model_design.md`
- `docs/data_quality_observability_design.md`
- `docs/powerbi_semantic_model_design.md`

These documents explain how the local concepts map to future Microsoft Fabric Lakehouse, notebook, Data Factory, Warehouse, and Power BI work.

## What Demonstrates Production Readiness

- Medallion architecture design.
- Local executable prototype.
- Deterministic synthetic data generation.
- Data quality rules and observability design.
- Run logging and row count reconciliation concepts.
- GitHub Actions CI.
- Tests for local medallion outputs and key relationships.

## What Demonstrates Business Value

- Gold dimensional model for business-ready analytics.
- KPI definitions for revenue, margin, marketing, customer, support, and data health.
- Power BI semantic model and report design.
- Reviewer-friendly architecture and roadmap documentation.

## What Is Not Implemented Yet

- Deployed Microsoft Fabric workspace.
- Fabric Lakehouse tables.
- Data Factory pipeline orchestration.
- Power BI `.pbix` or `.pbit` file.
- Report screenshots.
- AI/Data Agent extension.

## Suggested 10-Minute Reviewer Walkthrough

1. Read the README summary and current status.
2. Open the architecture diagram.
3. Review the local prototype README.
4. Skim the Bronze, Silver, and Gold design docs.
5. Review the data quality and observability design.
6. Review the Power BI report design.
7. Run the local prototype commands if time allows.
8. Check the roadmap for planned Fabric and demo milestones.
