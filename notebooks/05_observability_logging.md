# 05 Observability Logging Notebook Plan

## Objective

Design a future Microsoft Fabric notebook that creates or updates observability tables, logs pipeline run status, records dataset freshness, writes row count reconciliation results, and captures concise error information for operational monitoring.

This Markdown file is a notebook implementation plan. It is not an executable `.ipynb` artifact yet.

## Parameters

Planned notebook parameters:

- `run_id`: unique execution identifier.
- `pipeline_name`: pipeline or notebook workflow name.
- `layer_name`: target layer, such as `bronze`, `silver`, or `gold`.
- `status`: `running`, `succeeded`, `failed`, or `completed_with_warnings`.
- `start_time`: run start timestamp.
- `end_time`: run end timestamp.
- `rows_read`: optional count of rows read.
- `rows_written`: optional count of rows written.
- `error_message`: optional concise error text.
- `triggered_by`: run trigger source.

## Observability Table Creation Or Upsert Strategy

The future implementation should create observability tables if they do not exist and then use append or merge patterns depending on table behavior.

- `pipeline_run_log`: upsert by `run_id`.
- `data_quality_results`: append one row per check result.
- `dataset_freshness`: upsert by dataset, layer, and check timestamp pattern.
- `row_count_reconciliation`: append one row per reconciliation check.

## Pipeline Run Logging

```python
def log_pipeline_run(
    run_id: str,
    pipeline_name: str,
    layer_name: str,
    status: str,
    start_time,
    end_time,
    rows_read: int | None,
    rows_written: int | None,
    error_message: str | None,
    triggered_by: str,
):
    duration_seconds = None
    if start_time and end_time:
        duration_seconds = int((end_time - start_time).total_seconds())

    row = [{
        "run_id": run_id,
        "pipeline_name": pipeline_name,
        "layer_name": layer_name,
        "status": status,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration_seconds,
        "rows_read": rows_read,
        "rows_written": rows_written,
        "error_message": error_message,
        "triggered_by": triggered_by,
        "created_at": datetime.now(timezone.utc),
    }]

    spark.createDataFrame(row).write.mode("append").saveAsTable("pipeline_run_log")
```

## Dataset Freshness Logging

Freshness logging should calculate delay from the latest successful load for each dataset.

```python
def classify_freshness(delay_minutes: int, expected_minutes: int):
    if delay_minutes <= expected_minutes:
        return "fresh"
    if delay_minutes <= expected_minutes * 2:
        return "delayed"
    return "stale"
```

## Row Count Reconciliation Logging

```python
def log_row_count_reconciliation(
    reconciliation_id: str,
    run_id: str,
    source_layer: str,
    target_layer: str,
    source_table: str,
    target_table: str,
    source_row_count: int,
    target_row_count: int,
):
    difference = source_row_count - target_row_count
    status = "matched" if difference == 0 else "mismatch"

    row = [{
        "reconciliation_id": reconciliation_id,
        "run_id": run_id,
        "source_layer": source_layer,
        "target_layer": target_layer,
        "source_table": source_table,
        "target_table": target_table,
        "source_row_count": source_row_count,
        "target_row_count": target_row_count,
        "row_count_difference": difference,
        "reconciliation_status": status,
        "checked_at": datetime.now(timezone.utc),
    }]

    spark.createDataFrame(row).write.mode("append").saveAsTable("row_count_reconciliation")
```

## Error Logging

Errors should be concise and safe to display in operational reports. They should not include secrets, credentials, tokens, or sensitive local paths.

Recommended fields:

- Failed run identifier.
- Pipeline or notebook name.
- Layer.
- Status.
- Short error message.
- Start and end timestamps.

## Integration With Data Factory Pipelines

Future Data Factory pipelines can call observability notebooks at these points:

- At run start to insert `running` status.
- After each layer completes to log row counts.
- After data quality checks to log pass or fail outcomes.
- At run end to update final status and duration.
- On failure paths to record error details.

## Expected Outputs

- A row in `pipeline_run_log` for each run.
- Rows in `dataset_freshness` for each monitored dataset.
- Rows in `row_count_reconciliation` for layer-to-layer checks.
- Concise operational summaries for future Power BI dashboards.
