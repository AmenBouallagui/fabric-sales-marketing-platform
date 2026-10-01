# Power BI Report Build Guide

This repo ships the Power BI **semantic model as code** (PBIP / TMDL) in
[`SalesMarketing.SemanticModel/`](SalesMarketing.SemanticModel/). The model defines
the tables, relationships, and 28 DAX measures over the dbt **gold** star schema,
and the report (`SalesMarketing.Report/`) ships fully built — 7 pages, all visuals,
no assembly required.

The semantic model uses **Import mode** through Power BI's native Snowflake connector,
loading the gold marts produced by the [dbt project](../dbt/) (see its README for
the DuckDB-local vs. Snowflake-via-dbt-Cloud dual setup). No ODBC driver or file
export is needed — Power BI's Snowflake connector is built in.

## Prerequisites

1. **Power BI Desktop** (latest), with **Preview features → Power BI Project (.pbip)
   save format** enabled, and *Store semantic model using TMDL format* on.
2. A Snowflake account with the gold marts already built — run the
   [dbt project](../dbt/) against a Snowflake target (`dbt seed && dbt build`) so the
   `SALES_MARKETING.MARTS` schema contains the 9 gold tables.
3. Your Snowflake **account identifier** and **warehouse** name, and a login
   (username/password or key-pair) for the account's `MARTS` schema.

## Open and refresh

1. Open the project and configure Transform data → Manage parameters: `SnowflakeServer`, `SnowflakeWarehouse`, `SnowflakeDatabase`, `SnowflakeRole`, `SnowflakeMartsSchema`, and `SnowflakeObservabilitySchema`. The server is a placeholder; the role defaults to `ANALYTICS_READER`. Your Snowflake administrator must provide a reporting role with warehouse usage, database/schema usage, and SELECT on the imported tables. No credentials are committed.
2. Open `powerbi/SalesMarketing.pbip` in Power BI Desktop, then **Refresh**
   and authenticate with your own Snowflake credentials.
3. Refresh imports eight business tables from `SALES_MARKETING.MARTS` and three
   demonstration telemetry tables from `SALES_MARKETING.OBSERVABILITY`. The
   disconnected measure table is defined locally in TMDL. Data changes in
   Snowflake appear after a refresh, not through live queries.

The model arrives with relationships and measures already defined (display folders:
Revenue and Margin, Customer, Marketing, Support). Technical keys are hidden, and
`dim_date` is already marked as the model's date table.

## Report pages (all built)

| Page | Key visuals | Primary measures |
| --- | --- | --- |
| Executive Overview | Hero KPI + sparkline, revenue trend, revenue mix donut, margin combo | Revenue, Net Revenue, Gross Margin %, ROAS |
| Revenue & Margin | Revenue/Net Revenue trend, margin by category, category detail table | Revenue, Net Revenue, Gross Margin, Average Order Value |
| Marketing Performance | Conversion rate trend, ROAS by campaign, ad spend mix donut | Ad Spend, ROAS, Cost Per Click, Cost Per Acquisition |
| Customer & Segment Analysis | New customers trend, revenue by segment, customers by country donut | Customers, New Customers, Revenue, Average Order Value |
| Product Performance | Orders by product, revenue mix donut, margin by plan tier combo | Revenue, Gross Margin, Gross Margin %, Orders |
| Support Quality | Satisfaction trend, first response by priority, ticket status donut | Ticket Count, Avg First Response, Avg Resolution, Avg Satisfaction |
| Operations & Data Health | Run status, failed checks, row-count reconciliation | Pipeline Success Rate, Failed Checks, Reconciliation Mismatches |

Each page has a horizontal filter bar (month, plus two page-relevant dimensions) and
a dark sidebar with global navigation. Operations & Data Health uses the
committed observability seeds. These are demonstration records, not current CI
results or a live feed from the pandas pipeline.

## Demo screenshot

The README screenshot is a frame from the committed recording, with the Startup segment selected. It predates the KPI corrections; current values require a new Desktop refresh. Only Executive Overview is shown in that recording.

## Capture screenshots

Export page screenshots (File → Export, or a screenshot tool) into a
`powerbi/report_screenshots/` folder and link them from [README](../README.md).
Recruiters look for these first.

## Reviewing without Snowflake access

If you don't have Snowflake credentials, you can still verify the underlying data
modeling — the [dbt project](../dbt/) runs entirely locally via DuckDB with zero
cloud credentials (run `dbt deps`, `dbt seed`, then `dbt build` with
`--project-dir dbt` and `DBT_PROFILES_DIR=dbt`), producing the same gold star
schema this report reads from. The semantic model (TMDL) and report layout (PBIR)
are also fully readable as plain text/JSON in source control without opening
Desktop at all.
