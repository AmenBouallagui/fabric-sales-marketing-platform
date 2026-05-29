# Report Design

## Executive Overview

### Purpose

Provide a concise summary of revenue, margin, marketing efficiency, support health, and data freshness.

### Main Visuals

- KPI cards for Revenue, Net Revenue, Gross Margin %, ROAS, Ticket Count, and Average Satisfaction Score.
- Revenue trend by month.
- Revenue and Ad Spend comparison.
- Data health status strip.

### Key Measures

- Revenue.
- Net Revenue.
- Gross Margin %.
- ROAS.
- Ticket Count.
- Average Satisfaction Score.

### Suggested Slicers

- Date range.
- Customer segment.
- Channel.
- Product category.

### Reviewer Talking Points

- The page shows the business-facing value of the Gold model.
- Metrics come from curated facts and dimensions, not raw extracts.
- Data health indicators make trust visible.

## Revenue & Margin

### Purpose

Show order performance, margin, and product contribution.

### Main Visuals

- Revenue and Net Revenue by month.
- Gross Margin by product category.
- Average Order Value by customer segment.
- Order detail table.

### Key Measures

- Revenue.
- Net Revenue.
- Gross Margin.
- Gross Margin %.
- Average Order Value.
- Orders.

### Suggested Slicers

- Date range.
- Product category.
- Plan tier.
- Customer segment.

### Reviewer Talking Points

- Margin uses Gold calculated fields from order and product cost data.
- Date filtering is driven by `dim_date`.
- Product and segment slicing comes from conformed dimensions.

## Marketing Performance

### Purpose

Evaluate campaign and channel efficiency.

### Main Visuals

- ROAS by campaign.
- Ad Spend, Clicks, and Conversions by channel.
- Conversion Rate trend.
- Cost Per Click and Cost Per Acquisition cards.

### Key Measures

- Ad Spend.
- Impressions.
- Clicks.
- Conversions.
- Conversion Rate.
- Cost Per Click.
- Cost Per Acquisition.
- ROAS.

### Suggested Slicers

- Date range.
- Channel.
- Campaign.
- Target segment.

### Reviewer Talking Points

- Campaign and spend data use shared campaign and channel dimensions.
- Ratio measures should use divide-by-zero safe logic.
- Channel filtering supports both acquisition and campaign analysis.

## Customer & Segment Analysis

### Purpose

Understand customer mix and segment behavior.

### Main Visuals

- Customer count by segment.
- Revenue by segment.
- New Customers by month.
- Customer geography table or map-ready summary.

### Key Measures

- Customers.
- New Customers.
- Revenue.
- Average Order Value.
- Ticket Count.

### Suggested Slicers

- Date range.
- Customer segment.
- Country.
- Industry.
- Acquisition channel.

### Reviewer Talking Points

- Customer attributes are centralized in `dim_customer`.
- Segment can be analyzed through both customer and segment dimensions.
- Customer KPIs can connect commercial and service outcomes.

## Product Performance

### Purpose

Show how products contribute to revenue and margin.

### Main Visuals

- Revenue by product category.
- Gross Margin by plan tier.
- Orders by product.
- Product detail matrix.

### Key Measures

- Revenue.
- Net Revenue.
- Gross Margin.
- Gross Margin %.
- Orders.

### Suggested Slicers

- Date range.
- Product category.
- Plan tier.
- Subscription flag.

### Reviewer Talking Points

- Product attributes are managed in `dim_product`.
- Product cost supports margin analysis.
- The model can show both product mix and profitability.

## Support Quality

### Purpose

Monitor service quality and customer support outcomes.

### Main Visuals

- Ticket Count by status.
- Average First Response Minutes by priority.
- Average Resolution Minutes by category.
- Average Satisfaction Score trend.

### Key Measures

- Ticket Count.
- Average First Response Minutes.
- Average Resolution Minutes.
- Average Satisfaction Score.

### Suggested Slicers

- Date range.
- Priority.
- Category.
- Status.
- Customer segment.

### Reviewer Talking Points

- Support facts connect to customer attributes.
- Response and resolution metrics show operational quality.
- Satisfaction can be viewed by customer segment or support category.

## Operations / Data Health

### Purpose

Show platform reliability and data trust signals.

### Main Visuals

- Pipeline success rate.
- Failed critical checks.
- Warning checks.
- Freshness status by dataset.
- Row count reconciliation failures.
- Tables with repeated failures.

### Key Measures

- Pipeline Success Rate.
- Failed Checks.
- Failed Critical Checks.
- Warning Checks.
- Freshness Status Count.
- Row Count Difference.

### Suggested Slicers

- Date range.
- Layer.
- Table.
- Severity.
- Pipeline name.

### Reviewer Talking Points

- Observability data makes platform readiness visible.
- Critical failures should block downstream publication in future orchestration.
- The dashboard complements business reporting with operational trust.
