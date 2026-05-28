-- Gold validation queries for the AI-Ready Sales & Marketing Data Platform.
-- Intended for a future Fabric SQL endpoint after Gold tables have been created.

-- ============================================================================
-- Row counts by Gold table
-- ============================================================================
SELECT 'dim_customer' AS gold_table, COUNT(*) AS row_count FROM dim_customer
UNION ALL SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL SELECT 'dim_campaign', COUNT(*) FROM dim_campaign
UNION ALL SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL SELECT 'dim_customer_segment', COUNT(*) FROM dim_customer_segment
UNION ALL SELECT 'dim_channel', COUNT(*) FROM dim_channel
UNION ALL SELECT 'fact_orders', COUNT(*) FROM fact_orders
UNION ALL SELECT 'fact_ad_spend', COUNT(*) FROM fact_ad_spend
UNION ALL SELECT 'fact_support_tickets', COUNT(*) FROM fact_support_tickets;

-- ============================================================================
-- Duplicate dimension keys
-- ============================================================================
SELECT 'dim_customer' AS gold_table, customer_key AS dimension_key, COUNT(*) AS duplicate_count
FROM dim_customer
GROUP BY customer_key
HAVING COUNT(*) > 1;

SELECT 'dim_product' AS gold_table, product_key AS dimension_key, COUNT(*) AS duplicate_count
FROM dim_product
GROUP BY product_key
HAVING COUNT(*) > 1;

SELECT 'dim_campaign' AS gold_table, campaign_key AS dimension_key, COUNT(*) AS duplicate_count
FROM dim_campaign
GROUP BY campaign_key
HAVING COUNT(*) > 1;

SELECT 'dim_date' AS gold_table, date_key AS dimension_key, COUNT(*) AS duplicate_count
FROM dim_date
GROUP BY date_key
HAVING COUNT(*) > 1;

-- ============================================================================
-- Duplicate fact business keys
-- ============================================================================
SELECT 'fact_orders' AS gold_table, order_id AS business_key, COUNT(*) AS duplicate_count
FROM fact_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT 'fact_ad_spend' AS gold_table, spend_id AS business_key, COUNT(*) AS duplicate_count
FROM fact_ad_spend
GROUP BY spend_id
HAVING COUNT(*) > 1;

SELECT 'fact_support_tickets' AS gold_table, ticket_id AS business_key, COUNT(*) AS duplicate_count
FROM fact_support_tickets
GROUP BY ticket_id
HAVING COUNT(*) > 1;

-- ============================================================================
-- Null foreign keys in facts
-- ============================================================================
SELECT 'fact_orders' AS gold_table, COUNT(*) AS null_foreign_key_count
FROM fact_orders
WHERE customer_key IS NULL OR product_key IS NULL OR campaign_key IS NULL OR order_date_key IS NULL
UNION ALL
SELECT 'fact_ad_spend', COUNT(*)
FROM fact_ad_spend
WHERE campaign_key IS NULL OR channel_key IS NULL OR spend_date_key IS NULL
UNION ALL
SELECT 'fact_support_tickets', COUNT(*)
FROM fact_support_tickets
WHERE customer_key IS NULL OR created_date_key IS NULL;

-- ============================================================================
-- Unknown dimension key usage
-- ============================================================================
SELECT 'fact_orders.customer_key' AS relationship_name, COUNT(*) AS unknown_key_count
FROM fact_orders
WHERE customer_key = -1
UNION ALL
SELECT 'fact_orders.product_key', COUNT(*) FROM fact_orders WHERE product_key = -1
UNION ALL
SELECT 'fact_orders.campaign_key', COUNT(*) FROM fact_orders WHERE campaign_key = -1
UNION ALL
SELECT 'fact_ad_spend.campaign_key', COUNT(*) FROM fact_ad_spend WHERE campaign_key = -1
UNION ALL
SELECT 'fact_ad_spend.channel_key', COUNT(*) FROM fact_ad_spend WHERE channel_key = -1
UNION ALL
SELECT 'fact_support_tickets.customer_key', COUNT(*) FROM fact_support_tickets WHERE customer_key = -1;

-- ============================================================================
-- Fact-to-dimension referential checks
-- ============================================================================
SELECT 'fact_orders.customer_key' AS relationship_name, COUNT(*) AS failed_row_count
FROM fact_orders fact
LEFT JOIN dim_customer dim
    ON fact.customer_key = dim.customer_key
WHERE dim.customer_key IS NULL;

SELECT 'fact_orders.product_key' AS relationship_name, COUNT(*) AS failed_row_count
FROM fact_orders fact
LEFT JOIN dim_product dim
    ON fact.product_key = dim.product_key
WHERE dim.product_key IS NULL;

SELECT 'fact_orders.campaign_key' AS relationship_name, COUNT(*) AS failed_row_count
FROM fact_orders fact
LEFT JOIN dim_campaign dim
    ON fact.campaign_key = dim.campaign_key
WHERE dim.campaign_key IS NULL;

SELECT 'fact_ad_spend.campaign_key' AS relationship_name, COUNT(*) AS failed_row_count
FROM fact_ad_spend fact
LEFT JOIN dim_campaign dim
    ON fact.campaign_key = dim.campaign_key
WHERE dim.campaign_key IS NULL;

SELECT 'fact_support_tickets.customer_key' AS relationship_name, COUNT(*) AS failed_row_count
FROM fact_support_tickets fact
LEFT JOIN dim_customer dim
    ON fact.customer_key = dim.customer_key
WHERE dim.customer_key IS NULL;

-- ============================================================================
-- Additive measure sanity checks
-- ============================================================================
SELECT
    COUNT(*) AS order_rows,
    SUM(total_amount) AS revenue,
    SUM(net_revenue) AS net_revenue,
    SUM(gross_margin) AS gross_margin
FROM fact_orders
WHERE total_amount < 0
   OR net_revenue < 0;

SELECT
    COUNT(*) AS spend_rows,
    SUM(spend_amount) AS ad_spend,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions
FROM fact_ad_spend
WHERE spend_amount < 0
   OR impressions < 0
   OR clicks < 0
   OR conversions < 0;

-- ============================================================================
-- Date coverage checks
-- ============================================================================
SELECT 'fact_orders.order_date_key' AS date_check, COUNT(*) AS missing_date_count
FROM fact_orders fact
LEFT JOIN dim_date dim
    ON fact.order_date_key = dim.date_key
WHERE dim.date_key IS NULL
UNION ALL
SELECT 'fact_ad_spend.spend_date_key', COUNT(*)
FROM fact_ad_spend fact
LEFT JOIN dim_date dim
    ON fact.spend_date_key = dim.date_key
WHERE dim.date_key IS NULL
UNION ALL
SELECT 'fact_support_tickets.created_date_key', COUNT(*)
FROM fact_support_tickets fact
LEFT JOIN dim_date dim
    ON fact.created_date_key = dim.date_key
WHERE dim.date_key IS NULL;

-- ============================================================================
-- Silver-to-Gold row count reconciliation
-- ============================================================================
WITH silver_counts AS (
    SELECT 'orders' AS entity_name, COUNT(*) AS silver_valid_rows
    FROM silver_orders
    WHERE is_current_record = 1 AND dq_status = 'valid'
    UNION ALL
    SELECT 'ad_spend', COUNT(*)
    FROM silver_ad_spend
    WHERE is_current_record = 1 AND dq_status = 'valid'
    UNION ALL
    SELECT 'support_tickets', COUNT(*)
    FROM silver_support_tickets
    WHERE is_current_record = 1 AND dq_status = 'valid'
),
gold_counts AS (
    SELECT 'orders' AS entity_name, COUNT(*) AS gold_rows FROM fact_orders
    UNION ALL SELECT 'ad_spend', COUNT(*) FROM fact_ad_spend
    UNION ALL SELECT 'support_tickets', COUNT(*) FROM fact_support_tickets
)
SELECT
    silver_counts.entity_name,
    silver_counts.silver_valid_rows,
    gold_counts.gold_rows,
    silver_counts.silver_valid_rows - gold_counts.gold_rows AS row_count_difference
FROM silver_counts
INNER JOIN gold_counts
    ON silver_counts.entity_name = gold_counts.entity_name
ORDER BY silver_counts.entity_name;

-- ============================================================================
-- KPI sanity checks
-- ============================================================================
SELECT
    SUM(total_amount) AS revenue,
    SUM(net_revenue) AS net_revenue,
    SUM(gross_margin) AS gross_margin,
    CASE WHEN SUM(net_revenue) = 0 THEN NULL ELSE SUM(gross_margin) / SUM(net_revenue) END AS gross_margin_pct
FROM fact_orders;

SELECT
    SUM(orders.total_amount) AS revenue,
    SUM(spend.spend_amount) AS ad_spend,
    CASE WHEN SUM(spend.spend_amount) = 0 THEN NULL ELSE SUM(orders.total_amount) / SUM(spend.spend_amount) END AS roas
FROM fact_orders orders
INNER JOIN fact_ad_spend spend
    ON orders.campaign_key = spend.campaign_key;
