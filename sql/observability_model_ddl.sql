-- Representative observability model DDL for the AI-Ready Sales & Marketing Data Platform.
-- Intended as a Fabric Warehouse / SQL endpoint style reference.
-- Do not assume a production schema name; apply one during deployment if needed.

CREATE TABLE pipeline_run_log (
    run_id VARCHAR(100) NOT NULL,
    pipeline_name VARCHAR(200) NOT NULL,
    layer_name VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    start_time DATETIME2(6) NULL,
    end_time DATETIME2(6) NULL,
    duration_seconds INT NULL,
    rows_read BIGINT NULL,
    rows_written BIGINT NULL,
    error_message VARCHAR(4000) NULL,
    triggered_by VARCHAR(200) NULL,
    created_at DATETIME2(6) NOT NULL
);

CREATE TABLE data_quality_results (
    check_id VARCHAR(200) NOT NULL,
    run_id VARCHAR(100) NOT NULL,
    layer_name VARCHAR(50) NOT NULL,
    table_name VARCHAR(200) NOT NULL,
    check_name VARCHAR(200) NOT NULL,
    check_category VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    expected_value VARCHAR(500) NULL,
    actual_value VARCHAR(500) NULL,
    failed_row_count BIGINT NULL,
    dq_issue_reason VARCHAR(2000) NULL,
    checked_at DATETIME2(6) NOT NULL
);

CREATE TABLE dataset_freshness (
    dataset_name VARCHAR(200) NOT NULL,
    layer_name VARCHAR(50) NOT NULL,
    source_system VARCHAR(100) NULL,
    expected_frequency VARCHAR(100) NOT NULL,
    last_successful_load DATETIME2(6) NULL,
    freshness_status VARCHAR(50) NOT NULL,
    delay_minutes INT NULL,
    checked_at DATETIME2(6) NOT NULL
);

CREATE TABLE row_count_reconciliation (
    reconciliation_id VARCHAR(200) NOT NULL,
    run_id VARCHAR(100) NOT NULL,
    source_layer VARCHAR(50) NOT NULL,
    target_layer VARCHAR(50) NOT NULL,
    source_table VARCHAR(200) NOT NULL,
    target_table VARCHAR(200) NOT NULL,
    source_row_count BIGINT NOT NULL,
    target_row_count BIGINT NOT NULL,
    row_count_difference BIGINT NOT NULL,
    reconciliation_status VARCHAR(50) NOT NULL,
    checked_at DATETIME2(6) NOT NULL
);
