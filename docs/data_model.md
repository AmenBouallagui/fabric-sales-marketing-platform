# Data Model

## Modeling Approach

The MVP data model will use a dimensional structure optimized for sales, marketing, product, and customer support analytics. Source-like operational extracts are landed in Bronze, cleaned and standardized in Silver, and later transformed into conformed dimensions and facts in the Gold layer.

## Planned Source Entities

- Customers: customer and account profile data including geography, segment, industry, acquisition channel, and status.
- Products: product catalog data including category, plan tier, pricing, cost, subscription flag, and validity dates.
- Campaigns: marketing campaign metadata including channel, objective, target segment, and campaign dates.
- Orders: sales order transactions including customer, product, quantity, price, discount, tax, payment status, refund flag, and optional campaign attribution.
- Ad spend: campaign-level spend and engagement activity including impressions, clicks, conversions, and spend amount.
- Support tickets: customer support interactions including priority, category, status, satisfaction, response time, and resolution time.

## Planned Silver Tables

The Silver layer prepares cleaned, standardized, typed, and deduplicated entities for Gold modeling:

- `silver_customers`: current customer/account profile records with standardized segments, industries, geography, status, and acquisition channel.
- `silver_products`: current product catalog records with typed prices, costs, categories, plan tiers, subscription flags, and valid date ranges.
- `silver_campaigns`: current marketing campaign records with standardized channels, objectives, target segments, and campaign date ranges.
- `silver_orders`: cleaned order transactions with typed monetary fields, payment status, refund flags, and validated customer/product/campaign relationships.
- `silver_ad_spend`: cleaned campaign spend and engagement measures with validated campaign relationships and non-negative numeric metrics.
- `silver_support_tickets`: cleaned support ticket records with standardized priority, category, status, timestamps, response metrics, and customer relationships.

## Planned Gold Dimensions

- `dim_customer`
- `dim_product`
- `dim_campaign`
- `dim_date`
- `dim_customer_segment`
- `dim_channel`

## Planned Gold Facts

- `fact_orders`
- `fact_ad_spend`
- `fact_support_tickets`

## Relationship Strategy

Gold facts should use surrogate or stable business keys that relate cleanly to conformed dimensions. Order, campaign, ad spend, and support ticket date fields should connect to `dim_date` for consistent time intelligence in Power BI.

## Grain Definitions

- `fact_orders`: one row per order.
- `fact_ad_spend`: one row per campaign spend record.
- `fact_support_tickets`: one row per support ticket.
