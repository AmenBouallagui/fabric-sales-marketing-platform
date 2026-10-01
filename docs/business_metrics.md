# Business metrics

These definitions apply to the committed Power BI model and [SQL validation queries](../sql/business_metric_queries.sql). Fact tables retain all valid orders for audit; sales KPIs count only **Paid orders with refund_flag = false**. This is a demonstration convention, not an accounting ledger or partial-refund model.

| Measure | Definition and filter |
| --- | --- |
| Revenue | Sum of total_amount for eligible orders; includes tax |
| Net Revenue | Sum of total_amount minus tax for eligible orders |
| Estimated Cost | Quantity × product unit_cost for eligible orders; blank if any eligible order lacks cost |
| Gross Margin | Net Revenue minus Estimated Cost; blank if cost is incomplete |
| Gross Margin % | Gross Margin / Net Revenue |
| Orders | Distinct eligible order_id |
| Average Order Value | Revenue / Orders |
| Customers | Registered dim_customer members, excluding UNKNOWN; not a count of buyers |
| New Customers | Registered customers whose signup_date is in the selected calendar period; excludes UNKNOWN |
| Ad Spend / Impressions / Clicks / Conversions | Sum of corresponding fct_ad_spend columns |
| Click-Through Rate | Clicks / Impressions |
| Conversion Rate | Conversions / Clicks |
| Cost Per Click / Acquisition | Ad Spend / Clicks or Conversions |
| ROAS | Eligible order revenue for known campaigns / spend for those campaigns; selected channel filters campaigns by their configured channel |
| Ticket Count | Distinct ticket_id, all statuses |
| Avg First Response / Resolution / Satisfaction | Average of the respective support fact column; null values excluded |

Ratios return blank for zero denominators. Campaign attribution uses the campaign_id carried by the source order; it is not multi-touch attribution. Channel-filtered ROAS uses dim_campaign.channel for both numerator and denominator, rather than inferring revenue from spend rows. Paid sales without a known campaign remain in Revenue but are excluded from ROAS.

Operations measures count seeded demonstration runs/checks and reconciliation statuses. They do not describe current CI health. The [build guide](../powerbi/report_build_guide.md) lists the report pages; [quality documentation](data_quality_observability.md) distinguishes implemented monitoring from planned controls.
