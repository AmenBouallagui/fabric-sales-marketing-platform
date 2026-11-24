-- Current dbt marts; DuckDB and Snowflake. Sales = Paid and not refunded.
-- Revenue includes tax; net_revenue excludes it. See docs/business_metrics.md.

-- Revenue by month
SELECT d.calendar_year, d.calendar_month, d.month_name,
       SUM(o.total_amount) AS revenue, SUM(o.net_revenue) AS net_revenue
FROM marts.fct_orders o
JOIN marts.dim_date d ON o.order_date_key = d.date_key
WHERE o.payment_status = 'Paid' AND o.refund_flag = false
GROUP BY d.calendar_year, d.calendar_month, d.month_name
ORDER BY d.calendar_year, d.calendar_month;

-- Gross margin by product category; unknown costs invalidate the group margin.
SELECT p.category, SUM(o.net_revenue) AS net_revenue,
       CASE WHEN COUNT(*) = COUNT(o.estimated_cost) THEN SUM(o.gross_margin) END AS gross_margin,
       CASE WHEN COUNT(*) = COUNT(o.estimated_cost)
            THEN SUM(o.gross_margin) / NULLIF(SUM(o.net_revenue), 0) END AS gross_margin_pct
FROM marts.fct_orders o
JOIN marts.dim_product p ON o.product_key = p.product_key
WHERE o.payment_status = 'Paid' AND o.refund_flag = false
GROUP BY p.category
ORDER BY gross_margin DESC;

-- ROAS by campaign: aggregate each fact first to prevent many-to-many fanout.
WITH campaign_revenue AS (
    SELECT campaign_key, SUM(total_amount) AS revenue
    FROM marts.fct_orders
    WHERE payment_status = 'Paid' AND refund_flag = false
    GROUP BY campaign_key
), campaign_spend AS (
    SELECT campaign_key, SUM(spend_amount) AS ad_spend
    FROM marts.fct_ad_spend
    GROUP BY campaign_key
)
SELECT c.campaign_key, c.campaign_name, c.channel,
       COALESCE(r.revenue, 0) AS revenue, COALESCE(s.ad_spend, 0) AS ad_spend,
       COALESCE(r.revenue, 0) / NULLIF(s.ad_spend, 0) AS roas
FROM marts.dim_campaign c
LEFT JOIN campaign_revenue r ON c.campaign_key = r.campaign_key
LEFT JOIN campaign_spend s ON c.campaign_key = s.campaign_key
WHERE c.campaign_id <> 'UNKNOWN'
ORDER BY roas DESC;

-- Ad spend and conversions by channel (spend's recorded channel).
SELECT c.channel, SUM(s.spend_amount) AS ad_spend,
       SUM(s.impressions) AS impressions, SUM(s.clicks) AS clicks,
       SUM(s.conversions) AS conversions,
       CAST(SUM(s.conversions) AS DOUBLE) / NULLIF(SUM(s.clicks), 0) AS conversion_rate
FROM marts.fct_ad_spend s
JOIN marts.dim_channel c ON s.channel_key = c.channel_key
GROUP BY c.channel
ORDER BY ad_spend DESC;

-- Registered customers, excluding the unknown member; not a buyer count.
SELECT customer_segment, COUNT(DISTINCT customer_id) AS customers
FROM marts.dim_customer
WHERE customer_id <> 'UNKNOWN'
GROUP BY customer_segment
ORDER BY customers DESC;

-- Support: all statuses; null satisfaction scores are excluded by AVG.
SELECT status, COUNT(DISTINCT ticket_id) AS ticket_count,
       AVG(satisfaction_score) AS average_satisfaction_score
FROM marts.fct_support_tickets
GROUP BY status
ORDER BY ticket_count DESC;

-- Seeded demonstration operations data, not current CI results.
SELECT layer_name, severity, COUNT(*) AS failed_checks
FROM observability.data_quality_results
WHERE status = 'failed'
GROUP BY layer_name, severity
ORDER BY failed_checks DESC;

SELECT run_id, pipeline_name, layer_name, status, start_time, end_time,
       duration_seconds, rows_read, rows_written
FROM observability.pipeline_run_log
ORDER BY COALESCE(end_time, start_time) DESC
LIMIT 20;
