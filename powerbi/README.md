# Power BI

This folder contains the Power BI layer as **code**: a Power BI Project (`.pbip`)
whose semantic model is defined in TMDL over the dbt **gold** star schema. It
connects live to Snowflake via Power BI's native connector — no ODBC driver, no
file export. All 7 report pages are fully built.

## Power BI Project (BI as code)

- [`SalesMarketing.pbip`](SalesMarketing.pbip) — open this in Power BI Desktop.
- [`SalesMarketing.SemanticModel/`](SalesMarketing.SemanticModel/) — TMDL definition: 11 tables, relationships, and ~28 DAX measures over the gold model, reading live from Snowflake's `SALES_MARKETING.MARTS` schema.
- [`SalesMarketing.Report/`](SalesMarketing.Report/) — fully built report (PBIR format): Executive Overview, Revenue & Margin, Marketing Performance, Customer & Segment Analysis, Product Performance, Support Quality, and Operations & Data Health.
- [`export_gold.py`](export_gold.py) — legacy: exports the gold marts to `data/powerbi/*.parquet`, from when the model read local files instead of Snowflake. Kept for reference; not used by the current model.
- [`report_build_guide.md`](report_build_guide.md) — prerequisites, Snowflake connection details, and the built page/visual reference.

## Design Files

- `semantic_model_notes.md`: semantic model table, field, relationship, formatting, display folder, and future security notes.
- `report_design.md`: planned report pages, visuals, measures, slicers, and reviewer talking points.

These build the Power BI layer over the Gold star schema from the [dbt project](../dbt/), described in [docs/medallion_design.md](../docs/medallion_design.md).

## Report Pages

All 7 pages are built — see [report_build_guide.md](report_build_guide.md) for the
full per-page visual and measure breakdown: Executive Overview, Revenue & Margin,
Marketing Performance, Customer & Segment Analysis, Product Performance,
Support Quality, and Operations & Data Health.

## Operations & Data Health Dashboard

The 7th report page, sourced from `dbt seed`-loaded observability tables (`pipeline_run_log`, `data_quality_results`, `row_count_reconciliation`) in a dedicated `observability` schema:

- Pipeline success rate.
- Failed checks (by severity, over time).
- Failed critical checks.
- Warning checks.
- Row count reconciliation detail.

## Screenshot Storage

Report screenshots should be added under `powerbi/` (e.g. a `report_screenshots/` folder) once the report visuals are built and ready for portfolio presentation.

The committed artifact is the source-controlled semantic model (TMDL). Report
visuals and screenshots are produced in Power BI Desktop per the build guide; no
`.pbix` binary is committed.
