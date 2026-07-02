# Power BI Report Build Guide

This repo ships the Power BI **semantic model as code** (PBIP / TMDL) in
[`SalesMarketing.SemanticModel/`](SalesMarketing.SemanticModel/). The model defines
the tables, relationships, and ~22 DAX measures over the dbt **gold** star schema.
It reads the gold tables as **Parquet files** (exported from the DuckDB warehouse),
so there is no database driver to install — Power BI loads the files directly. You
open it in Power BI Desktop, refresh, then lay out the report pages.

> **Authoring note:** the TMDL/PBIP files were authored in source control without a
> local Power BI Desktop to validate them. The semantic model is the reviewable
> artifact. If Power BI flags an issue opening the *report*, see *Recovery* below —
> the model itself is independent and reusable.

## Prerequisites

1. **Power BI Desktop** (latest), with **Preview features → Power BI Project (.pbip) save format** enabled, and *Store semantic model using TMDL format* on.
2. The gold Parquet files. From the repo root run:
   ```bash
   pip install -r requirements.txt
   python data_generation/generate_source_data.py
   export DBT_PROFILES_DIR=dbt        # PowerShell: $env:DBT_PROFILES_DIR='dbt'
   dbt deps  --project-dir dbt
   dbt build --project-dir dbt        # build + test the warehouse
   python powerbi/export_gold.py      # export gold marts -> data/powerbi/*.parquet
   ```
   The export step writes one Parquet file per gold table into `data/powerbi/`
   (gitignored). No database driver is required — Power BI reads the files directly.

## Open and refresh

1. Open `powerbi/SalesMarketing.pbip` in Power BI Desktop.
2. Set the data folder: **Transform data → Manage parameters → `GoldDataFolder`** and point it at your absolute path to `data/powerbi` (the committed default is this machine's path).
3. **Refresh**. All eight tables load from the Parquet files — no credentials prompt.
4. **Mark the date table:** select `dim_date` → **Table tools → Mark as date table** → date column `calendar_date`.

The model arrives with relationships and measures already defined (display folders:
Revenue and Margin, Customer, Marketing, Support). Technical keys are hidden.

## Build the pages

The report opens on a starter **Executive Overview** page. Add the other six pages
with **Insert → New page** (or the `+` at the bottom) and build the visuals per
[report_design.md](report_design.md). Suggested layout:

| Page | Key visuals | Primary measures |
| --- | --- | --- |
| Executive Overview | KPI cards + revenue trend + revenue vs. spend | Revenue, Net Revenue, Gross Margin %, ROAS, Ticket Count, Avg Satisfaction |
| Revenue & Margin | Revenue/Net Revenue by month; margin by category; AOV by segment | Revenue, Net Revenue, Gross Margin, Gross Margin %, Average Order Value, Orders |
| Marketing Performance | ROAS by campaign; spend/clicks/conversions by channel; conversion-rate trend | Ad Spend, Clicks, Conversions, Conversion Rate, Cost Per Click, Cost Per Acquisition, ROAS |
| Customer & Segment | Customers by segment; revenue by segment; new customers by month | Customers, New Customers, Revenue, Average Order Value |
| Product Performance | Revenue by category; margin by plan tier; orders by product | Revenue, Gross Margin, Gross Margin %, Orders |
| Support Quality | Tickets by status; response/resolution by priority/category; satisfaction trend | Ticket Count, Avg First Response (min), Avg Resolution (min), Avg Satisfaction |
| Operations / Data Health | (Optional) dbt test / observability summary | — see note below |

Add slicers (date, customer segment, channel, product category) consistently across
pages. Use `dim_date[calendar_date]` for all time axes.

> **Operations / Data Health page** is optional. The current model loads the gold
> star only. To populate it, add the local pipeline's `data/observability/` outputs
> or `dbt test` results as extra tables, or remove the page.

## Capture screenshots

When the report looks good, export page screenshots (File → Export, or a screenshot
tool) into a `powerbi/report_screenshots/` folder and link them from
[README](../README.md). Recruiters look for these first.

## Recovery (if the report still won't open)

The report layout (PBIR JSON) is version-sensitive and was authored without a local
Desktop to validate. The **semantic model is independent** — if the report fails to
load, you lose nothing of value. Bulletproof fix using your own Desktop to generate a
valid report shell:

1. Open Power BI Desktop (blank). Ensure **File → Options → Preview features → "Power
   BI Project (.pbip) save format"** is enabled.
2. **File → Save as → Power BI project (.pbip)** into a new empty temp folder, named
   `SalesMarketing`. Desktop writes a valid, version-matched `SalesMarketing.Report/`
   and `SalesMarketing.SemanticModel/`.
3. Close Desktop. In that temp project, replace the contents of
   `SalesMarketing.SemanticModel/` with this repo's
   `powerbi/SalesMarketing.SemanticModel/` (the whole `definition/` folder plus
   `definition.pbism`).
4. Open the temp `SalesMarketing.pbip`. The report is now Desktop-native (valid) and
   the model is ours. Build the pages, then copy the project back into `powerbi/`.

You keep the full TMDL model, measures, and relationships either way.
