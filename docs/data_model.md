# Data Model

## Overview

The data model for the AI-Ready Sales & Marketing Data Platform follows a medallion pattern. Synthetic source extracts are landed as raw Bronze tables, transformed into cleaned Silver entities, and later modeled into Gold dimensions and facts for Power BI reporting.

The current project domains are:

- Customers
- Products
- Campaigns
- Orders
- Ad spend
- Support tickets

## Planned Source Entities

- Customers: profile, geography, segment, industry, acquisition channel, signup date, lifecycle status, and update timestamp.
- Products: product catalog attributes, category, plan tier, price, cost, subscription flag, validity dates, and update timestamp.
- Campaigns: campaign metadata, marketing channel, date range, target segment, objective, and update timestamp.
- Orders: customer purchases with product, date, quantity, price, discount, tax, total amount, payment status, refund flag, optional campaign attribution, and update timestamp.
- Ad spend: campaign spend by date with channel, impressions, clicks, conversions, spend amount, and update timestamp.
- Support tickets: service interactions with customer, open and close timestamps, priority, category, status, satisfaction, response time, resolution time, and update timestamp.

## Bronze Layer Tables

Bronze tables preserve source records with ingestion metadata and minimal transformation:

- `bronze_customers_raw`
- `bronze_products_raw`
- `bronze_campaigns_raw`
- `bronze_orders_raw`
- `bronze_ad_spend_raw`
- `bronze_support_tickets_raw`

Bronze records should keep source identifiers, source values, file lineage, load date, ingestion run details, `source_updated_at`, and `row_hash`.

## Silver Layer Tables

Silver tables clean, standardize, type-cast, deduplicate, and validate Bronze records:

- `silver_customers`: one current customer record per `customer_id`, with standardized geography, segment, industry, status, and acquisition channel.
- `silver_products`: one current product record per `product_id`, with typed price, cost, validity dates, category, plan tier, and subscription flag.
- `silver_campaigns`: one current campaign record per `campaign_id`, with standardized channel, objective, target segment, and campaign date range.
- `silver_orders`: one current order record per `order_id`, with typed monetary fields, payment status, refund flag, and validated customer, product, and optional campaign relationships.
- `silver_ad_spend`: one current spend record per `spend_id`, with typed spend and engagement metrics and validated campaign relationship.
- `silver_support_tickets`: one current ticket record per `ticket_id`, with standardized priority, category, status, timestamps, satisfaction score, response time, resolution time, and validated customer relationship.

Silver records should include `silver_processed_at`, `is_current_record`, `dq_status`, and `dq_issue_reason`.

## Planned Gold Dimensions

Gold dimensions should provide reporting-friendly descriptive tables:

- `dim_customer`
- `dim_product`
- `dim_campaign`
- `dim_date`
- `dim_customer_segment`
- `dim_channel`

## Planned Gold Facts

Gold facts should provide metric-ready transactional and activity tables:

- `fact_orders`
- `fact_ad_spend`
- `fact_support_tickets`

## Relationship Strategy

Gold facts should relate to conformed dimensions through stable keys derived from Silver tables:

- `fact_orders` links to `dim_customer`, `dim_product`, `dim_campaign` when campaign attribution exists, and `dim_date`.
- `fact_ad_spend` links to `dim_campaign`, `dim_channel`, and `dim_date`.
- `fact_support_tickets` links to `dim_customer` and `dim_date`.
- Customer segment attributes should be available through `dim_customer` and can also be modeled in `dim_customer_segment` for reusable segment analysis.
- Channel attributes should be available through campaign and spend records and can also be modeled in `dim_channel` for reusable channel analysis.

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

## Notes For Power BI

- Power BI should consume Gold tables rather than raw Bronze tables.
- Gold facts should expose additive measures such as order amount, tax amount, discount amount, spend amount, impressions, clicks, conversions, response minutes, and resolution minutes.
- `dim_date` should support filtering by order date, spend date, ticket created date, and ticket closed date where useful.
- The model should keep relationships simple and mostly single-directional for predictable report behavior.
- Data quality indicators from Silver can be summarized in Power BI to show record readiness before Gold publication.
