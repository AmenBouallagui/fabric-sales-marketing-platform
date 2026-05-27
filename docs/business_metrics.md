# Business Metrics

## Purpose

This document defines the first set of sales and marketing metrics for the Power BI semantic model. Definitions should remain consistent across SQL, notebooks, and report visuals.

## Sales Metrics

- Pipeline value: total open opportunity amount.
- Weighted pipeline: opportunity amount multiplied by probability.
- Closed won revenue: total value of opportunities with a closed won status.
- Win rate: closed won opportunities divided by all closed opportunities.
- Average deal size: closed won revenue divided by count of won opportunities.
- Sales cycle length: days between opportunity created date and close date.
- Forecasted revenue: expected revenue based on open opportunities and probability.

## Marketing Metrics

- Campaign spend: total budget or actual spend assigned to campaigns.
- Marketing generated leads: leads sourced from marketing campaigns.
- Lead conversion rate: converted leads divided by total leads.
- Cost per lead: campaign spend divided by generated leads.
- Campaign influenced pipeline: open and closed opportunity value linked to campaign-sourced or campaign-influenced leads.
- Engagement rate: interactions divided by reachable contacts or delivered messages, depending on channel.

## Customer Metrics

- Revenue by segment: booked revenue grouped by customer segment.
- Revenue by region: booked revenue grouped by sales region.
- Product mix: revenue share by product category.
- Account penetration: number of active products or opportunities per account.

## Metric Governance

Each metric should include a definition, grain, filters, exclusions, and owner before being promoted to portfolio-ready status.
