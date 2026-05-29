-- Representative business metric preview queries for the AI-Ready Sales & Marketing Data Platform.
-- These queries are intended for validating or previewing Power BI measures from Gold tables.

-- ============================================================================
-- Revenue by month
-- ============================================================================
SELECT
    dates.calendar_year,
    dates.calendar_month,
    dates.month_name,
    SUM(orders.total_amount) AS revenue,
    SUM(orders.net_revenue) AS net_revenue
FROM fact_orders orders
INNER JOIN dim_date dates
    ON orders.order_date_key = dates.date_key
GROUP BY dates.calendar_year, dates.calendar_month, dates.month_name
ORDER BY dates.calendar_year, dates.calendar_month;

-- ============================================================================
-- Gross margin by product category
-- ============================================================================
SELECT
    product.category,
    SUM(orders.net_revenue) AS net_revenue,
    SUM(orders.gross_margin) AS gross_margin,
    CASE
        WHEN SUM(orders.net_revenue) = 0 THEN NULL
        ELSE SUM(orders.gross_margin) / SUM(orders.net_revenue)
    END AS gross_margin_pct
FROM fact_orders orders
INNER JOIN dim_product product
    ON orders.product_key = product.product_key
GROUP BY product.category
ORDER BY gross_margin DESC;

-- ============================================================================
-- ROAS by campaign
-- ============================================================================
SELECT
    campaign.campaign_name,
    SUM(orders.total_amount) AS revenue,
    SUM(spend.spend_amount) AS ad_spend,
    CASE
        WHEN SUM(spend.spend_amount) = 0 THEN NULL
        ELSE SUM(orders.total_amount) / SUM(spend.spend_amount)
    END AS roas
FROM dim_campaign campaign
LEFT JOIN fact_orders orders
    ON campaign.campaign_key = orders.campaign_key
LEFT JOIN fact_ad_spend spend
    ON campaign.campaign_key = spend.campaign_key
GROUP BY campaign.campaign_name
ORDER BY roas DESC;

-- ============================================================================
-- Ad spend and conversions by channel
-- ============================================================================
SELECT
    channel.channel,
    SUM(spend.spend_amount) AS ad_spend,
    SUM(spend.impressions) AS impressions,
    SUM(spend.clicks) AS clicks,
    SUM(spend.conversions) AS conversions,
    CASE
        WHEN SUM(spend.clicks) = 0 THEN NULL
        ELSE CAST(SUM(spend.conversions) AS DECIMAL(18, 4)) / SUM(spend.clicks)
    END AS conversion_rate
FROM fact_ad_spend spend
INNER JOIN dim_channel channel
    ON spend.channel_key = channel.channel_key
GROUP BY channel.channel
ORDER BY ad_spend DESC;

-- ============================================================================
-- Customer count by segment
-- ============================================================================
SELECT
    customer.customer_segment,
    COUNT(DISTINCT customer.customer_id) AS customers
FROM dim_customer customer
GROUP BY customer.customer_segment
ORDER BY customers DESC;

-- ============================================================================
-- Support ticket count and average satisfaction by status
-- ============================================================================
SELECT
    tickets.status,
    COUNT(DISTINCT tickets.ticket_id) AS ticket_count,
    AVG(tickets.satisfaction_score) AS average_satisfaction_score
FROM fact_support_tickets tickets
GROUP BY tickets.status
ORDER BY ticket_count DESC;

-- ============================================================================
-- Data quality failed checks by layer, if observability tables exist
-- ============================================================================
SELECT
    layer_name,
    severity,
    COUNT(*) AS failed_checks
FROM data_quality_results
WHERE status = 'failed'
GROUP BY layer_name, severity
ORDER BY failed_checks DESC;

-- ============================================================================
-- Latest pipeline run status, if observability tables exist
-- ============================================================================
SELECT TOP 20
    run_id,
    pipeline_name,
    layer_name,
    status,
    start_time,
    end_time,
    duration_seconds,
    rows_read,
    rows_written
FROM pipeline_run_log
ORDER BY COALESCE(end_time, start_time, created_at) DESC;
