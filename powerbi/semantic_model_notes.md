# Semantic Model Notes

## Target Users & Scope

- Executives: revenue, margin, campaign performance, customer health.
- Marketing analysts: channel efficiency, campaign performance, conversion metrics.
- Support managers: ticket volume, response/resolution time, satisfaction.
- Platform reviewers: model structure, data-quality outcomes, operational health.

The model exposes the curated Gold star schema and hides technical fields. Report
pages are detailed in [report_design.md](report_design.md); metric definitions in
[../docs/business_metrics.md](../docs/business_metrics.md).

## Relationship Key Mapping

Single-direction relationships from dimensions to facts:

- `fct_orders.customer_key` → `dim_customer.customer_key`
- `fct_orders.product_key` → `dim_product.product_key`
- `fct_orders.campaign_key` → `dim_campaign.campaign_key`
- `fct_orders.order_date_key` → `dim_date.date_key`
- `fct_ad_spend.campaign_key` → `dim_campaign.campaign_key`
- `fct_ad_spend.channel_key` → `dim_channel.channel_key`
- `fct_ad_spend.spend_date_key` → `dim_date.date_key`
- `fct_support_tickets.customer_key` → `dim_customer.customer_key`
- `fct_support_tickets.created_date_key` → `dim_date.date_key`

Mark `dim_date` as the official date table. Keep secondary date relationships
(e.g. ticket closed date) inactive unless a page needs them.

## Table Descriptions

- `dim_customer`: customer attributes for geography, segment, industry, acquisition channel, lifecycle status, and signup date.
- `dim_product`: product attributes for category, plan tier, price, cost, subscription flag, and validity dates.
- `dim_campaign`: campaign attributes for channel, target segment, objective, and campaign dates.
- `dim_date`: calendar attributes for time filtering and time intelligence.
- `dim_customer_segment`: reusable segment labels for customer analysis.
- `dim_channel`: reusable channel labels for acquisition and marketing analysis.
- `fact_orders`: order-level revenue, cost, margin, payment, and refund measures.
- `fact_ad_spend`: campaign spend and engagement metrics by date and channel.
- `fact_support_tickets`: support ticket volume, satisfaction, response time, and resolution time.

## Hidden Technical Fields

Recommended hidden fields:

- Surrogate keys such as `customer_key`, `product_key`, `campaign_key`, `channel_key`, and date keys.
- Technical timestamps such as `gold_processed_at`.
- Source system or lineage fields if they are added to Gold later.
- Raw numeric columns when a curated measure should be used instead.

## Recommended Visible Fields

Recommended visible fields:

- Customer name, segment, country, city, industry, status, and signup date.
- Product name, category, plan tier, price, and subscription flag.
- Campaign name, channel, objective, target segment, and campaign dates.
- Calendar date, year, quarter, month, month name, and day of week.
- Support ticket priority, category, status, and satisfaction score.

## Recommended Measure Table

Create a dedicated measure table named `Measures` or `_Measures` with no relationship to facts or dimensions.

Suggested display folders:

- Revenue and Margin
- Customer
- Marketing
- Support
- Data Health

## Relationship Notes

- Use single-direction relationships from dimensions to facts where possible.
- Use `dim_date` as the official date table.
- Keep secondary date relationships inactive unless a report page explicitly needs them.
- Facts should join through Gold surrogate keys, while source business IDs remain available for drill-through or validation where useful.

## Formatting Conventions

- Currency: Revenue, Net Revenue, Gross Margin, Average Order Value, Ad Spend, Cost Per Click, Cost Per Acquisition.
- Percentage: Gross Margin %, Conversion Rate, ROAS where expressed as a percentage.
- Whole numbers: Orders, Customers, New Customers, Impressions, Clicks, Conversions, Ticket Count.
- Decimal: Average Satisfaction Score.
- Duration: Average First Response Minutes and Average Resolution Minutes.

## Display Folders

Recommended model display folders:

- Customer Attributes.
- Product Attributes.
- Campaign Attributes.
- Date Attributes.
- Revenue and Margin Measures.
- Marketing Measures.
- Support Measures.
- Data Health Measures.

## Future Row-Level Security Notes

Future row-level security can be designed after real access requirements are known. Candidate patterns include filtering by customer segment, geography, or operational responsibility. This portfolio version does not include security rules or sensitive data.
