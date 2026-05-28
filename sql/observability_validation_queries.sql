-- Observability validation and monitoring queries for the AI-Ready Sales & Marketing Data Platform.
-- Intended for a future Fabric SQL endpoint after observability tables have been created.

-- ============================================================================
-- Latest pipeline runs
-- ============================================================================
SELECT TOP 50
    run_id,
    pipeline_name,
    layer_name,
    status,
    start_time,
    end_time,
    duration_seconds,
    rows_read,
    rows_written,
    triggered_by
FROM pipeline_run_log
ORDER BY COALESCE(end_time, start_time, created_at) DESC;

-- ============================================================================
-- Failed runs
-- ============================================================================
SELECT
    run_id,
    pipeline_name,
    layer_name,
    status,
    start_time,
    end_time,
    error_message
FROM pipeline_run_log
WHERE status = 'failed'
ORDER BY COALESCE(end_time, start_time, created_at) DESC;

-- ============================================================================
-- Failed critical checks
-- ============================================================================
SELECT
    run_id,
    layer_name,
    table_name,
    check_name,
    failed_row_count,
    dq_issue_reason,
    checked_at
FROM data_quality_results
WHERE severity = 'critical'
  AND status = 'failed'
ORDER BY checked_at DESC;

-- ============================================================================
-- Warning checks
-- ============================================================================
SELECT
    run_id,
    layer_name,
    table_name,
    check_name,
    actual_value,
    dq_issue_reason,
    checked_at
FROM data_quality_results
WHERE severity = 'warning'
  AND status IN ('failed', 'warning')
ORDER BY checked_at DESC;

-- ============================================================================
-- Dataset freshness status
-- ============================================================================
SELECT
    dataset_name,
    layer_name,
    source_system,
    expected_frequency,
    last_successful_load,
    freshness_status,
    delay_minutes,
    checked_at
FROM dataset_freshness
ORDER BY checked_at DESC, layer_name, dataset_name;

-- ============================================================================
-- Row count reconciliation failures
-- ============================================================================
SELECT
    reconciliation_id,
    run_id,
    source_layer,
    target_layer,
    source_table,
    target_table,
    source_row_count,
    target_row_count,
    row_count_difference,
    reconciliation_status,
    checked_at
FROM row_count_reconciliation
WHERE reconciliation_status <> 'matched'
ORDER BY checked_at DESC;

-- ============================================================================
-- Quality check pass rate by layer
-- ============================================================================
SELECT
    layer_name,
    COUNT(*) AS total_checks,
    SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) AS passed_checks,
    CAST(SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) AS DECIMAL(18, 4))
        / NULLIF(COUNT(*), 0) AS pass_rate
FROM data_quality_results
GROUP BY layer_name
ORDER BY layer_name;

-- ============================================================================
-- Quality check pass rate by table
-- ============================================================================
SELECT
    layer_name,
    table_name,
    COUNT(*) AS total_checks,
    SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) AS passed_checks,
    CAST(SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) AS DECIMAL(18, 4))
        / NULLIF(COUNT(*), 0) AS pass_rate
FROM data_quality_results
GROUP BY layer_name, table_name
ORDER BY layer_name, table_name;

-- ============================================================================
-- Failed check trend by date
-- ============================================================================
SELECT
    CAST(checked_at AS DATE) AS check_date,
    layer_name,
    severity,
    COUNT(*) AS failed_check_count
FROM data_quality_results
WHERE status = 'failed'
GROUP BY CAST(checked_at AS DATE), layer_name, severity
ORDER BY check_date DESC, layer_name, severity;

-- ============================================================================
-- Average pipeline duration by pipeline
-- ============================================================================
SELECT
    pipeline_name,
    layer_name,
    AVG(CAST(duration_seconds AS DECIMAL(18, 2))) AS avg_duration_seconds,
    COUNT(*) AS run_count
FROM pipeline_run_log
WHERE duration_seconds IS NOT NULL
GROUP BY pipeline_name, layer_name
ORDER BY pipeline_name, layer_name;

-- ============================================================================
-- Tables with repeated failures
-- ============================================================================
SELECT
    layer_name,
    table_name,
    check_name,
    COUNT(*) AS failed_occurrences,
    MAX(checked_at) AS latest_failure_at
FROM data_quality_results
WHERE status = 'failed'
GROUP BY layer_name, table_name, check_name
HAVING COUNT(*) >= 2
ORDER BY failed_occurrences DESC, latest_failure_at DESC;
