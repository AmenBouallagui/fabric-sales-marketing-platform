# Microsoft Fabric notebook source: nb_01_bronze_ingestion
#
# This file is version-controlled source code for a future Microsoft Fabric
# notebook named `nb_01_bronze_ingestion`.
#
# It expects to run inside a Microsoft Fabric notebook session with Spark
# available and attached to the Bronze Lakehouse. It is not an `.ipynb` file and
# does not indicate that Fabric execution has already happened.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

try:
    from notebookutils import mssparkutils  # type: ignore
except ImportError:  # pragma: no cover - available only in Fabric notebooks
    mssparkutils = None


# Notebook parameters. In Fabric, these can be replaced by pipeline parameters
# or notebook parameter cells.
source_base_path = "Files/source"
load_date = "YYYY-MM-DD"
ingestion_run_id = str(uuid4())
ingested_at = datetime.now(timezone.utc).isoformat()
fail_on_missing_file = True


SOURCES: list[dict[str, Any]] = [
    {
        "source_system": "synthetic_crm",
        "entity_name": "customers",
        "file_name": "customers.csv",
        "bronze_table": "bronze_customers_raw",
        "primary_key": "customer_id",
        "required_columns": [
            "customer_id",
            "account_id",
            "customer_name",
            "email",
            "country",
            "city",
            "signup_date",
            "acquisition_channel",
            "customer_segment",
            "company_size",
            "industry",
            "status",
            "updated_at",
        ],
    },
    {
        "source_system": "synthetic_crm",
        "entity_name": "products",
        "file_name": "products.csv",
        "bronze_table": "bronze_products_raw",
        "primary_key": "product_id",
        "required_columns": [
            "product_id",
            "product_name",
            "category",
            "plan_tier",
            "unit_price",
            "unit_cost",
            "is_subscription",
            "valid_from",
            "valid_to",
            "updated_at",
        ],
    },
    {
        "source_system": "synthetic_marketing",
        "entity_name": "campaigns",
        "file_name": "campaigns.csv",
        "bronze_table": "bronze_campaigns_raw",
        "primary_key": "campaign_id",
        "required_columns": [
            "campaign_id",
            "campaign_name",
            "channel",
            "campaign_start_date",
            "campaign_end_date",
            "target_segment",
            "objective",
            "updated_at",
        ],
    },
    {
        "source_system": "synthetic_crm",
        "entity_name": "orders",
        "file_name": "orders.csv",
        "bronze_table": "bronze_orders_raw",
        "primary_key": "order_id",
        "required_columns": [
            "order_id",
            "customer_id",
            "product_id",
            "order_date",
            "quantity",
            "unit_price",
            "discount_amount",
            "tax_amount",
            "total_amount",
            "payment_status",
            "refund_flag",
            "campaign_id",
            "updated_at",
        ],
    },
    {
        "source_system": "synthetic_marketing",
        "entity_name": "ad_spend",
        "file_name": "ad_spend.csv",
        "bronze_table": "bronze_ad_spend_raw",
        "primary_key": "spend_id",
        "required_columns": [
            "spend_id",
            "campaign_id",
            "spend_date",
            "channel",
            "impressions",
            "clicks",
            "conversions",
            "spend_amount",
            "updated_at",
        ],
    },
    {
        "source_system": "synthetic_crm",
        "entity_name": "support_tickets",
        "file_name": "support_tickets.csv",
        "bronze_table": "bronze_support_tickets_raw",
        "primary_key": "ticket_id",
        "required_columns": [
            "ticket_id",
            "customer_id",
            "created_at",
            "closed_at",
            "priority",
            "category",
            "status",
            "satisfaction_score",
            "first_response_minutes",
            "resolution_minutes",
            "updated_at",
        ],
    },
]


def build_source_file_path(
    config: dict[str, Any], source_base_path: str, load_date: str
) -> str:
    """Build the Lakehouse Files path for a configured source entity."""
    return (
        f"{source_base_path}/{config['source_system']}/{config['entity_name']}"
        f"/load_date={load_date}/{config['file_name']}"
    )


def read_source_csv(config: dict[str, Any], source_file_path: str) -> DataFrame:
    """Read a source CSV file with Spark using the expected Bronze options."""
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(source_file_path)
    )


def validate_required_columns(df: DataFrame, config: dict[str, Any]) -> None:
    """Validate required columns and primary key completeness before writing."""
    required_columns = set(config["required_columns"])
    actual_columns = set(df.columns)
    missing_columns = sorted(required_columns - actual_columns)

    if missing_columns:
        raise ValueError(
            f"{config['entity_name']} is missing required columns: {missing_columns}"
        )

    primary_key = config["primary_key"]
    null_key_count = df.filter(F.col(primary_key).isNull()).count()

    if null_key_count > 0:
        raise ValueError(
            f"{config['entity_name']} contains {null_key_count} null primary keys "
            f"for `{primary_key}`"
        )


def add_ingestion_metadata(
    df: DataFrame,
    config: dict[str, Any],
    source_file_path: str,
    ingestion_run_id: str,
    ingested_at: str,
    load_date: str,
) -> DataFrame:
    """Preserve source columns and add standard Bronze ingestion metadata."""
    source_columns = df.columns
    row_hash = F.sha2(
        F.concat_ws(
            "||",
            *[F.coalesce(F.col(column).cast("string"), F.lit("")) for column in source_columns],
        ),
        256,
    )

    return (
        df.withColumn("ingestion_run_id", F.lit(ingestion_run_id))
        .withColumn("source_file_name", F.lit(config["file_name"]))
        .withColumn("source_file_path", F.lit(source_file_path))
        .withColumn("source_system", F.lit(config["source_system"]))
        .withColumn("entity_name", F.lit(config["entity_name"]))
        .withColumn("load_date", F.to_date(F.lit(load_date)))
        .withColumn("ingested_at", F.to_timestamp(F.lit(ingested_at)))
        .withColumn("source_updated_at", F.to_timestamp(F.col("updated_at")))
        .withColumn("row_hash", row_hash)
    )


def write_bronze_table(df: DataFrame, table_name: str) -> None:
    """Append an enriched source DataFrame to a Bronze Delta table."""
    df.write.format("delta").mode("append").saveAsTable(table_name)


def source_file_exists(source_file_path: str) -> bool | None:
    """Return file existence when Fabric utilities are available."""
    if mssparkutils is None:
        return None

    try:
        return bool(mssparkutils.fs.exists(source_file_path))
    except Exception as exc:
        print(f"Could not pre-check file existence for {source_file_path}: {exc}")
        return None


def load_entity(config: dict[str, Any]) -> dict[str, Any] | None:
    """Load one configured entity from Lakehouse Files into a Bronze table."""
    source_file_path = build_source_file_path(config, source_base_path, load_date)
    file_exists = source_file_exists(source_file_path)

    if file_exists is False:
        message = f"Missing source file for {config['entity_name']}: {source_file_path}"
        if fail_on_missing_file:
            raise FileNotFoundError(message)
        print(f"Skipping entity. {message}")
        return None

    try:
        raw_df = read_source_csv(config, source_file_path)
    except Exception as exc:
        message = f"Failed to read {config['entity_name']} from {source_file_path}: {exc}"
        if fail_on_missing_file:
            raise FileNotFoundError(message) from exc
        print(f"Skipping entity. {message}")
        return None

    validate_required_columns(raw_df, config)
    bronze_df = add_ingestion_metadata(
        raw_df,
        config,
        source_file_path,
        ingestion_run_id,
        ingested_at,
        load_date,
    )

    row_count = bronze_df.count()
    write_bronze_table(bronze_df, config["bronze_table"])

    return {
        "entity_name": config["entity_name"],
        "source_system": config["source_system"],
        "source_file_path": source_file_path,
        "bronze_table": config["bronze_table"],
        "row_count": row_count,
        "ingestion_run_id": ingestion_run_id,
    }


def main() -> None:
    """Run Bronze ingestion for every configured source entity."""
    print("Starting Bronze ingestion")
    print(f"load_date={load_date}")
    print(f"ingestion_run_id={ingestion_run_id}")
    print(f"ingested_at={ingested_at}")

    results: list[dict[str, Any]] = []

    for config in SOURCES:
        result = load_entity(config)
        if result is not None:
            results.append(result)

    print("Bronze ingestion summary")
    for result in results:
        print(
            f"- {result['entity_name']} -> {result['bronze_table']}: "
            f"{result['row_count']} rows"
        )

    print(f"Entities loaded: {len(results)} of {len(SOURCES)}")


main()
