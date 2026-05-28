# Gold Dimensional Model Design

## Purpose

The Gold layer transforms cleaned Silver tables into business-ready dimensions, facts, KPI definitions, and a Power BI-ready semantic model structure. Gold is optimized for reporting, metric consistency, and reviewer-friendly analytics rather than raw source preservation.

This document is a design and implementation plan for a future Microsoft Fabric build. It does not claim that the Fabric notebook, Warehouse objects, or Power BI semantic model have already been deployed.

## Inputs And Outputs

Gold modeling reads from cleaned Silver tables:

- `silver_customers`
- `silver_products`
- `silver_campaigns`
- `silver_orders`
- `silver_ad_spend`
- `silver_support_tickets`

Gold modeling produces dimensions and facts:

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

## Star Schema Overview

The Gold model follows a simple star schema:

- `fact_orders` is the primary sales fact and connects to customer, product, campaign, channel, and date dimensions.
- `fact_ad_spend` is the marketing investment fact and connects to campaign, channel, and date dimensions.
- `fact_support_tickets` is the service quality fact and connects to customer and date dimensions.

This structure keeps Power BI relationships predictable and makes common KPI calculations easy to define in a semantic model.

## Dimension Design

| Dimension | Grain | Source | Purpose |
| --- | --- | --- | --- |
| `dim_customer` | One row per current customer | `silver_customers` | Customer attributes for segmentation, geography, industry, status, and acquisition analysis. |
| `dim_product` | One row per current product | `silver_products` | Product attributes for category, plan tier, pricing, cost, and subscription analysis. |
| `dim_campaign` | One row per current campaign | `silver_campaigns` | Campaign attributes for objective, target segment, channel, and date analysis. |
| `dim_date` | One row per calendar date | Generated date spine | Standard date filtering and time intelligence. |
| `dim_customer_segment` | One row per customer segment | `silver_customers` | Reusable customer segment reporting. |
| `dim_channel` | One row per marketing or acquisition channel | `silver_customers`, `silver_campaigns`, `silver_ad_spend` | Reusable channel reporting across acquisition, campaign, and spend analysis. |

## Fact Table Design

| Fact | Grain | Source | Main measures |
| --- | --- | --- | --- |
| `fact_orders` | One row per order | `silver_orders` | Quantity, unit price, discount amount, tax amount, total amount, net revenue, estimated cost, gross margin. |
| `fact_ad_spend` | One row per campaign spend record | `silver_ad_spend` | Spend amount, impressions, clicks, conversions. |
| `fact_support_tickets` | One row per support ticket | `silver_support_tickets` | Ticket count, first response minutes, resolution minutes, satisfaction score. |

## Grain Definitions

- `dim_customer`: one row per current customer.
- `dim_product`: one row per current product.
- `dim_campaign`: one row per current campaign.
- `dim_date`: one row per calendar date.
- `dim_customer_segment`: one row per customer segment.
- `dim_channel`: one row per channel.
- `fact_orders`: one row per order.
- `fact_ad_spend`: one row per campaign spend record.
- `fact_support_tickets`: one row per support ticket.

## Surrogate Key Strategy

- Gold dimensions should use stable generated integer or hash-based surrogate keys.
- Source business IDs should be preserved as alternate keys, such as `customer_id`, `product_id`, and `campaign_id`.
- Facts should join to dimensions using Gold surrogate keys where possible.
- Unknown or missing dimension members should use a documented default surrogate key such as `-1`.
- Surrogate key generation should be deterministic so reruns produce stable joins when source business keys do not change.

## Date Dimension Strategy

`dim_date` should cover the full analytical date range across order dates, spend dates, ticket created dates, ticket closed dates, campaign dates, product validity dates, and customer signup dates.

Recommended attributes:

- `date_key` in `YYYYMMDD` integer format.
- Calendar date.
- Year, quarter, month, month name, week, day of month, and day of week.
- Weekend flag.
- Month start date and month end date.

Facts should store date foreign keys for the relevant business date fields.

## Handling Unknown Or Missing Dimension Values

Unknown dimension members should exist in each dimension where facts may have missing or unmatched values:

- `customer_key = -1`
- `product_key = -1`
- `campaign_key = -1`
- `date_key = -1`
- `customer_segment_key = -1`
- `channel_key = -1`

Unknown members should use clear labels such as `Unknown Customer`, `Unknown Product`, `Unknown Campaign`, `Unknown Segment`, and `Unknown Channel`.

## KPI And Measure Strategy

The Power BI semantic model should define measures from Gold facts, not directly from Silver tables.

Planned KPI examples:

- Revenue
- Net Revenue
- Gross Margin
- Gross Margin %
- Average Order Value
- Orders
- Customers
- New Customers
- Ad Spend
- Impressions
- Clicks
- Conversions
- Conversion Rate
- Cost Per Click
- Cost Per Acquisition
- ROAS
- Ticket Count
- Average First Response Minutes
- Average Resolution Minutes
- Average Satisfaction Score

Measure definitions should be documented in `docs/business_metrics.md` and implemented consistently in Power BI.

## Power BI Semantic Model Notes

- Hide technical keys by default and expose business-friendly attributes.
- Use a single-direction relationship pattern where possible.
- Mark `dim_date` as the date table in Power BI.
- Build measures in the semantic model instead of repeating calculations in visuals.
- Use display folders for sales, marketing, customer, and support metrics.
- Keep Gold facts additive and avoid pre-aggregating away useful dimensions.

## Gold Validation Strategy

Gold validation should confirm:

- One row per expected dimension and fact grain.
- Unique surrogate keys in dimensions.
- Unique fact business keys where applicable.
- Facts do not contain null required foreign keys.
- Unknown dimension key usage is visible and explainable.
- Fact-to-dimension joins are valid.
- Additive measures are non-negative where expected.
- Date keys are covered by `dim_date`.
- Silver-to-Gold row counts reconcile for valid/current records.
- KPI sanity checks, including ROAS and gross margin, produce reasonable values.

## Future Fabric Implementation Notes

The future Microsoft Fabric implementation can use:

- Fabric notebooks with PySpark for dimension and fact construction.
- Delta tables for Gold dimensions and facts.
- Fabric Warehouse or SQL endpoint DDL for table shape review.
- Data Factory pipelines to orchestrate Silver-to-Gold runs.
- Power BI semantic model relationships and DAX measures over Gold tables.

The first implementation should prioritize transparent transformations, deterministic keys, and reviewable validation output.

## Success Criteria

The Gold design is successful when:

- All six planned dimensions and three planned facts are documented.
- Fact and dimension grains are clear.
- Surrogate key and unknown-member handling are defined.
- KPI definitions align with available source domains.
- Power BI relationship and measure strategy is understandable.
- SQL DDL and validation queries provide a practical implementation reference.
- A reviewer can understand how Silver data becomes a Power BI-ready Gold model.
