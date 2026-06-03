# Microsoft Fabric notebook source: nb_02_silver_transformations
#
# This file is version-controlled source code for a future Microsoft Fabric
# notebook named `nb_02_silver_transformations`.
#
# It expects to run inside a Microsoft Fabric notebook session with Spark
# available and access to the Bronze Delta tables. It has not been executed in
# Fabric until a later implementation note or pull request explicitly documents
# that run.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F
from pyspark.sql.types import BooleanType, DecimalType, IntegerType


# Notebook parameters. In Fabric, these can be replaced by pipeline parameters
# or notebook parameter cells.
silver_processed_at = datetime.now(timezone.utc).isoformat()
write_mode = "overwrite"
fail_on_critical = True


VALID_CUSTOMER_STATUSES = ["Active", "Inactive", "Churned"]
VALID_PAYMENT_STATUSES = ["Paid", "Failed", "Pending"]
VALID_CAMPAIGN_CHANNELS = [
    "Paid Search",
    "Paid Social",
    "Organic",
    "Email",
    "Referral",
    "Partner",
    "Direct",
]
VALID_TICKET_STATUSES = ["Closed", "Resolved", "Open", "In Progress"]


SOURCES: list[dict[str, Any]] = [
    {
        "entity_name": "customers",
        "bronze_table": "bronze_customers_raw",
        "silver_table": "silver_customers",
        "primary_key": "customer_id",
        "required_columns": ["customer_id", "customer_name", "signup_date"],
        "date_columns": ["signup_date", "load_date"],
        "timestamp_columns": ["source_updated_at", "ingested_at"],
        "numeric_columns": [],
        "boolean_columns": [],
        "valid_values": {"status": VALID_CUSTOMER_STATUSES},
    },
    {
        "entity_name": "products",
        "bronze_table": "bronze_products_raw",
        "silver_table": "silver_products",
        "primary_key": "product_id",
        "required_columns": ["product_id", "unit_price", "unit_cost"],
        "date_columns": ["valid_from", "valid_to", "load_date"],
        "timestamp_columns": ["source_updated_at", "ingested_at"],
        "numeric_columns": ["unit_price", "unit_cost"],
        "boolean_columns": ["is_subscription"],
        "valid_values": {},
    },
    {
        "entity_name": "campaigns",
        "bronze_table": "bronze_campaigns_raw",
        "silver_table": "silver_campaigns",
        "primary_key": "campaign_id",
        "required_columns": ["campaign_id", "channel", "campaign_start_date"],
        "date_columns": ["campaign_start_date", "campaign_end_date", "load_date"],
        "timestamp_columns": ["source_updated_at", "ingested_at"],
        "numeric_columns": [],
        "boolean_columns": [],
        "valid_values": {"channel": VALID_CAMPAIGN_CHANNELS},
    },
    {
        "entity_name": "orders",
        "bronze_table": "bronze_orders_raw",
        "silver_table": "silver_orders",
        "primary_key": "order_id",
        "required_columns": [
            "order_id",
            "customer_id",
            "product_id",
            "total_amount",
            "payment_status",
        ],
        "date_columns": ["order_date", "load_date"],
        "timestamp_columns": ["source_updated_at", "ingested_at"],
        "numeric_columns": [
            "quantity",
            "unit_price",
            "discount_amount",
            "tax_amount",
            "total_amount",
        ],
        "boolean_columns": ["refund_flag"],
        "valid_values": {"payment_status": VALID_PAYMENT_STATUSES},
    },
    {
        "entity_name": "ad_spend",
        "bronze_table": "bronze_ad_spend_raw",
        "silver_table": "silver_ad_spend",
        "primary_key": "spend_id",
        "required_columns": ["spend_id", "campaign_id", "spend_amount"],
        "date_columns": ["spend_date", "load_date"],
        "timestamp_columns": ["source_updated_at", "ingested_at"],
        "numeric_columns": ["impressions", "clicks", "conversions", "spend_amount"],
        "boolean_columns": [],
        "valid_values": {"channel": VALID_CAMPAIGN_CHANNELS},
    },
    {
        "entity_name": "support_tickets",
        "bronze_table": "bronze_support_tickets_raw",
        "silver_table": "silver_support_tickets",
        "primary_key": "ticket_id",
        "required_columns": ["ticket_id", "customer_id", "created_at", "status"],
        "date_columns": ["load_date"],
        "timestamp_columns": [
            "created_at",
            "closed_at",
            "source_updated_at",
            "ingested_at",
        ],
        "numeric_columns": [
            "satisfaction_score",
            "first_response_minutes",
            "resolution_minutes",
        ],
        "boolean_columns": [],
        "valid_values": {"status": VALID_TICKET_STATUSES},
    },
]


def read_bronze_table(config: dict[str, Any]) -> DataFrame:
    """Read a configured Bronze Delta table."""
    return spark.table(config["bronze_table"])


def trim_string_columns(df: DataFrame) -> DataFrame:
    """Trim leading and trailing whitespace from all string columns."""
    for column_name, dtype in df.dtypes:
        if dtype == "string":
            df = df.withColumn(column_name, F.trim(F.col(column_name)))
    return df


def cast_columns(df: DataFrame, config: dict[str, Any]) -> DataFrame:
    """Cast configured date, timestamp, numeric, and boolean columns."""
    for column_name in config.get("date_columns", []):
        if column_name in df.columns:
            df = df.withColumn(column_name, F.to_date(F.col(column_name)))

    for column_name in config.get("timestamp_columns", []):
        if column_name in df.columns:
            df = df.withColumn(column_name, F.to_timestamp(F.col(column_name)))

    for column_name in config.get("numeric_columns", []):
        if column_name not in df.columns:
            continue

        if column_name in {"quantity", "impressions", "clicks", "conversions"}:
            df = df.withColumn(column_name, F.col(column_name).cast(IntegerType()))
        else:
            df = df.withColumn(column_name, F.col(column_name).cast(DecimalType(18, 2)))

    for column_name in config.get("boolean_columns", []):
        if column_name not in df.columns:
            continue

        normalized = F.lower(F.col(column_name).cast("string"))
        df = df.withColumn(
            column_name,
            F.when(normalized.isin("true", "1", "yes", "y"), F.lit(True))
            .when(normalized.isin("false", "0", "no", "n"), F.lit(False))
            .otherwise(F.col(column_name).cast(BooleanType())),
        )

    return df


def normalize_categories(df: DataFrame, config: dict[str, Any]) -> DataFrame:
    """Normalize configured categorical fields to expected business casing."""
    for column_name, valid_values in config.get("valid_values", {}).items():
        if column_name not in df.columns:
            continue

        normalized = F.initcap(F.lower(F.col(column_name)))
        df = df.withColumn(
            column_name,
            F.when(F.col(column_name).isNull(), F.lit(None))
            .when(normalized.isin(*valid_values), normalized)
            .otherwise(F.col(column_name)),
        )

    return df


def deduplicate_latest(df: DataFrame, config: dict[str, Any]) -> DataFrame:
    """Keep one latest current record per primary key for the MVP."""
    primary_key = config["primary_key"]
    window_spec = (
        Window.partitionBy(primary_key)
        .orderBy(
            F.col("source_updated_at").desc_nulls_last(),
            F.col("ingested_at").desc_nulls_last(),
            F.col("row_hash").desc_nulls_last(),
        )
    )

    return (
        df.withColumn("_record_rank", F.row_number().over(window_spec))
        .filter(F.col("_record_rank") == F.lit(1))
        .drop("_record_rank")
    )


def build_quality_issues(df: DataFrame, config: dict[str, Any]) -> DataFrame:
    """Build a semicolon-delimited quality issue reason column."""
    issue_expressions = []
    primary_key = config["primary_key"]

    if primary_key in df.columns:
        issue_expressions.append(
            F.when(F.col(primary_key).isNull(), F.lit(f"missing {primary_key}"))
        )

    for column_name in config.get("required_columns", []):
        if column_name not in df.columns:
            issue_expressions.append(F.lit(f"missing required column {column_name}"))
            continue

        issue_expressions.append(
            F.when(F.col(column_name).isNull(), F.lit(f"missing {column_name}"))
        )

    for column_name in config.get("numeric_columns", []):
        if column_name in df.columns:
            issue_expressions.append(
                F.when(F.col(column_name) < F.lit(0), F.lit(f"negative {column_name}"))
            )

    for column_name, valid_values in config.get("valid_values", {}).items():
        if column_name in df.columns:
            issue_expressions.append(
                F.when(
                    F.col(column_name).isNotNull()
                    & ~F.col(column_name).isin(*valid_values),
                    F.lit(f"invalid {column_name}"),
                )
            )

    if not issue_expressions:
        return df.withColumn("dq_issue_reason", F.lit(""))

    return (
        df.withColumn("_dq_issues", F.array(*issue_expressions))
        .withColumn(
            "dq_issue_reason",
            F.concat_ws("; ", F.expr("filter(_dq_issues, issue -> issue is not null)")),
        )
        .drop("_dq_issues")
    )


def add_silver_metadata(
    df: DataFrame, config: dict[str, Any], silver_processed_at: str
) -> DataFrame:
    """Add Silver processing metadata and record-level quality status."""
    return (
        df.withColumn("silver_processed_at", F.to_timestamp(F.lit(silver_processed_at)))
        .withColumn("is_current_record", F.lit(True))
        .withColumn(
            "dq_status",
            F.when(F.length(F.col("dq_issue_reason")) > 0, F.lit("rejected")).otherwise(
                F.lit("valid")
            ),
        )
    )


def write_silver_table(df: DataFrame, table_name: str, write_mode: str) -> None:
    """Write a Silver DataFrame to a Delta table."""
    (
        df.write.format("delta")
        .mode(write_mode)
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )


def transform_entity(config: dict[str, Any]) -> DataFrame:
    """Transform one Bronze entity into its Silver representation."""
    bronze_df = read_bronze_table(config)
    standardized_df = trim_string_columns(bronze_df)
    typed_df = cast_columns(standardized_df, config)
    normalized_df = normalize_categories(typed_df, config)
    current_df = deduplicate_latest(normalized_df, config)
    quality_df = build_quality_issues(current_df, config)
    return add_silver_metadata(quality_df, config, silver_processed_at)


def count_missing_relationship(
    child_df: DataFrame,
    parent_df: DataFrame,
    child_key: str,
    parent_key: str,
    child_filter: Any | None = None,
) -> int:
    """Count child records that do not have a matching parent key."""
    filtered_child = child_df if child_filter is None else child_df.filter(child_filter)
    parent_keys = parent_df.select(F.col(parent_key).alias("_parent_key")).distinct()

    return (
        filtered_child.join(parent_keys, F.col(child_key) == F.col("_parent_key"), "left")
        .filter(F.col("_parent_key").isNull())
        .count()
    )


def run_referential_integrity_checks(silver_tables: dict[str, DataFrame]) -> None:
    """Print referential integrity results and fail on critical issues if configured."""
    checks = [
        {
            "name": "silver_orders.customer_id exists in silver_customers.customer_id",
            "child_table": "silver_orders",
            "parent_table": "silver_customers",
            "child_key": "customer_id",
            "parent_key": "customer_id",
            "filter": F.col("customer_id").isNotNull(),
        },
        {
            "name": "silver_orders.product_id exists in silver_products.product_id",
            "child_table": "silver_orders",
            "parent_table": "silver_products",
            "child_key": "product_id",
            "parent_key": "product_id",
            "filter": F.col("product_id").isNotNull(),
        },
        {
            "name": "silver_orders.campaign_id exists in silver_campaigns.campaign_id",
            "child_table": "silver_orders",
            "parent_table": "silver_campaigns",
            "child_key": "campaign_id",
            "parent_key": "campaign_id",
            "filter": F.col("campaign_id").isNotNull(),
        },
        {
            "name": "silver_ad_spend.campaign_id exists in silver_campaigns.campaign_id",
            "child_table": "silver_ad_spend",
            "parent_table": "silver_campaigns",
            "child_key": "campaign_id",
            "parent_key": "campaign_id",
            "filter": F.col("campaign_id").isNotNull(),
        },
        {
            "name": "silver_support_tickets.customer_id exists in silver_customers.customer_id",
            "child_table": "silver_support_tickets",
            "parent_table": "silver_customers",
            "child_key": "customer_id",
            "parent_key": "customer_id",
            "filter": F.col("customer_id").isNotNull(),
        },
    ]

    failed_checks = []

    print("Referential integrity check summary")
    for check in checks:
        failed_count = count_missing_relationship(
            silver_tables[check["child_table"]],
            silver_tables[check["parent_table"]],
            check["child_key"],
            check["parent_key"],
            check["filter"],
        )
        print(f"- {check['name']}: {failed_count} failed rows")

        if failed_count > 0:
            failed_checks.append((check["name"], failed_count))

    if failed_checks and fail_on_critical:
        details = "; ".join(f"{name}: {count}" for name, count in failed_checks)
        raise ValueError(f"Critical referential integrity failures detected: {details}")


def main() -> None:
    """Run Silver transformations for every configured Bronze source."""
    print("Starting Silver transformations")
    print(f"silver_processed_at={silver_processed_at}")
    print(f"write_mode={write_mode}")

    silver_tables: dict[str, DataFrame] = {}
    results: list[dict[str, Any]] = []

    for config in SOURCES:
        silver_df = transform_entity(config)
        silver_tables[config["silver_table"]] = silver_df

        total_rows = silver_df.count()
        rejected_rows = silver_df.filter(F.col("dq_status") == F.lit("rejected")).count()
        results.append(
            {
                "entity_name": config["entity_name"],
                "bronze_table": config["bronze_table"],
                "silver_table": config["silver_table"],
                "row_count": total_rows,
                "rejected_count": rejected_rows,
            }
        )

    run_referential_integrity_checks(silver_tables)

    for config in SOURCES:
        write_silver_table(
            silver_tables[config["silver_table"]],
            config["silver_table"],
            write_mode,
        )

    print("Silver transformation summary")
    for result in results:
        print(
            f"- {result['entity_name']} -> {result['silver_table']}: "
            f"{result['row_count']} rows, {result['rejected_count']} rejected"
        )

    print(f"Entities transformed: {len(results)} of {len(SOURCES)}")


main()
