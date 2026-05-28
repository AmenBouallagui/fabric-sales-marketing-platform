# Data Model

## Modeling Approach

The MVP data model will use a dimensional structure optimized for sales and marketing analytics. Source-like operational tables will be transformed into conformed dimensions and facts in the Gold layer.

## Planned Source Entities

- Accounts: organizations, industries, regions, segments, and ownership.
- Contacts: people associated with accounts.
- Leads: inbound and outbound prospects with lifecycle status.
- Opportunities: sales pipeline records with stage, value, probability, and close dates.
- Campaigns: marketing programs, channels, budget, and targeting.
- Campaign interactions: email, event, ad, and content engagement activity.
- Products: product catalog and commercial attributes.
- Revenue transactions: booked revenue by account, product, and period.
- Sales activities: calls, meetings, demos, and follow-ups.

## Planned Silver Tables

The Silver layer prepares cleaned, standardized, typed, and deduplicated entities for Gold modeling:

- `silver_customers`: current customer/account profile records with standardized segments, industries, geography, status, and acquisition channel.
- `silver_products`: current product catalog records with typed prices, costs, categories, plan tiers, subscription flags, and valid date ranges.
- `silver_campaigns`: current marketing campaign records with standardized channels, objectives, target segments, and campaign date ranges.
- `silver_orders`: cleaned order transactions with typed monetary fields, payment status, refund flags, and validated customer/product/campaign relationships.
- `silver_ad_spend`: cleaned campaign spend and engagement measures with validated campaign relationships and non-negative numeric metrics.
- `silver_support_tickets`: cleaned support ticket records with standardized priority, category, status, timestamps, response metrics, and customer relationships.

## Planned Gold Dimensions

- `dim_account`
- `dim_contact`
- `dim_product`
- `dim_campaign`
- `dim_date`
- `dim_sales_rep`
- `dim_region`

## Planned Gold Facts

- `fact_opportunity`
- `fact_lead`
- `fact_campaign_interaction`
- `fact_revenue`
- `fact_sales_activity`

## Relationship Strategy

Gold facts should use surrogate or stable business keys that relate cleanly to conformed dimensions. Date fields should connect to `dim_date` for consistent time intelligence in Power BI.

## Grain Definitions

- `fact_opportunity`: one row per opportunity.
- `fact_lead`: one row per lead.
- `fact_campaign_interaction`: one row per campaign interaction event.
- `fact_revenue`: one row per account, product, transaction date, and order event.
- `fact_sales_activity`: one row per sales activity.
