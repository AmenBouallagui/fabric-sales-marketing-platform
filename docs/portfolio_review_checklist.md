# Portfolio Review Checklist

Target roles: **BI Developer**, **Analytics Engineer**, **Data Analyst (BI-focused)**

---

## Where To Start (5 minutes)

1. [README.md](../README.md) — what runs, what's designed, tech stack overview
2. [docs/real_world_context.md](real_world_context.md) — professional background this project extends
3. [assets/architecture_diagram.md](../assets/architecture_diagram.md) — end-to-end architecture at a glance
4. [dbt/README.md](../dbt/README.md) — the runnable dbt warehouse (the engineering core)
5. [powerbi/semantic_model_notes.md](../powerbi/semantic_model_notes.md) — semantic model design and DAX measures

---

## How To Run Locally (under 5 minutes)

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py
$env:DBT_PROFILES_DIR = 'dbt'   # PowerShell
dbt deps  --project-dir dbt
dbt build --project-dir dbt     # builds 21 models, runs ~38 tests
python local_pipeline/run_local_medallion.py
python -m pytest
```

Generated data is written under ignored `data/` folders and is not committed.

---

## Skills Demonstrated

### Analytics Engineering
- dbt project: sources, staging, intermediate (Silver), marts (Gold) — all tested in CI
- dbt testing: uniqueness, not-null, referential integrity, accepted values, singular business logic test
- Surrogate keys via `dbt_utils.generate_surrogate_key()` — warehouse-agnostic
- Dimensional modeling: unknown member rows, conformed dimensions, date dimension, 3 fact tables

### Data Engineering
- Medallion pipeline: Bronze (ingestion metadata + row hash) → Silver (dedup, type casting, quality flags) → Gold (star schema + KPI measures)
- Observability: pipeline run log, quality check results, row count reconciliation
- Deterministic synthetic data generation with relational integrity validation

### Power BI & BI
- Semantic model as code (PBIP / TMDL): 8 tables, relationships, ~22 DAX measures
- Business metrics definitions: revenue, gross margin, marketing ROI, customer, support
- Report design across 5 domains (Executive, Revenue, Marketing, Customer, Support)
- Star schema optimized for Power BI: correct relationship cardinality, hidden FK columns, display folders

### Microsoft Fabric
- Medallion architecture mapped to Fabric (OneLake, Lakehouse, Delta tables, notebooks, SQL endpoint)
- PySpark notebook source for all three layers — ready to import into Fabric
- Practical setup guides covering workspace creation through SQL endpoint validation

### Engineering Practices
- GitHub Actions CI validates the full local pipeline on every push
- No secrets, no client data — all data is synthetic and seeded

---

## What Is Not Implemented Yet

- Microsoft Fabric workspace (guides and notebook source are ready; not yet executed)
- Power BI report visuals (semantic model defined; pages to be built in Desktop)
- Data Factory pipeline orchestration

---

## Reviewer Notes

The local prototype is fully executable and CI-validated. Fabric and Power BI execution are the planned next phases, clearly separated from what works today.

For professional context — real-world experience with Power BI, Fabric, and data migration — see [docs/real_world_context.md](real_world_context.md).
