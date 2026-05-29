# Business Metrics

## Purpose

This document defines the first set of KPI definitions for the future Power BI semantic model. Measures should be implemented from Gold tables so calculations remain consistent across reports.

## Revenue And Customer Metrics

- Revenue (`[Revenue]`): sum of `fact_orders.total_amount`.
- Net Revenue (`[Net Revenue]`): sum of `fact_orders.net_revenue`, calculated as order total less tax.
- Gross Margin (`[Gross Margin]`): sum of `fact_orders.gross_margin`, calculated as net revenue less estimated product cost.
- Gross Margin % (`[Gross Margin %]`): gross margin divided by net revenue.
- Average Order Value (`[Average Order Value]`): revenue divided by order count.
- Orders (`[Orders]`): distinct count of `fact_orders.order_id`.
- Customers (`[Customers]`): distinct count of `dim_customer.customer_id`.
- New Customers (`[New Customers]`): count of customers by `dim_customer.signup_date` within the selected date period.

## Marketing Metrics

- Ad Spend (`[Ad Spend]`): sum of `fact_ad_spend.spend_amount`.
- Impressions (`[Impressions]`): sum of `fact_ad_spend.impressions`.
- Clicks (`[Clicks]`): sum of `fact_ad_spend.clicks`.
- Conversions (`[Conversions]`): sum of `fact_ad_spend.conversions`.
- Conversion Rate (`[Conversion Rate]`): conversions divided by clicks.
- Cost Per Click (`[Cost Per Click]`): ad spend divided by clicks.
- Cost Per Acquisition (`[Cost Per Acquisition]`): ad spend divided by conversions.
- ROAS (`[ROAS]`): revenue attributed to campaigns divided by ad spend.

## Support Metrics

- Ticket Count (`[Ticket Count]`): distinct count of `fact_support_tickets.ticket_id`.
- Average First Response Minutes (`[Average First Response Minutes]`): average of `fact_support_tickets.first_response_minutes`.
- Average Resolution Time (`[Average Resolution Time]`): average of `fact_support_tickets.resolution_minutes`.
- Customer Satisfaction Score (`[Customer Satisfaction Score]`): average of `fact_support_tickets.satisfaction_score`.

## Divide-By-Zero Handling

Ratio measures should use safe division logic so blank or zero denominators return blank rather than an error. Examples include Gross Margin %, Average Order Value, Conversion Rate, Cost Per Click, Cost Per Acquisition, and ROAS.

## Metric Governance

Each metric should include:

- Metric owner.
- Business definition.
- Grain.
- Source table.
- Calculation logic.
- Filters.
- Exclusions.
- Validation query.

These details should be documented before a metric is promoted to portfolio-ready status in Power BI.
