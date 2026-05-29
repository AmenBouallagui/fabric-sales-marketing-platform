# Semantic Model Notes

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
