# Business Metrics

## Purpose

This document defines the first set of KPI definitions for the future Power BI semantic model. Measures should be implemented from Gold tables so calculations remain consistent across reports.

## Revenue And Customer Metrics

- Revenue: sum of `fact_orders.total_amount`.
- Net Revenue: sum of `fact_orders.net_revenue`, calculated as order total less tax.
- Gross Margin: sum of `fact_orders.gross_margin`, calculated as net revenue less estimated product cost.
- Gross Margin %: gross margin divided by net revenue.
- Average Order Value: revenue divided by order count.
- Orders: distinct count of `fact_orders.order_id`.
- Customers: distinct count of `dim_customer.customer_id`.
- New Customers: count of customers by `dim_customer.signup_date` within the selected date period.

## Marketing Metrics

- Ad Spend: sum of `fact_ad_spend.spend_amount`.
- Impressions: sum of `fact_ad_spend.impressions`.
- Clicks: sum of `fact_ad_spend.clicks`.
- Conversions: sum of `fact_ad_spend.conversions`.
- Conversion Rate: conversions divided by clicks.
- Cost Per Click: ad spend divided by clicks.
- Cost Per Acquisition: ad spend divided by conversions.
- ROAS: revenue attributed to campaigns divided by ad spend.

## Support Metrics

- Ticket Count: distinct count of `fact_support_tickets.ticket_id`.
- Average First Response Minutes: average of `fact_support_tickets.first_response_minutes`.
- Average Resolution Time: average of `fact_support_tickets.resolution_minutes`.
- Customer Satisfaction Score: average of `fact_support_tickets.satisfaction_score`.

## Metric Governance

Each metric should include a definition, source table, calculation logic, filters, exclusions, and owner before being promoted to portfolio-ready status in Power BI.
