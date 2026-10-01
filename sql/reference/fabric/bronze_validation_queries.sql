-- Bronze validation queries for the AI-Ready Sales & Marketing Data Platform.
-- These queries are intended for a future Microsoft Fabric SQL endpoint after
-- Bronze Delta tables have been created.

-- ============================================================================
-- Row counts by Bronze table
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, COUNT(*) AS row_count FROM bronze_customers_raw
UNION ALL
SELECT 'bronze_products_raw' AS bronze_table, COUNT(*) AS row_count FROM bronze_products_raw
UNION ALL
SELECT 'bronze_campaigns_raw' AS bronze_table, COUNT(*) AS row_count FROM bronze_campaigns_raw
UNION ALL
SELECT 'bronze_orders_raw' AS bronze_table, COUNT(*) AS row_count FROM bronze_orders_raw
UNION ALL
SELECT 'bronze_ad_spend_raw' AS bronze_table, COUNT(*) AS row_count FROM bronze_ad_spend_raw
UNION ALL
SELECT 'bronze_support_tickets_raw' AS bronze_table, COUNT(*) AS row_count FROM bronze_support_tickets_raw;

-- ============================================================================
-- Duplicate source IDs
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, customer_id AS source_id, COUNT(*) AS duplicate_count
FROM bronze_customers_raw
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT 'bronze_products_raw' AS bronze_table, product_id AS source_id, COUNT(*) AS duplicate_count
FROM bronze_products_raw
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT 'bronze_campaigns_raw' AS bronze_table, campaign_id AS source_id, COUNT(*) AS duplicate_count
FROM bronze_campaigns_raw
GROUP BY campaign_id
HAVING COUNT(*) > 1;

SELECT 'bronze_orders_raw' AS bronze_table, order_id AS source_id, COUNT(*) AS duplicate_count
FROM bronze_orders_raw
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT 'bronze_ad_spend_raw' AS bronze_table, spend_id AS source_id, COUNT(*) AS duplicate_count
FROM bronze_ad_spend_raw
GROUP BY spend_id
HAVING COUNT(*) > 1;

SELECT 'bronze_support_tickets_raw' AS bronze_table, ticket_id AS source_id, COUNT(*) AS duplicate_count
FROM bronze_support_tickets_raw
GROUP BY ticket_id
HAVING COUNT(*) > 1;

-- ============================================================================
-- Null primary keys
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, COUNT(*) AS null_primary_key_count
FROM bronze_customers_raw
WHERE customer_id IS NULL;

SELECT 'bronze_products_raw' AS bronze_table, COUNT(*) AS null_primary_key_count
FROM bronze_products_raw
WHERE product_id IS NULL;

SELECT 'bronze_campaigns_raw' AS bronze_table, COUNT(*) AS null_primary_key_count
FROM bronze_campaigns_raw
WHERE campaign_id IS NULL;

SELECT 'bronze_orders_raw' AS bronze_table, COUNT(*) AS null_primary_key_count
FROM bronze_orders_raw
WHERE order_id IS NULL;

SELECT 'bronze_ad_spend_raw' AS bronze_table, COUNT(*) AS null_primary_key_count
FROM bronze_ad_spend_raw
WHERE spend_id IS NULL;

SELECT 'bronze_support_tickets_raw' AS bronze_table, COUNT(*) AS null_primary_key_count
FROM bronze_support_tickets_raw
WHERE ticket_id IS NULL;

-- ============================================================================
-- Null source_updated_at values
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, COUNT(*) AS null_source_updated_at_count
FROM bronze_customers_raw
WHERE source_updated_at IS NULL
UNION ALL
SELECT 'bronze_products_raw' AS bronze_table, COUNT(*) AS null_source_updated_at_count
FROM bronze_products_raw
WHERE source_updated_at IS NULL
UNION ALL
SELECT 'bronze_campaigns_raw' AS bronze_table, COUNT(*) AS null_source_updated_at_count
FROM bronze_campaigns_raw
WHERE source_updated_at IS NULL
UNION ALL
SELECT 'bronze_orders_raw' AS bronze_table, COUNT(*) AS null_source_updated_at_count
FROM bronze_orders_raw
WHERE source_updated_at IS NULL
UNION ALL
SELECT 'bronze_ad_spend_raw' AS bronze_table, COUNT(*) AS null_source_updated_at_count
FROM bronze_ad_spend_raw
WHERE source_updated_at IS NULL
UNION ALL
SELECT 'bronze_support_tickets_raw' AS bronze_table, COUNT(*) AS null_source_updated_at_count
FROM bronze_support_tickets_raw
WHERE source_updated_at IS NULL;

-- ============================================================================
-- Max source_updated_at by table
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, MAX(source_updated_at) AS max_source_updated_at FROM bronze_customers_raw
UNION ALL
SELECT 'bronze_products_raw' AS bronze_table, MAX(source_updated_at) AS max_source_updated_at FROM bronze_products_raw
UNION ALL
SELECT 'bronze_campaigns_raw' AS bronze_table, MAX(source_updated_at) AS max_source_updated_at FROM bronze_campaigns_raw
UNION ALL
SELECT 'bronze_orders_raw' AS bronze_table, MAX(source_updated_at) AS max_source_updated_at FROM bronze_orders_raw
UNION ALL
SELECT 'bronze_ad_spend_raw' AS bronze_table, MAX(source_updated_at) AS max_source_updated_at FROM bronze_ad_spend_raw
UNION ALL
SELECT 'bronze_support_tickets_raw' AS bronze_table, MAX(source_updated_at) AS max_source_updated_at FROM bronze_support_tickets_raw;

-- ============================================================================
-- Records by load_date
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, load_date, COUNT(*) AS row_count
FROM bronze_customers_raw
GROUP BY load_date
UNION ALL
SELECT 'bronze_products_raw' AS bronze_table, load_date, COUNT(*) AS row_count
FROM bronze_products_raw
GROUP BY load_date
UNION ALL
SELECT 'bronze_campaigns_raw' AS bronze_table, load_date, COUNT(*) AS row_count
FROM bronze_campaigns_raw
GROUP BY load_date
UNION ALL
SELECT 'bronze_orders_raw' AS bronze_table, load_date, COUNT(*) AS row_count
FROM bronze_orders_raw
GROUP BY load_date
UNION ALL
SELECT 'bronze_ad_spend_raw' AS bronze_table, load_date, COUNT(*) AS row_count
FROM bronze_ad_spend_raw
GROUP BY load_date
UNION ALL
SELECT 'bronze_support_tickets_raw' AS bronze_table, load_date, COUNT(*) AS row_count
FROM bronze_support_tickets_raw
GROUP BY load_date
ORDER BY bronze_table, load_date;

-- ============================================================================
-- Records by ingestion_run_id
-- ============================================================================
SELECT 'bronze_customers_raw' AS bronze_table, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_customers_raw
GROUP BY ingestion_run_id
UNION ALL
SELECT 'bronze_products_raw' AS bronze_table, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_products_raw
GROUP BY ingestion_run_id
UNION ALL
SELECT 'bronze_campaigns_raw' AS bronze_table, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_campaigns_raw
GROUP BY ingestion_run_id
UNION ALL
SELECT 'bronze_orders_raw' AS bronze_table, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_orders_raw
GROUP BY ingestion_run_id
UNION ALL
SELECT 'bronze_ad_spend_raw' AS bronze_table, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_ad_spend_raw
GROUP BY ingestion_run_id
UNION ALL
SELECT 'bronze_support_tickets_raw' AS bronze_table, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_support_tickets_raw
GROUP BY ingestion_run_id
ORDER BY bronze_table, ingestion_run_id;

-- ============================================================================
-- Source file metadata completeness
-- ============================================================================
SELECT entity_name, source_system, source_file_name, source_file_path, load_date, ingestion_run_id, COUNT(*) AS row_count
FROM bronze_orders_raw
GROUP BY entity_name, source_system, source_file_name, source_file_path, load_date, ingestion_run_id
ORDER BY load_date, ingestion_run_id, source_file_name;

-- ============================================================================
-- Simple reconciliation between expected entities and Bronze tables
-- ============================================================================
WITH expected_entities AS (
    SELECT 'customers' AS entity_name, 'bronze_customers_raw' AS bronze_table
    UNION ALL SELECT 'products', 'bronze_products_raw'
    UNION ALL SELECT 'campaigns', 'bronze_campaigns_raw'
    UNION ALL SELECT 'orders', 'bronze_orders_raw'
    UNION ALL SELECT 'ad_spend', 'bronze_ad_spend_raw'
    UNION ALL SELECT 'support_tickets', 'bronze_support_tickets_raw'
),
actual_counts AS (
    SELECT 'customers' AS entity_name, COUNT(*) AS row_count FROM bronze_customers_raw
    UNION ALL SELECT 'products', COUNT(*) FROM bronze_products_raw
    UNION ALL SELECT 'campaigns', COUNT(*) FROM bronze_campaigns_raw
    UNION ALL SELECT 'orders', COUNT(*) FROM bronze_orders_raw
    UNION ALL SELECT 'ad_spend', COUNT(*) FROM bronze_ad_spend_raw
    UNION ALL SELECT 'support_tickets', COUNT(*) FROM bronze_support_tickets_raw
)
SELECT
    expected_entities.entity_name,
    expected_entities.bronze_table,
    COALESCE(actual_counts.row_count, 0) AS row_count,
    CASE
        WHEN actual_counts.row_count IS NULL THEN 'MISSING'
        WHEN actual_counts.row_count = 0 THEN 'EMPTY'
        ELSE 'LOADED'
    END AS load_status
FROM expected_entities
LEFT JOIN actual_counts
    ON expected_entities.entity_name = actual_counts.entity_name
ORDER BY expected_entities.entity_name;
