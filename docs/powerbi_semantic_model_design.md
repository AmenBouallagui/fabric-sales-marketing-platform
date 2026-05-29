# Power BI Semantic Model Design

## Purpose

This document describes how the Gold dimensional model will be exposed through a future Power BI semantic model and report experience. It is a design and implementation plan, not a claim that a Power BI report already exists.

## Target Users

- Executive stakeholders reviewing revenue, margin, campaign performance, and customer health.
- Marketing analysts reviewing channel efficiency, campaign performance, and conversion metrics.
- Customer success and support managers reviewing ticket volume, response time, resolution time, and satisfaction.
- Data platform reviewers validating model structure, data quality outcomes, and operational health.

## Semantic Model Scope

The semantic model should expose curated Gold dimensions and facts for business reporting:

- Revenue and margin analysis.
- Customer and segment analysis.
- Marketing performance analysis.
- Support quality analysis.
- Data health and observability monitoring.

The model should hide technical implementation details where possible and expose business-friendly fields and measures.

## Gold Tables Used

Dimensions:

- `dim_customer`
- `dim_product`
- `dim_campaign`
- `dim_date`
- `dim_customer_segment`
- `dim_channel`

Facts:

- `fact_orders`
- `fact_ad_spend`
- `fact_support_tickets`

Future operations reporting can also use observability tables such as `pipeline_run_log`, `data_quality_results`, `dataset_freshness`, and `row_count_reconciliation`.

## Relationship Design

Core relationships should generally be single-direction from dimensions to facts:

- `fact_orders.customer_key` -> `dim_customer.customer_key`
- `fact_orders.product_key` -> `dim_product.product_key`
- `fact_orders.campaign_key` -> `dim_campaign.campaign_key`
- `fact_orders.order_date_key` -> `dim_date.date_key`
- `fact_ad_spend.campaign_key` -> `dim_campaign.campaign_key`
- `fact_ad_spend.channel_key` -> `dim_channel.channel_key`
- `fact_ad_spend.spend_date_key` -> `dim_date.date_key`
- `fact_support_tickets.customer_key` -> `dim_customer.customer_key`
- `fact_support_tickets.created_date_key` -> `dim_date.date_key`

Optional inactive relationships can be considered later for secondary dates, such as ticket closed date or campaign end date.

## Measure Design Principles

- Define measures in a dedicated measure table.
- Prefer explicit base measures such as Revenue, Ad Spend, Orders, and Ticket Count.
- Build ratio measures from base measures.
- Use divide-by-zero safe logic for ratios.
- Use consistent formatting for currency, percentages, whole numbers, and durations.
- Hide raw numeric columns when a curated measure should be used instead.
- Keep measure names business-friendly and stable.

## KPI Groups

- Revenue and margin: Revenue, Net Revenue, Gross Margin, Gross Margin %, Average Order Value, Orders.
- Customer: Customers, New Customers, customer segment mix, active customer share.
- Marketing: Ad Spend, Impressions, Clicks, Conversions, Conversion Rate, Cost Per Click, Cost Per Acquisition, ROAS.
- Support: Ticket Count, Average First Response Minutes, Average Resolution Minutes, Average Satisfaction Score.
- Data health / observability: pipeline success rate, failed checks, freshness status, warning checks, row count reconciliation.

## Date Table Strategy

`dim_date` should be marked as the official date table in Power BI.

Recommended behavior:

- Use `dim_date.calendar_date` as the primary date column.
- Relate `fact_orders.order_date_key` to `dim_date.date_key`.
- Relate `fact_ad_spend.spend_date_key` to `dim_date.date_key`.
- Relate `fact_support_tickets.created_date_key` to `dim_date.date_key`.
- Add inactive relationships later only when a report needs alternate date analysis.

## Filter And Slicer Strategy

Recommended slicers:

- Date range.
- Customer segment.
- Country and city.
- Product category and plan tier.
- Campaign and channel.
- Support ticket priority, category, and status.
- Data quality status and layer for operations pages.

Keep slicers consistent across pages where possible so reviewers can compare metrics without relearning filters.

## Report Page Design

Planned report pages:

- Executive Overview.
- Revenue & Margin.
- Marketing Performance.
- Customer & Segment Analysis.
- Product Performance.
- Support Quality.
- Operations / Data Health.

Each page should have a clear purpose, a small set of primary KPIs, supporting trend visuals, and drillable detail where useful.

## Security And Governance Notes

- Do not store secrets or credentials in Power BI files or repository assets.
- Hide surrogate keys, hashes, and technical timestamps from report users by default.
- Keep metric definitions documented in `docs/business_metrics.md`.
- Use consistent measure names and formatting.
- Future row-level security can be designed by customer segment, geography, or business ownership if real organizational requirements are introduced.

## Future Fabric / Power BI Implementation Notes

Future implementation steps:

1. Publish Gold tables to a Fabric Lakehouse or Warehouse.
2. Build a Power BI semantic model over Gold tables.
3. Configure relationships and mark `dim_date` as the date table.
4. Create a dedicated measure table.
5. Build report pages using the planned layout.
6. Capture screenshots in `powerbi/report_screenshots/` for portfolio presentation.

## Screenshot And Demo Plan

Future demo assets should include:

- Executive Overview screenshot.
- Revenue & Margin screenshot.
- Marketing Performance screenshot.
- Support Quality screenshot.
- Operations / Data Health screenshot.
- Short walkthrough notes explaining source generation, local prototype validation, Gold model shape, and Power BI KPI usage.

No `.pbix`, `.pbit`, screenshots, or generated files are created by this design.

## Success Criteria

The design is successful when:

- Gold tables map cleanly into a Power BI star schema.
- Relationships are documented and predictable.
- Measures are grouped and named for business users.
- Report pages align with the current project domains.
- Data health reporting is represented as part of the user experience.
- A reviewer can understand how the Gold model becomes a future Power BI semantic model and dashboard.
