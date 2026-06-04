# Microsoft Fabric notebook source: nb_03_gold_modeling
#
# This file is version-controlled source code for a future Microsoft Fabric
# notebook named `nb_03_gold_modeling`.
#
# It expects to run inside a Microsoft Fabric notebook session with Spark
# available and access to the Silver Delta tables. It has not been executed in
# Fabric until a later implementation note or pull request explicitly documents
# that run.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


# Notebook parameters. In Fabric, these can be replaced by pipeline parameters
# or notebook parameter cells.
gold_processed_at = datetime.now(timezone.utc).isoformat()
write_mode = "overwrite"
unknown_key = -1


SILVER_TABLE_NAMES = {
    "customers": "silver_customers",
    "products": "silver_products",
    "campaigns": "silver_campaigns",
    "orders": "silver_orders",
    "ad_spend": "silver_ad_spend",
    "support_tickets": "silver_support_tickets",
}


DIMENSION_KEY_COLUMNS = {
    "dim_customer": "customer_key",
    "dim_product": "product_key",
    "dim_campaign": "campaign_key",
    "dim_date": "date_key",
    "dim_customer_segment": "customer_segment_key",
    "dim_channel": "channel_key",
}


FACT_BUSINESS_KEYS = {
    "fact_orders": "order_id",
    "fact_ad_spend": "spend_id",
    "fact_support_tickets": "ticket_id",
}


FACT_FOREIGN_KEYS = {
    "fact_orders": ["customer_key", "product_key", "campaign_key", "order_date_key"],
    "fact_ad_spend": ["campaign_key", "channel_key", "spend_date_key"],
    "fact_support_tickets": ["customer_key", "created_date_key", "closed_date_key"],
}


def read_silver_tables() -> dict[str, DataFrame]:
    """Read all expected Silver Delta tables."""
    return {
        entity_name: spark.table(table_name)
        for entity_name, table_name in SILVER_TABLE_NAMES.items()
    }


def current_valid(df: DataFrame) -> DataFrame:
    """Filter to current valid Silver records."""
    return df.filter(
        (F.col("is_current_record") == F.lit(True)) & (F.col("dq_status") == F.lit("valid"))
    )


def stable_hash_key(column: str) -> Any:
    """Create a deterministic positive hash-based surrogate key expression."""
    return F.abs(F.xxhash64(F.coalesce(F.col(column).cast("string"), F.lit("UNKNOWN"))))


def gold_timestamp() -> Any:
    """Return the configured Gold processing timestamp expression."""
    return F.to_timestamp(F.lit(gold_processed_at))


def build_dim_customer(customers: DataFrame) -> DataFrame:
    """Build one Gold customer dimension row per current valid customer."""
    return (
        customers.select(
            stable_hash_key("customer_id").alias("customer_key"),
            "customer_id",
            "customer_name",
            "email",
            "country",
            "city",
            "customer_segment",
            "company_size",
            "industry",
            "acquisition_channel",
            "status",
            "signup_date",
        )
        .dropDuplicates(["customer_key"])
        .withColumn("gold_processed_at", gold_timestamp())
    )


def build_dim_product(products: DataFrame) -> DataFrame:
    """Build one Gold product dimension row per current valid product."""
    return (
        products.select(
            stable_hash_key("product_id").alias("product_key"),
            "product_id",
            "product_name",
            "category",
            "plan_tier",
            "unit_price",
            "unit_cost",
            "is_subscription",
            "valid_from",
            "valid_to",
        )
        .dropDuplicates(["product_key"])
        .withColumn("gold_processed_at", gold_timestamp())
    )


def build_dim_campaign(campaigns: DataFrame) -> DataFrame:
    """Build one Gold campaign dimension row per current valid campaign."""
    return (
        campaigns.select(
            stable_hash_key("campaign_id").alias("campaign_key"),
            "campaign_id",
            "campaign_name",
            "channel",
            "campaign_start_date",
            "campaign_end_date",
            "target_segment",
            "objective",
        )
        .dropDuplicates(["campaign_key"])
        .withColumn("gold_processed_at", gold_timestamp())
    )


def build_dim_customer_segment(customers: DataFrame) -> DataFrame:
    """Build a reusable customer segment dimension."""
    return (
        customers.select(F.col("customer_segment"))
        .where(F.col("customer_segment").isNotNull())
        .dropDuplicates(["customer_segment"])
        .withColumn(
            "customer_segment_key",
            stable_hash_key("customer_segment"),
        )
        .select("customer_segment_key", "customer_segment")
        .withColumn("gold_processed_at", gold_timestamp())
    )


def build_dim_channel(
    customers: DataFrame, campaigns: DataFrame, ad_spend: DataFrame
) -> DataFrame:
    """Build a reusable channel dimension across acquisition and marketing data."""
    acquisition_channels = customers.select(F.col("acquisition_channel").alias("channel"))
    campaign_channels = campaigns.select(F.col("channel"))
    spend_channels = ad_spend.select(F.col("channel"))

    return (
        acquisition_channels.unionByName(campaign_channels, allowMissingColumns=True)
        .unionByName(spend_channels, allowMissingColumns=True)
        .where(F.col("channel").isNotNull())
        .dropDuplicates(["channel"])
        .withColumn("channel_key", stable_hash_key("channel"))
        .select("channel_key", "channel")
        .withColumn("gold_processed_at", gold_timestamp())
    )


def collect_date_bounds(date_frames: list[DataFrame]) -> tuple[str, str]:
    """Collect minimum and maximum dates across source date columns."""
    date_values = date_frames[0]
    for frame in date_frames[1:]:
        date_values = date_values.unionByName(frame, allowMissingColumns=True)

    bounds = date_values.select(
        F.min("calendar_date").alias("min_date"),
        F.max("calendar_date").alias("max_date"),
    ).collect()[0]

    min_date = bounds["min_date"] or "2024-01-01"
    max_date = bounds["max_date"] or "2025-12-31"
    return str(min_date), str(max_date)


def build_dim_date(
    customers: DataFrame,
    campaigns: DataFrame,
    orders: DataFrame,
    ad_spend: DataFrame,
    support_tickets: DataFrame,
) -> DataFrame:
    """Build a date dimension covering the analytical source date range."""
    date_frames = [
        customers.select(F.col("signup_date").alias("calendar_date")),
        campaigns.select(F.col("campaign_start_date").alias("calendar_date")),
        campaigns.select(F.col("campaign_end_date").alias("calendar_date")),
        orders.select(F.col("order_date").alias("calendar_date")),
        ad_spend.select(F.col("spend_date").alias("calendar_date")),
        support_tickets.select(F.to_date(F.col("created_at")).alias("calendar_date")),
        support_tickets.select(F.to_date(F.col("closed_at")).alias("calendar_date")),
    ]

    start_date, end_date = collect_date_bounds(date_frames)
    dates = spark.sql(
        "SELECT explode(sequence("
        f"to_date('{start_date}'), to_date('{end_date}'), interval 1 day"
        ")) AS calendar_date"
    )

    return (
        dates.withColumn("date_key", F.date_format("calendar_date", "yyyyMMdd").cast("int"))
        .withColumn("calendar_year", F.year("calendar_date"))
        .withColumn("calendar_quarter", F.quarter("calendar_date"))
        .withColumn("calendar_month", F.month("calendar_date"))
        .withColumn("month_name", F.date_format("calendar_date", "MMMM"))
        .withColumn("day_of_month", F.dayofmonth("calendar_date"))
        .withColumn("day_of_week", F.date_format("calendar_date", "EEEE"))
        .withColumn("is_weekend", F.dayofweek("calendar_date").isin(1, 7))
        .withColumn("month_start_date", F.trunc("calendar_date", "month"))
        .withColumn("month_end_date", F.last_day("calendar_date"))
        .withColumn("gold_processed_at", gold_timestamp())
    )


def unknown_dimension_rows() -> dict[str, list[dict[str, Any]]]:
    """Define unknown members for dimensions that facts may reference."""
    return {
        "dim_customer": [
            {
                "customer_key": unknown_key,
                "customer_id": "UNKNOWN",
                "customer_name": "Unknown Customer",
                "email": None,
                "country": "Unknown",
                "city": "Unknown",
                "customer_segment": "Unknown",
                "company_size": "Unknown",
                "industry": "Unknown",
                "acquisition_channel": "Unknown",
                "status": "Unknown",
                "signup_date": None,
                "gold_processed_at": gold_processed_at,
            }
        ],
        "dim_product": [
            {
                "product_key": unknown_key,
                "product_id": "UNKNOWN",
                "product_name": "Unknown Product",
                "category": "Unknown",
                "plan_tier": "Unknown",
                "unit_price": None,
                "unit_cost": None,
                "is_subscription": None,
                "valid_from": None,
                "valid_to": None,
                "gold_processed_at": gold_processed_at,
            }
        ],
        "dim_campaign": [
            {
                "campaign_key": unknown_key,
                "campaign_id": "UNKNOWN",
                "campaign_name": "Unknown Campaign",
                "channel": "Unknown",
                "campaign_start_date": None,
                "campaign_end_date": None,
                "target_segment": "Unknown",
                "objective": "Unknown",
                "gold_processed_at": gold_processed_at,
            }
        ],
        "dim_date": [
            {
                "date_key": unknown_key,
                "calendar_date": None,
                "calendar_year": None,
                "calendar_quarter": None,
                "calendar_month": None,
                "month_name": "Unknown",
                "day_of_month": None,
                "day_of_week": "Unknown",
                "is_weekend": None,
                "month_start_date": None,
                "month_end_date": None,
                "gold_processed_at": gold_processed_at,
            }
        ],
        "dim_customer_segment": [
            {
                "customer_segment_key": unknown_key,
                "customer_segment": "Unknown",
                "gold_processed_at": gold_processed_at,
            }
        ],
        "dim_channel": [
            {
                "channel_key": unknown_key,
                "channel": "Unknown",
                "gold_processed_at": gold_processed_at,
            }
        ],
    }


def add_unknown_members(dimensions: dict[str, DataFrame]) -> dict[str, DataFrame]:
    """Add a documented unknown member to each Gold dimension."""
    unknown_rows = unknown_dimension_rows()
    enriched_dimensions = {}

    for table_name, df in dimensions.items():
        unknown_row = unknown_rows[table_name][0]
        unknown_df = df.limit(0).select(
            *[
                F.lit(unknown_row.get(field.name)).cast(field.dataType).alias(field.name)
                for field in df.schema.fields
            ]
        )
        enriched_dimensions[table_name] = unknown_df.unionByName(
            df, allowMissingColumns=True
        )

    return enriched_dimensions


def date_key(column: str) -> Any:
    """Build a YYYYMMDD integer key from a date or timestamp column."""
    return F.date_format(F.to_date(F.col(column)), "yyyyMMdd").cast("int")


def build_fact_orders(
    orders: DataFrame,
    dim_customer: DataFrame,
    dim_product: DataFrame,
    dim_campaign: DataFrame,
) -> DataFrame:
    """Build one Gold order fact row per current valid order."""
    customer_lookup = dim_customer.select("customer_key", "customer_id")
    product_lookup = dim_product.select("product_key", "product_id", "unit_cost")
    campaign_lookup = dim_campaign.select("campaign_key", "campaign_id")

    return (
        orders.join(customer_lookup, "customer_id", "left")
        .join(product_lookup, "product_id", "left")
        .join(campaign_lookup, "campaign_id", "left")
        .withColumn("order_key", stable_hash_key("order_id"))
        .withColumn("customer_key", F.coalesce(F.col("customer_key"), F.lit(unknown_key)))
        .withColumn("product_key", F.coalesce(F.col("product_key"), F.lit(unknown_key)))
        .withColumn("campaign_key", F.coalesce(F.col("campaign_key"), F.lit(unknown_key)))
        .withColumn("order_date_key", F.coalesce(date_key("order_date"), F.lit(unknown_key)))
        .withColumn("net_revenue", F.col("total_amount") - F.col("tax_amount"))
        .withColumn("estimated_cost", F.col("quantity") * F.col("unit_cost"))
        .withColumn("gross_margin", F.col("net_revenue") - F.col("estimated_cost"))
        .select(
            "order_key",
            "order_id",
            "customer_key",
            "product_key",
            "campaign_key",
            "order_date_key",
            "quantity",
            "unit_price",
            "discount_amount",
            "tax_amount",
            "total_amount",
            "net_revenue",
            "estimated_cost",
            "gross_margin",
            "payment_status",
            "refund_flag",
        )
        .withColumn("gold_processed_at", gold_timestamp())
    )


def build_fact_ad_spend(
    ad_spend: DataFrame, dim_campaign: DataFrame, dim_channel: DataFrame
) -> DataFrame:
    """Build one Gold ad spend fact row per campaign spend record."""
    campaign_lookup = dim_campaign.select("campaign_key", "campaign_id")
    channel_lookup = dim_channel.select("channel_key", "channel")

    return (
        ad_spend.join(campaign_lookup, "campaign_id", "left")
        .join(channel_lookup, "channel", "left")
        .withColumn("ad_spend_key", stable_hash_key("spend_id"))
        .withColumn("campaign_key", F.coalesce(F.col("campaign_key"), F.lit(unknown_key)))
        .withColumn("channel_key", F.coalesce(F.col("channel_key"), F.lit(unknown_key)))
        .withColumn("spend_date_key", F.coalesce(date_key("spend_date"), F.lit(unknown_key)))
        .select(
            "ad_spend_key",
            "spend_id",
            "campaign_key",
            "channel_key",
            "spend_date_key",
            "impressions",
            "clicks",
            "conversions",
            "spend_amount",
        )
        .withColumn("gold_processed_at", gold_timestamp())
    )


def build_fact_support_tickets(
    support_tickets: DataFrame, dim_customer: DataFrame
) -> DataFrame:
    """Build one Gold support ticket fact row per support ticket."""
    customer_lookup = dim_customer.select("customer_key", "customer_id")

    return (
        support_tickets.join(customer_lookup, "customer_id", "left")
        .withColumn("ticket_key", stable_hash_key("ticket_id"))
        .withColumn("customer_key", F.coalesce(F.col("customer_key"), F.lit(unknown_key)))
        .withColumn("created_date_key", F.coalesce(date_key("created_at"), F.lit(unknown_key)))
        .withColumn("closed_date_key", F.coalesce(date_key("closed_at"), F.lit(unknown_key)))
        .select(
            "ticket_key",
            "ticket_id",
            "customer_key",
            "created_date_key",
            "closed_date_key",
            "priority",
            "category",
            "status",
            "satisfaction_score",
            "first_response_minutes",
            "resolution_minutes",
        )
        .withColumn("gold_processed_at", gold_timestamp())
    )


def write_gold_table(df: DataFrame, table_name: str, write_mode: str) -> None:
    """Write a Gold DataFrame to a Delta table."""
    (
        df.write.format("delta")
        .mode(write_mode)
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )


def count_duplicate_values(df: DataFrame, key_column: str) -> int:
    """Count duplicate key values in a DataFrame."""
    return (
        df.groupBy(key_column)
        .count()
        .filter(F.col("count") > F.lit(1))
        .count()
    )


def validate_gold_tables(gold_tables: dict[str, DataFrame]) -> None:
    """Validate key uniqueness, required foreign keys, row counts, and unknown usage."""
    validation_errors = []

    print("Gold validation summary")

    for table_name, df in gold_tables.items():
        row_count = df.count()
        print(f"- {table_name}: {row_count} rows")

        if table_name in DIMENSION_KEY_COLUMNS:
            key_column = DIMENSION_KEY_COLUMNS[table_name]
            duplicate_count = count_duplicate_values(df, key_column)
            print(f"  duplicate {key_column}: {duplicate_count}")
            if duplicate_count > 0:
                validation_errors.append(
                    f"{table_name} has {duplicate_count} duplicate {key_column} values"
                )

        if table_name in FACT_BUSINESS_KEYS:
            key_column = FACT_BUSINESS_KEYS[table_name]
            duplicate_count = count_duplicate_values(df, key_column)
            print(f"  duplicate {key_column}: {duplicate_count}")
            if duplicate_count > 0:
                validation_errors.append(
                    f"{table_name} has {duplicate_count} duplicate {key_column} values"
                )

        for foreign_key in FACT_FOREIGN_KEYS.get(table_name, []):
            null_count = df.filter(F.col(foreign_key).isNull()).count()
            unknown_count = df.filter(F.col(foreign_key) == F.lit(unknown_key)).count()
            print(f"  {foreign_key}: {null_count} null, {unknown_count} unknown")
            if null_count > 0:
                validation_errors.append(
                    f"{table_name} has {null_count} null {foreign_key} values"
                )

    if validation_errors:
        raise ValueError("Gold validation failed: " + "; ".join(validation_errors))


def main() -> None:
    """Run Gold dimensional modeling from valid/current Silver records."""
    print("Starting Gold modeling")
    print(f"gold_processed_at={gold_processed_at}")
    print(f"write_mode={write_mode}")
    print(f"unknown_key={unknown_key}")

    silver_tables = read_silver_tables()
    customers = current_valid(silver_tables["customers"])
    products = current_valid(silver_tables["products"])
    campaigns = current_valid(silver_tables["campaigns"])
    orders = current_valid(silver_tables["orders"])
    ad_spend = current_valid(silver_tables["ad_spend"])
    support_tickets = current_valid(silver_tables["support_tickets"])

    dimensions = {
        "dim_customer": build_dim_customer(customers),
        "dim_product": build_dim_product(products),
        "dim_campaign": build_dim_campaign(campaigns),
        "dim_date": build_dim_date(
            customers, campaigns, orders, ad_spend, support_tickets
        ),
        "dim_customer_segment": build_dim_customer_segment(customers),
        "dim_channel": build_dim_channel(customers, campaigns, ad_spend),
    }
    dimensions = add_unknown_members(dimensions)

    facts = {
        "fact_orders": build_fact_orders(
            orders,
            dimensions["dim_customer"],
            dimensions["dim_product"],
            dimensions["dim_campaign"],
        ),
        "fact_ad_spend": build_fact_ad_spend(
            ad_spend,
            dimensions["dim_campaign"],
            dimensions["dim_channel"],
        ),
        "fact_support_tickets": build_fact_support_tickets(
            support_tickets,
            dimensions["dim_customer"],
        ),
    }

    gold_tables = {**dimensions, **facts}
    validate_gold_tables(gold_tables)

    for table_name, df in gold_tables.items():
        write_gold_table(df, table_name, write_mode)

    print("Gold modeling write summary")
    for table_name, df in gold_tables.items():
        print(f"- {table_name}: {df.count()} rows")


main()
