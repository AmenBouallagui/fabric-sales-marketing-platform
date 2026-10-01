-- Silver validation queries for the AI-Ready Sales & Marketing Data Platform.
-- These queries are intended for a future Microsoft Fabric SQL endpoint after
-- Silver Delta tables have been created.

-- ============================================================================
-- Row counts by Silver table
-- ============================================================================
SELECT 'silver_customers' AS silver_table, COUNT(*) AS row_count FROM silver_customers
UNION ALL
SELECT 'silver_products' AS silver_table, COUNT(*) AS row_count FROM silver_products
UNION ALL
SELECT 'silver_campaigns' AS silver_table, COUNT(*) AS row_count FROM silver_campaigns
UNION ALL
SELECT 'silver_orders' AS silver_table, COUNT(*) AS row_count FROM silver_orders
UNION ALL
SELECT 'silver_ad_spend' AS silver_table, COUNT(*) AS row_count FROM silver_ad_spend
UNION ALL
SELECT 'silver_support_tickets' AS silver_table, COUNT(*) AS row_count FROM silver_support_tickets;

-- ============================================================================
-- Duplicate business keys
-- ============================================================================
SELECT 'silver_customers' AS silver_table, customer_id AS business_key, COUNT(*) AS duplicate_count
FROM silver_customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT 'silver_products' AS silver_table, product_id AS business_key, COUNT(*) AS duplicate_count
FROM silver_products
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT 'silver_campaigns' AS silver_table, campaign_id AS business_key, COUNT(*) AS duplicate_count
FROM silver_campaigns
GROUP BY campaign_id
HAVING COUNT(*) > 1;

SELECT 'silver_orders' AS silver_table, order_id AS business_key, COUNT(*) AS duplicate_count
FROM silver_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT 'silver_ad_spend' AS silver_table, spend_id AS business_key, COUNT(*) AS duplicate_count
FROM silver_ad_spend
GROUP BY spend_id
HAVING COUNT(*) > 1;

SELECT 'silver_support_tickets' AS silver_table, ticket_id AS business_key, COUNT(*) AS duplicate_count
FROM silver_support_tickets
GROUP BY ticket_id
HAVING COUNT(*) > 1;

-- ============================================================================
-- Null required fields
-- ============================================================================
SELECT 'silver_customers' AS silver_table, COUNT(*) AS failed_row_count
FROM silver_customers
WHERE customer_id IS NULL OR customer_name IS NULL OR signup_date IS NULL
UNION ALL
SELECT 'silver_products' AS silver_table, COUNT(*) AS failed_row_count
FROM silver_products
WHERE product_id IS NULL OR unit_price IS NULL OR unit_cost IS NULL
UNION ALL
SELECT 'silver_campaigns' AS silver_table, COUNT(*) AS failed_row_count
FROM silver_campaigns
WHERE campaign_id IS NULL OR channel IS NULL OR campaign_start_date IS NULL
UNION ALL
SELECT 'silver_orders' AS silver_table, COUNT(*) AS failed_row_count
FROM silver_orders
WHERE order_id IS NULL OR customer_id IS NULL OR product_id IS NULL OR total_amount IS NULL OR payment_status IS NULL
UNION ALL
SELECT 'silver_ad_spend' AS silver_table, COUNT(*) AS failed_row_count
FROM silver_ad_spend
WHERE spend_id IS NULL OR campaign_id IS NULL OR spend_amount IS NULL
UNION ALL
SELECT 'silver_support_tickets' AS silver_table, COUNT(*) AS failed_row_count
FROM silver_support_tickets
WHERE ticket_id IS NULL OR customer_id IS NULL OR created_at IS NULL OR status IS NULL;

-- ============================================================================
-- Invalid monetary and numeric values
-- ============================================================================
SELECT 'silver_products' AS silver_table, COUNT(*) AS invalid_value_count
FROM silver_products
WHERE unit_price <= 0 OR unit_cost < 0
UNION ALL
SELECT 'silver_orders' AS silver_table, COUNT(*) AS invalid_value_count
FROM silver_orders
WHERE total_amount < 0 OR unit_price < 0 OR discount_amount < 0 OR tax_amount < 0 OR quantity < 0
UNION ALL
SELECT 'silver_ad_spend' AS silver_table, COUNT(*) AS invalid_value_count
FROM silver_ad_spend
WHERE spend_amount < 0 OR impressions < 0 OR clicks < 0 OR conversions < 0;

-- ============================================================================
-- Invalid categorical values
-- ============================================================================
SELECT 'silver_customers' AS silver_table, status AS invalid_value, COUNT(*) AS invalid_count
FROM silver_customers
WHERE status NOT IN ('Active', 'Inactive', 'Churned')
GROUP BY status;

SELECT 'silver_orders' AS silver_table, payment_status AS invalid_value, COUNT(*) AS invalid_count
FROM silver_orders
WHERE payment_status NOT IN ('Paid', 'Failed', 'Pending')
GROUP BY payment_status;

SELECT 'silver_campaigns' AS silver_table, channel AS invalid_value, COUNT(*) AS invalid_count
FROM silver_campaigns
WHERE channel NOT IN ('Paid Search', 'Paid Social', 'Organic', 'Email', 'Referral', 'Partner', 'Direct')
GROUP BY channel;

SELECT 'silver_support_tickets' AS silver_table, status AS invalid_value, COUNT(*) AS invalid_count
FROM silver_support_tickets
WHERE status NOT IN ('Closed', 'Resolved', 'Open', 'In Progress')
GROUP BY status;

-- ============================================================================
-- Referential integrity failures
-- ============================================================================
SELECT 'silver_orders.customer_id' AS relationship_name, COUNT(*) AS failed_row_count
FROM silver_orders orders
LEFT JOIN silver_customers customers
    ON orders.customer_id = customers.customer_id
WHERE customers.customer_id IS NULL;

SELECT 'silver_orders.product_id' AS relationship_name, COUNT(*) AS failed_row_count
FROM silver_orders orders
LEFT JOIN silver_products products
    ON orders.product_id = products.product_id
WHERE products.product_id IS NULL;

SELECT 'silver_orders.campaign_id' AS relationship_name, COUNT(*) AS failed_row_count
FROM silver_orders orders
LEFT JOIN silver_campaigns campaigns
    ON orders.campaign_id = campaigns.campaign_id
WHERE orders.campaign_id IS NOT NULL
  AND campaigns.campaign_id IS NULL;

SELECT 'silver_ad_spend.campaign_id' AS relationship_name, COUNT(*) AS failed_row_count
FROM silver_ad_spend ad_spend
LEFT JOIN silver_campaigns campaigns
    ON ad_spend.campaign_id = campaigns.campaign_id
WHERE campaigns.campaign_id IS NULL;

SELECT 'silver_support_tickets.customer_id' AS relationship_name, COUNT(*) AS failed_row_count
FROM silver_support_tickets tickets
LEFT JOIN silver_customers customers
    ON tickets.customer_id = customers.customer_id
WHERE customers.customer_id IS NULL;

-- ============================================================================
-- Latest silver_processed_at by table
-- ============================================================================
SELECT 'silver_customers' AS silver_table, MAX(silver_processed_at) AS latest_silver_processed_at FROM silver_customers
UNION ALL
SELECT 'silver_products' AS silver_table, MAX(silver_processed_at) AS latest_silver_processed_at FROM silver_products
UNION ALL
SELECT 'silver_campaigns' AS silver_table, MAX(silver_processed_at) AS latest_silver_processed_at FROM silver_campaigns
UNION ALL
SELECT 'silver_orders' AS silver_table, MAX(silver_processed_at) AS latest_silver_processed_at FROM silver_orders
UNION ALL
SELECT 'silver_ad_spend' AS silver_table, MAX(silver_processed_at) AS latest_silver_processed_at FROM silver_ad_spend
UNION ALL
SELECT 'silver_support_tickets' AS silver_table, MAX(silver_processed_at) AS latest_silver_processed_at FROM silver_support_tickets;

-- ============================================================================
-- dq_status distribution by table
-- ============================================================================
SELECT 'silver_customers' AS silver_table, dq_status, COUNT(*) AS row_count
FROM silver_customers
GROUP BY dq_status
UNION ALL
SELECT 'silver_products' AS silver_table, dq_status, COUNT(*) AS row_count
FROM silver_products
GROUP BY dq_status
UNION ALL
SELECT 'silver_campaigns' AS silver_table, dq_status, COUNT(*) AS row_count
FROM silver_campaigns
GROUP BY dq_status
UNION ALL
SELECT 'silver_orders' AS silver_table, dq_status, COUNT(*) AS row_count
FROM silver_orders
GROUP BY dq_status
UNION ALL
SELECT 'silver_ad_spend' AS silver_table, dq_status, COUNT(*) AS row_count
FROM silver_ad_spend
GROUP BY dq_status
UNION ALL
SELECT 'silver_support_tickets' AS silver_table, dq_status, COUNT(*) AS row_count
FROM silver_support_tickets
GROUP BY dq_status
ORDER BY silver_table, dq_status;

-- ============================================================================
-- Simple Bronze-to-Silver row count comparison
-- ============================================================================
WITH bronze_counts AS (
    SELECT 'customers' AS entity_name, COUNT(DISTINCT customer_id) AS bronze_distinct_keys FROM bronze_customers_raw
    UNION ALL SELECT 'products', COUNT(DISTINCT product_id) FROM bronze_products_raw
    UNION ALL SELECT 'campaigns', COUNT(DISTINCT campaign_id) FROM bronze_campaigns_raw
    UNION ALL SELECT 'orders', COUNT(DISTINCT order_id) FROM bronze_orders_raw
    UNION ALL SELECT 'ad_spend', COUNT(DISTINCT spend_id) FROM bronze_ad_spend_raw
    UNION ALL SELECT 'support_tickets', COUNT(DISTINCT ticket_id) FROM bronze_support_tickets_raw
),
silver_counts AS (
    SELECT 'customers' AS entity_name, COUNT(*) AS silver_rows FROM silver_customers
    UNION ALL SELECT 'products', COUNT(*) FROM silver_products
    UNION ALL SELECT 'campaigns', COUNT(*) FROM silver_campaigns
    UNION ALL SELECT 'orders', COUNT(*) FROM silver_orders
    UNION ALL SELECT 'ad_spend', COUNT(*) FROM silver_ad_spend
    UNION ALL SELECT 'support_tickets', COUNT(*) FROM silver_support_tickets
)
SELECT
    bronze_counts.entity_name,
    bronze_counts.bronze_distinct_keys,
    silver_counts.silver_rows,
    bronze_counts.bronze_distinct_keys - silver_counts.silver_rows AS key_count_difference
FROM bronze_counts
INNER JOIN silver_counts
    ON bronze_counts.entity_name = silver_counts.entity_name
ORDER BY bronze_counts.entity_name;
