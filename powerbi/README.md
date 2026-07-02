# Power BI

This folder contains the Power BI layer as **code**: a Power BI Project (`.pbip`)
whose semantic model is defined in TMDL over the dbt **gold** star schema. It reads
the gold tables as Parquet files (exported from DuckDB) — no database driver needed.
Report visuals are assembled in Power BI Desktop following the build guide.

## Power BI Project (BI as code)

- [`SalesMarketing.pbip`](SalesMarketing.pbip) — open this in Power BI Desktop.
- [`SalesMarketing.SemanticModel/`](SalesMarketing.SemanticModel/) — TMDL definition: 8 tables, relationships, and ~22 DAX measures over the gold model, reading the gold Parquet exports via the `GoldDataFolder` parameter (no database driver needed).
- [`SalesMarketing.Report/`](SalesMarketing.Report/) — report shell (PBIR format) with a starter page; add the remaining pages in Desktop.
- [`export_gold.py`](export_gold.py) — exports the gold marts to `data/powerbi/*.parquet` for Power BI to read.
- [`report_build_guide.md`](report_build_guide.md) — prerequisites, export step, open/refresh steps, and the per-page visual plan.

## Design Files

- `semantic_model_notes.md`: semantic model table, field, relationship, formatting, display folder, and future security notes.
- `report_design.md`: planned report pages, visuals, measures, slicers, and reviewer talking points.

These build the Power BI layer over the Gold star schema from the [dbt project](../dbt/), described in [docs/medallion_design.md](../docs/medallion_design.md).

## Planned Report Pages

- Executive revenue overview.
- Campaign performance.
- Customer and segment analysis.
- Product performance.
- Support quality.
- Data quality summary.

## Future Operations / Data Health Dashboard

A future operations dashboard should help reviewers and operators monitor platform health. Planned visuals include:

- Pipeline success rate.
- Failed checks.
- Freshness status.
- Failed critical checks.
- Warning checks.
- Row count reconciliation.
- Latest successful load.
- Tables with repeated failures.

## Screenshot Storage

Report screenshots should be added under `powerbi/` (e.g. a `report_screenshots/` folder) once the report visuals are built and ready for portfolio presentation.

The committed artifact is the source-controlled semantic model (TMDL). Report
visuals and screenshots are produced in Power BI Desktop per the build guide; no
`.pbix` binary is committed.
