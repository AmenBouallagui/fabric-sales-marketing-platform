# Power BI Report Build Guide

This repo ships the Power BI **semantic model as code** (PBIP / TMDL) in
[`SalesMarketing.SemanticModel/`](SalesMarketing.SemanticModel/). The model defines
the tables, relationships, and ~22 DAX measures over the dbt **gold** star schema,
and the report (`SalesMarketing.Report/`) ships fully built — 6 pages, all visuals,
no assembly required.

The semantic model connects **live to Snowflake** via Power BI's native connector,
reading the gold marts produced by the [dbt project](../dbt/) (see its README for
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

1. Open `powerbi/SalesMarketing.pbip` in Power BI Desktop.
2. **Refresh**. You'll be prompted for your Snowflake server (`<account>.snowflakecomputing.com`)
   and warehouse the first time; after that, credentials are cached per machine.
3. All 8 tables load directly from `SALES_MARKETING.MARTS`.

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

Each page has a horizontal filter bar (month, plus two page-relevant dimensions) and
a dark sidebar with global navigation. No "Operations / Data Health" page is built —
the model loads the gold star only; that page would need `dbt test` results or
pipeline observability output wired in as extra tables.

## Capture screenshots

Export page screenshots (File → Export, or a screenshot tool) into a
`powerbi/report_screenshots/` folder and link them from [README](../README.md).
Recruiters look for these first.

## Reviewing without Snowflake access

If you don't have Snowflake credentials, you can still verify the underlying data
modeling — the [dbt project](../dbt/) runs entirely locally via DuckDB with zero
cloud credentials (`dbt build --project-dir dbt`), producing the same gold star
schema this report reads from. The semantic model (TMDL) and report layout (PBIR)
are also fully readable as plain text/JSON in source control without opening
Desktop at all.
