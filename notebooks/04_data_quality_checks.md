# 04 Data Quality Checks Notebook Plan

## Objective

Design a future Microsoft Fabric notebook that runs configured quality checks across Bronze, Silver, and Gold tables, records results in `data_quality_results`, and decides whether downstream publication should continue based on severity.

This Markdown file is a notebook implementation plan. It is not an executable `.ipynb` artifact yet.

## Parameters

Planned notebook parameters:

- `run_id`: unique identifier for the pipeline or notebook run.
- `layer_name`: target layer to validate, such as `bronze`, `silver`, or `gold`.
- `fail_on_critical`: boolean flag, default `true`.
- `checked_at`: run timestamp.
- `write_results`: boolean flag, default `true`.

## Imports

Expected PySpark imports:

```python
from datetime import datetime, timezone
from pyspark.sql import functions as F
```

## Check Configuration

Quality checks should be configuration-driven so new checks can be added without rewriting notebook flow.

```python
CHECKS = [
    {
        "layer_name": "silver",
        "table_name": "silver_orders",
        "check_name": "order_id_not_null",
        "check_category": "completeness",
        "severity": "critical",
        "filter_sql": "order_id IS NULL",
        "expected_value": "0 failed rows",
    },
    {
        "layer_name": "silver",
        "table_name": "silver_orders",
        "check_name": "total_amount_non_negative",
        "check_category": "validity",
        "severity": "critical",
        "filter_sql": "total_amount < 0",
        "expected_value": "0 failed rows",
    },
]
```

## Run Completeness Checks

Completeness checks should confirm required fields are populated and expected tables contain rows.

```python
def run_failed_row_check(check: dict):
    df = spark.table(check["table_name"])
    failed_count = df.filter(check["filter_sql"]).count()
    return build_result(check, failed_count)
```

## Run Validity Checks

Validity checks should validate non-negative measures, acceptable date ranges, and parseable typed values.

Examples:

- Product price is positive.
- Order amounts are non-negative.
- Campaign end date is not earlier than campaign start date.
- Support ticket close time is not earlier than create time.

## Run Uniqueness Checks

Uniqueness checks should confirm business keys and surrogate keys are unique at the documented grain.

```python
def run_unique_key_check(table_name: str, key_column: str):
    df = spark.table(table_name)
    duplicates = (
        df.groupBy(key_column)
        .count()
        .filter(F.col("count") > 1)
        .count()
    )
    return duplicates
```

## Run Referential Integrity Checks

Referential checks should validate relationships such as:

- `silver_orders.customer_id` to `silver_customers.customer_id`.
- `silver_orders.product_id` to `silver_products.product_id`.
- `silver_ad_spend.campaign_id` to `silver_campaigns.campaign_id`.
- Gold facts to Gold dimensions.

## Run Freshness Checks

Freshness checks should compare the latest successful load timestamp to the dataset expected frequency.

```python
def calculate_delay_minutes(last_successful_load, checked_at):
    return int((checked_at - last_successful_load).total_seconds() / 60)
```

Freshness outcomes should also be written to `dataset_freshness`.

## Run Row Count Reconciliation

Row count checks should compare upstream and downstream layers.

Examples:

- Bronze distinct keys to Silver current rows.
- Silver valid/current rows to Gold fact rows.
- Gold dimension row counts to distinct Silver attributes.

## Write Results To `data_quality_results`

```python
def build_result(check: dict, failed_row_count: int):
    status = "passed" if failed_row_count == 0 else "failed"
    return {
        "check_id": f"{run_id}_{check['table_name']}_{check['check_name']}",
        "run_id": run_id,
        "layer_name": check["layer_name"],
        "table_name": check["table_name"],
        "check_name": check["check_name"],
        "check_category": check["check_category"],
        "severity": check["severity"],
        "status": status,
        "expected_value": check["expected_value"],
        "actual_value": f"{failed_row_count} failed rows",
        "failed_row_count": failed_row_count,
        "dq_issue_reason": None if status == "passed" else check["check_name"],
        "checked_at": checked_at,
    }
```

## Fail Or Continue Based On Severity

```python
critical_failures = [
    result for result in results
    if result["severity"] == "critical" and result["status"] == "failed"
]

if critical_failures and fail_on_critical:
    raise RuntimeError(f"Critical data quality checks failed: {len(critical_failures)}")
```

Warning and info checks should be logged but should not stop the run.

## Expected Outputs

- Rows written to `data_quality_results`.
- Optional rows written to `dataset_freshness`.
- Optional rows written to `row_count_reconciliation`.
- A compact summary of pass, warning, and failure counts by layer and table.
- A critical-failure signal that can stop downstream Gold publication.
