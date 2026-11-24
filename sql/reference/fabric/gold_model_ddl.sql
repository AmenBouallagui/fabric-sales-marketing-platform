-- Representative Gold model DDL for the AI-Ready Sales & Marketing Data Platform.
-- Intended as a Fabric Warehouse / SQL endpoint style reference.
-- Do not assume a production schema name; apply one during deployment if needed.

-- ============================================================================
-- Dimensions
-- ============================================================================

CREATE TABLE dim_customer (
    customer_key BIGINT NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(255) NULL,
    email VARCHAR(255) NULL,
    country VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    customer_segment VARCHAR(100) NULL,
    company_size VARCHAR(50) NULL,
    industry VARCHAR(150) NULL,
    acquisition_channel VARCHAR(100) NULL,
    status VARCHAR(50) NULL,
    signup_date DATE NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE dim_product (
    product_key BIGINT NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NULL,
    category VARCHAR(100) NULL,
    plan_tier VARCHAR(100) NULL,
    unit_price DECIMAL(18, 2) NULL,
    unit_cost DECIMAL(18, 2) NULL,
    is_subscription BIT NULL,
    valid_from DATE NULL,
    valid_to DATE NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE dim_campaign (
    campaign_key BIGINT NOT NULL,
    campaign_id VARCHAR(50) NOT NULL,
    campaign_name VARCHAR(255) NULL,
    channel VARCHAR(100) NULL,
    campaign_start_date DATE NULL,
    campaign_end_date DATE NULL,
    target_segment VARCHAR(100) NULL,
    objective VARCHAR(100) NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE dim_date (
    date_key INT NOT NULL,
    calendar_date DATE NOT NULL,
    calendar_year INT NOT NULL,
    calendar_quarter INT NOT NULL,
    calendar_month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    is_weekend BIT NOT NULL,
    month_start_date DATE NULL,
    month_end_date DATE NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE dim_customer_segment (
    customer_segment_key BIGINT NOT NULL,
    customer_segment VARCHAR(100) NOT NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE dim_channel (
    channel_key BIGINT NOT NULL,
    channel VARCHAR(100) NOT NULL,
    channel_group VARCHAR(100) NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

-- ============================================================================
-- Facts
-- ============================================================================

CREATE TABLE fact_orders (
    order_key BIGINT NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    campaign_key BIGINT NOT NULL,
    order_date_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(18, 2) NOT NULL,
    discount_amount DECIMAL(18, 2) NOT NULL,
    tax_amount DECIMAL(18, 2) NOT NULL,
    total_amount DECIMAL(18, 2) NOT NULL,
    net_revenue DECIMAL(18, 2) NOT NULL,
    estimated_cost DECIMAL(18, 2) NULL,
    gross_margin DECIMAL(18, 2) NULL,
    payment_status VARCHAR(50) NULL,
    refund_flag BIT NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE fact_ad_spend (
    ad_spend_key BIGINT NOT NULL,
    spend_id VARCHAR(50) NOT NULL,
    campaign_key BIGINT NOT NULL,
    channel_key BIGINT NOT NULL,
    spend_date_key INT NOT NULL,
    impressions BIGINT NOT NULL,
    clicks BIGINT NOT NULL,
    conversions BIGINT NOT NULL,
    spend_amount DECIMAL(18, 2) NOT NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);

CREATE TABLE fact_support_tickets (
    ticket_key BIGINT NOT NULL,
    ticket_id VARCHAR(50) NOT NULL,
    customer_key BIGINT NOT NULL,
    created_date_key INT NOT NULL,
    closed_date_key INT NULL,
    priority VARCHAR(50) NULL,
    category VARCHAR(100) NULL,
    status VARCHAR(50) NULL,
    satisfaction_score DECIMAL(5, 2) NULL,
    first_response_minutes INT NULL,
    resolution_minutes INT NULL,
    gold_processed_at DATETIME2(6) NOT NULL
);
