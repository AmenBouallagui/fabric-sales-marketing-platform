# Lakehouse Setup

## Purpose

This guide defines the recommended Lakehouse layout for the future Microsoft Fabric implementation of the medallion architecture.

## Recommended Portfolio Option

For this portfolio project, use one Lakehouse per medallion layer:

- `lh_sales_marketing_bronze`
- `lh_sales_marketing_silver`
- `lh_sales_marketing_gold`

This layout makes layer ownership and reviewer navigation clear. It also mirrors the local prototype outputs under `data/bronze/`, `data/silver/`, and `data/gold/`.

## Alternative Single-Lakehouse Option

For a smaller demo, a single Lakehouse can be used with table and folder conventions to separate layers. Example table prefixes:

- `bronze_`
- `silver_`
- `dim_`
- `fact_`

The single-Lakehouse option is simpler to manage but provides less visual separation between raw, cleaned, and curated assets.

## Suggested Files Path Convention

Source CSV extracts should land in Lakehouse Files using this convention:

```text
Files/source/{source_system}/{entity}/load_date=YYYY-MM-DD/file.csv
```

Example:

```text
Files/source/synthetic_crm/customers/load_date=2026-01-01/customers.csv
```

## Expected Source Systems

- `synthetic_crm`: customers, products, orders, support tickets.
- `synthetic_marketing`: campaigns, ad spend.

## Suggested Table Naming Conventions

Bronze tables:

- `bronze_customers_raw`
- `bronze_products_raw`
- `bronze_campaigns_raw`
- `bronze_orders_raw`
- `bronze_ad_spend_raw`
- `bronze_support_tickets_raw`

Silver tables:

- `silver_customers`
- `silver_products`
- `silver_campaigns`
- `silver_orders`
- `silver_ad_spend`
- `silver_support_tickets`

Gold tables:

- `dim_customer`
- `dim_product`
- `dim_campaign`
- `dim_date`
- `dim_customer_segment`
- `dim_channel`
- `fact_orders`
- `fact_ad_spend`
- `fact_support_tickets`

## Implementation Notes

- Keep raw files in Files until they are loaded into Bronze Delta tables.
- Preserve the load date and source system in both file paths and ingestion metadata.
- Use consistent entity names across folder paths, notebook configuration, table names, and validation queries.
