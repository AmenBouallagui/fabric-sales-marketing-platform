"""Run a local Bronze, Silver, Gold medallion prototype with pandas."""

from __future__ import annotations

import argparse
import hashlib
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


SOURCE_CONFIG = {
    "customers": {
        "file_name": "customers.csv",
        "source_system": "synthetic_crm",
        "business_key": "customer_id",
    },
    "products": {
        "file_name": "products.csv",
        "source_system": "synthetic_crm",
        "business_key": "product_id",
    },
    "campaigns": {
        "file_name": "campaigns.csv",
        "source_system": "synthetic_marketing",
        "business_key": "campaign_id",
    },
    "orders": {
        "file_name": "orders.csv",
        "source_system": "synthetic_crm",
        "business_key": "order_id",
    },
    "ad_spend": {
        "file_name": "ad_spend.csv",
        "source_system": "synthetic_marketing",
        "business_key": "spend_id",
    },
    "support_tickets": {
        "file_name": "support_tickets.csv",
        "source_system": "synthetic_crm",
        "business_key": "ticket_id",
    },
}

DATE_COLUMNS = {
    "customers": ["signup_date", "load_date"],
    "products": ["valid_from", "valid_to", "load_date"],
    "campaigns": ["campaign_start_date", "campaign_end_date", "load_date"],
    "orders": ["order_date", "load_date"],
    "ad_spend": ["spend_date", "load_date"],
    "support_tickets": ["load_date"],
}

TIMESTAMP_COLUMNS = {
    "customers": ["updated_at", "ingested_at", "source_updated_at"],
    "products": ["updated_at", "ingested_at", "source_updated_at"],
    "campaigns": ["updated_at", "ingested_at", "source_updated_at"],
    "orders": ["updated_at", "ingested_at", "source_updated_at"],
    "ad_spend": ["updated_at", "ingested_at", "source_updated_at"],
    "support_tickets": ["created_at", "closed_at", "updated_at", "ingested_at", "source_updated_at"],
}

INTEGER_COLUMNS = {
    "orders": ["quantity"],
    "ad_spend": ["impressions", "clicks", "conversions"],
    "support_tickets": ["first_response_minutes", "resolution_minutes"],
}

MONEY_COLUMNS = {
    "products": ["unit_price", "unit_cost"],
    "orders": ["unit_price", "discount_amount", "tax_amount", "total_amount"],
    "ad_spend": ["spend_amount"],
}

BOOLEAN_COLUMNS = {
    "products": ["is_subscription"],
    "orders": ["refund_flag"],
}

VALID_CUSTOMER_STATUSES = {"Active", "Inactive", "Churned"}
VALID_PAYMENT_STATUSES = {"Paid", "Failed", "Pending"}
VALID_CHANNELS = {"Paid Search", "Paid Social", "Organic", "Email", "Referral", "Partner", "Direct"}
VALID_TICKET_STATUSES = {"Closed", "Resolved", "Open", "In Progress"}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the local medallion prototype.")
    parser.add_argument("--source-dir", default="data/source", help="Folder containing source CSV files.")
    parser.add_argument("--output-dir", default="data", help="Base output folder for medallion outputs.")
    parser.add_argument("--load-date", default=date.today().isoformat(), help="Load date in YYYY-MM-DD format.")
    parser.add_argument("--run-id", default=None, help="Optional ingestion run identifier.")
    return parser.parse_args()


def stable_hash(value: Any) -> int:
    """Return a deterministic positive integer hash for a source value."""
    if pd.isna(value) or value == "":
        return -1
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return int(digest[:15], 16)


def row_hash(frame: pd.DataFrame) -> pd.Series:
    """Create deterministic row hashes from all source columns in a DataFrame."""
    source_values = frame.fillna("").astype(str)
    return source_values.apply(lambda row: hashlib.sha256("||".join(row).encode("utf-8")).hexdigest(), axis=1)


def read_sources(source_dir: Path) -> dict[str, pd.DataFrame]:
    """Read all required source CSV files."""
    sources: dict[str, pd.DataFrame] = {}
    for entity, config in SOURCE_CONFIG.items():
        path = source_dir / config["file_name"]
        if not path.exists():
            raise FileNotFoundError(f"Missing required source file: {path}")
        sources[entity] = pd.read_csv(path)
    return sources


def build_bronze(
    sources: dict[str, pd.DataFrame],
    source_dir: Path,
    load_date: str,
    run_id: str,
    ingested_at: pd.Timestamp,
) -> dict[str, pd.DataFrame]:
    """Build Bronze DataFrames with ingestion metadata."""
    bronze: dict[str, pd.DataFrame] = {}
    for entity, source_df in sources.items():
        config = SOURCE_CONFIG[entity]
        frame = source_df.copy()
        source_file_path = source_dir / config["file_name"]
        frame["ingestion_run_id"] = run_id
        frame["source_file_name"] = config["file_name"]
        frame["source_file_path"] = str(source_file_path)
        frame["source_system"] = config["source_system"]
        frame["entity_name"] = entity
        frame["load_date"] = pd.to_datetime(load_date).date()
        frame["ingested_at"] = ingested_at
        frame["source_updated_at"] = pd.to_datetime(frame["updated_at"], errors="coerce")
        frame["row_hash"] = row_hash(source_df)
        bronze[entity] = frame
    return bronze


def trim_strings(frame: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace in string columns."""
    result = frame.copy()
    for column in result.select_dtypes(include=["object", "string"]).columns:
        result[column] = result[column].map(lambda value: value.strip() if isinstance(value, str) else value)
    return result


def normalize_boolean(series: pd.Series) -> pd.Series:
    """Normalize common boolean-like values."""
    return series.map(
        lambda value: value
        if pd.isna(value)
        else str(value).strip().lower() in {"true", "1", "yes", "y", "t"}
    )


def cast_entity_types(entity: str, frame: pd.DataFrame) -> pd.DataFrame:
    """Cast date, timestamp, boolean, integer, and monetary columns."""
    result = frame.copy()
    for column in DATE_COLUMNS.get(entity, []):
        if column in result.columns:
            result[column] = pd.to_datetime(result[column], errors="coerce").dt.date
    for column in TIMESTAMP_COLUMNS.get(entity, []):
        if column in result.columns:
            result[column] = pd.to_datetime(result[column], errors="coerce")
    for column in INTEGER_COLUMNS.get(entity, []):
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce").astype("Int64")
    for column in MONEY_COLUMNS.get(entity, []):
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce").round(2)
    for column in BOOLEAN_COLUMNS.get(entity, []):
        if column in result.columns:
            result[column] = normalize_boolean(result[column])
    return result


def normalize_categories(entity: str, frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize known categorical values to stable casing."""
    result = frame.copy()
    if entity == "customers" and "status" in result.columns:
        result["status"] = result["status"].str.title()
    if entity == "orders" and "payment_status" in result.columns:
        result["payment_status"] = result["payment_status"].str.title()
    if entity == "support_tickets" and "status" in result.columns:
        result["status"] = result["status"].str.title()
        result["status"] = result["status"].replace({"In Progress": "In Progress"})
    return result


def deduplicate_latest(entity: str, frame: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate by business key using source_updated_at, ingested_at, then row_hash."""
    business_key = SOURCE_CONFIG[entity]["business_key"]
    sorted_frame = frame.sort_values(
        by=[business_key, "source_updated_at", "ingested_at", "row_hash"],
        ascending=[True, False, False, False],
        na_position="last",
    )
    return sorted_frame.drop_duplicates(subset=[business_key], keep="first").copy()


def validation_issues(entity: str, frame: pd.DataFrame) -> pd.Series:
    """Return semicolon-separated validation issues for each row."""
    issues = pd.Series([""] * len(frame), index=frame.index, dtype="object")
    key = SOURCE_CONFIG[entity]["business_key"]

    def add_issue(mask: pd.Series, message: str) -> None:
        nonlocal issues
        issues.loc[mask.fillna(False)] = issues.loc[mask.fillna(False)].map(
            lambda existing: message if existing == "" else f"{existing}; {message}"
        )

    add_issue(frame[key].isna(), f"missing {key}")

    if entity == "customers":
        add_issue(frame["customer_name"].isna(), "missing customer_name")
        add_issue(frame["signup_date"].isna(), "missing signup_date")
        add_issue(~frame["status"].isin(VALID_CUSTOMER_STATUSES), "invalid customer status")
    elif entity == "products":
        add_issue(frame["product_name"].isna(), "missing product_name")
        add_issue(frame["unit_price"].isna() | (frame["unit_price"] <= 0), "invalid unit_price")
        add_issue(frame["unit_cost"].isna() | (frame["unit_cost"] < 0), "invalid unit_cost")
    elif entity == "campaigns":
        add_issue(frame["channel"].isna(), "missing channel")
        add_issue(frame["campaign_start_date"].isna(), "missing campaign_start_date")
        add_issue(~frame["channel"].isin(VALID_CHANNELS), "invalid campaign channel")
    elif entity == "orders":
        add_issue(frame["customer_id"].isna(), "missing customer_id")
        add_issue(frame["product_id"].isna(), "missing product_id")
        add_issue(frame["payment_status"].isna(), "missing payment_status")
        add_issue(~frame["payment_status"].isin(VALID_PAYMENT_STATUSES), "invalid payment_status")
        add_issue(frame["total_amount"].isna() | (frame["total_amount"] < 0), "invalid total_amount")
        for column in ["unit_price", "discount_amount", "tax_amount"]:
            add_issue(frame[column].isna() | (frame[column] < 0), f"invalid {column}")
    elif entity == "ad_spend":
        add_issue(frame["campaign_id"].isna(), "missing campaign_id")
        for column in ["spend_amount", "impressions", "clicks", "conversions"]:
            add_issue(frame[column].isna() | (frame[column] < 0), f"invalid {column}")
    elif entity == "support_tickets":
        add_issue(frame["customer_id"].isna(), "missing customer_id")
        add_issue(frame["created_at"].isna(), "missing created_at")
        add_issue(frame["status"].isna(), "missing status")
        add_issue(~frame["status"].isin(VALID_TICKET_STATUSES), "invalid support ticket status")

    return issues


def build_silver(bronze: dict[str, pd.DataFrame], processed_at: pd.Timestamp) -> dict[str, pd.DataFrame]:
    """Build cleaned, typed, deduplicated Silver DataFrames."""
    silver: dict[str, pd.DataFrame] = {}
    for entity, bronze_df in bronze.items():
        frame = normalize_categories(entity, cast_entity_types(entity, trim_strings(bronze_df)))
        frame = deduplicate_latest(entity, frame)
        issues = validation_issues(entity, frame)
        frame["silver_processed_at"] = processed_at
        frame["is_current_record"] = True
        frame["dq_issue_reason"] = issues.replace("", pd.NA)
        frame["dq_status"] = np.where(issues == "", "valid", "rejected")
        silver[entity] = frame
    return silver


def date_key(series: pd.Series) -> pd.Series:
    """Convert date-like values to YYYYMMDD integer keys."""
    parsed = pd.to_datetime(series, errors="coerce")
    return parsed.dt.strftime("%Y%m%d").astype("float").astype("Int64")


def with_unknown_key(series: pd.Series) -> pd.Series:
    """Replace missing surrogate keys with the documented unknown key."""
    return series.fillna(-1).astype("int64")


def current_valid(silver: dict[str, pd.DataFrame], entity: str) -> pd.DataFrame:
    """Return current valid Silver records for an entity."""
    frame = silver[entity]
    return frame[(frame["is_current_record"]) & (frame["dq_status"] == "valid")].copy()


def build_dim_date(*date_series: pd.Series, processed_at: pd.Timestamp) -> pd.DataFrame:
    """Build a date dimension covering supplied date values."""
    parsed_dates = pd.concat([pd.to_datetime(series, errors="coerce") for series in date_series]).dropna()
    if parsed_dates.empty:
        start_date = pd.Timestamp(date.today())
        end_date = start_date
    else:
        start_date = parsed_dates.min().normalize()
        end_date = parsed_dates.max().normalize()
    dates = pd.date_range(start_date, end_date, freq="D")
    frame = pd.DataFrame({"calendar_date": dates})
    frame["date_key"] = frame["calendar_date"].dt.strftime("%Y%m%d").astype(int)
    frame["calendar_year"] = frame["calendar_date"].dt.year
    frame["calendar_quarter"] = frame["calendar_date"].dt.quarter
    frame["calendar_month"] = frame["calendar_date"].dt.month
    frame["month_name"] = frame["calendar_date"].dt.month_name()
    frame["day_of_month"] = frame["calendar_date"].dt.day
    frame["day_of_week"] = frame["calendar_date"].dt.day_name()
    frame["is_weekend"] = frame["calendar_date"].dt.dayofweek >= 5
    frame["gold_processed_at"] = processed_at
    return frame[["date_key", "calendar_date", "calendar_year", "calendar_quarter", "calendar_month", "month_name", "day_of_month", "day_of_week", "is_weekend", "gold_processed_at"]]


def build_gold(silver: dict[str, pd.DataFrame], processed_at: pd.Timestamp) -> dict[str, pd.DataFrame]:
    """Build Gold dimensions and facts from current valid Silver records."""
    customers = current_valid(silver, "customers")
    products = current_valid(silver, "products")
    campaigns = current_valid(silver, "campaigns")
    orders = current_valid(silver, "orders")
    ad_spend = current_valid(silver, "ad_spend")
    tickets = current_valid(silver, "support_tickets")

    dim_customer = customers[["customer_id", "customer_name", "email", "country", "city", "customer_segment", "company_size", "industry", "acquisition_channel", "status", "signup_date"]].copy()
    dim_customer["customer_key"] = dim_customer["customer_id"].map(stable_hash)
    dim_customer["gold_processed_at"] = processed_at

    dim_product = products[["product_id", "product_name", "category", "plan_tier", "unit_price", "unit_cost", "is_subscription", "valid_from", "valid_to"]].copy()
    dim_product["product_key"] = dim_product["product_id"].map(stable_hash)
    dim_product["gold_processed_at"] = processed_at

    dim_campaign = campaigns[["campaign_id", "campaign_name", "channel", "campaign_start_date", "campaign_end_date", "target_segment", "objective"]].copy()
    dim_campaign["campaign_key"] = dim_campaign["campaign_id"].map(stable_hash)
    dim_campaign["gold_processed_at"] = processed_at

    segments = sorted(set(customers["customer_segment"].dropna()))
    dim_customer_segment = pd.DataFrame({"customer_segment": segments})
    dim_customer_segment["customer_segment_key"] = dim_customer_segment["customer_segment"].map(stable_hash)
    dim_customer_segment["gold_processed_at"] = processed_at

    channels = sorted(set(pd.concat([customers["acquisition_channel"], campaigns["channel"], ad_spend["channel"]]).dropna()))
    dim_channel = pd.DataFrame({"channel": channels})
    dim_channel["channel_key"] = dim_channel["channel"].map(stable_hash)
    dim_channel["channel_group"] = dim_channel["channel"]
    dim_channel["gold_processed_at"] = processed_at

    dim_date = build_dim_date(
        customers["signup_date"],
        campaigns["campaign_start_date"],
        campaigns["campaign_end_date"],
        orders["order_date"],
        ad_spend["spend_date"],
        tickets["created_at"],
        tickets["closed_at"],
        processed_at=processed_at,
    )

    fact_orders = orders.merge(dim_customer[["customer_id", "customer_key"]], on="customer_id", how="left")
    fact_orders = fact_orders.merge(dim_product[["product_id", "product_key", "unit_cost"]], on="product_id", how="left")
    fact_orders = fact_orders.merge(dim_campaign[["campaign_id", "campaign_key"]], on="campaign_id", how="left")
    fact_orders["order_key"] = fact_orders["order_id"].map(stable_hash)
    fact_orders["customer_key"] = with_unknown_key(fact_orders["customer_key"])
    fact_orders["product_key"] = with_unknown_key(fact_orders["product_key"])
    fact_orders["campaign_key"] = with_unknown_key(fact_orders["campaign_key"])
    fact_orders["order_date_key"] = with_unknown_key(date_key(fact_orders["order_date"]))
    fact_orders["net_revenue"] = (fact_orders["total_amount"] - fact_orders["tax_amount"]).round(2)
    fact_orders["estimated_cost"] = (fact_orders["quantity"].astype(float) * fact_orders["unit_cost"].astype(float)).round(2)
    fact_orders["gross_margin"] = (fact_orders["net_revenue"] - fact_orders["estimated_cost"]).round(2)
    fact_orders["gold_processed_at"] = processed_at
    fact_orders = fact_orders[["order_key", "order_id", "customer_key", "product_key", "campaign_key", "order_date_key", "quantity", "unit_price", "discount_amount", "tax_amount", "total_amount", "net_revenue", "estimated_cost", "gross_margin", "payment_status", "refund_flag", "gold_processed_at"]]

    fact_ad_spend = ad_spend.merge(dim_campaign[["campaign_id", "campaign_key"]], on="campaign_id", how="left")
    fact_ad_spend = fact_ad_spend.merge(dim_channel[["channel", "channel_key"]], on="channel", how="left")
    fact_ad_spend["ad_spend_key"] = fact_ad_spend["spend_id"].map(stable_hash)
    fact_ad_spend["campaign_key"] = with_unknown_key(fact_ad_spend["campaign_key"])
    fact_ad_spend["channel_key"] = with_unknown_key(fact_ad_spend["channel_key"])
    fact_ad_spend["spend_date_key"] = with_unknown_key(date_key(fact_ad_spend["spend_date"]))
    fact_ad_spend["gold_processed_at"] = processed_at
    fact_ad_spend = fact_ad_spend[["ad_spend_key", "spend_id", "campaign_key", "channel_key", "spend_date_key", "impressions", "clicks", "conversions", "spend_amount", "gold_processed_at"]]

    fact_support_tickets = tickets.merge(dim_customer[["customer_id", "customer_key"]], on="customer_id", how="left")
    fact_support_tickets["ticket_key"] = fact_support_tickets["ticket_id"].map(stable_hash)
    fact_support_tickets["customer_key"] = with_unknown_key(fact_support_tickets["customer_key"])
    fact_support_tickets["created_date_key"] = with_unknown_key(date_key(fact_support_tickets["created_at"]))
    fact_support_tickets["closed_date_key"] = date_key(fact_support_tickets["closed_at"])
    fact_support_tickets["gold_processed_at"] = processed_at
    fact_support_tickets = fact_support_tickets[["ticket_key", "ticket_id", "customer_key", "created_date_key", "closed_date_key", "priority", "category", "status", "satisfaction_score", "first_response_minutes", "resolution_minutes", "gold_processed_at"]]

    return {
        "dim_customer": dim_customer[["customer_key", "customer_id", "customer_name", "email", "country", "city", "customer_segment", "company_size", "industry", "acquisition_channel", "status", "signup_date", "gold_processed_at"]],
        "dim_product": dim_product[["product_key", "product_id", "product_name", "category", "plan_tier", "unit_price", "unit_cost", "is_subscription", "valid_from", "valid_to", "gold_processed_at"]],
        "dim_campaign": dim_campaign[["campaign_key", "campaign_id", "campaign_name", "channel", "campaign_start_date", "campaign_end_date", "target_segment", "objective", "gold_processed_at"]],
        "dim_date": dim_date,
        "dim_customer_segment": dim_customer_segment[["customer_segment_key", "customer_segment", "gold_processed_at"]],
        "dim_channel": dim_channel[["channel_key", "channel", "channel_group", "gold_processed_at"]],
        "fact_orders": fact_orders,
        "fact_ad_spend": fact_ad_spend,
        "fact_support_tickets": fact_support_tickets,
    }


def write_outputs(output_dir: Path, bronze: dict[str, pd.DataFrame], silver: dict[str, pd.DataFrame], gold: dict[str, pd.DataFrame], observability: dict[str, pd.DataFrame]) -> None:
    """Write medallion outputs to parquet files."""
    for layer_name, datasets in {
        "bronze": bronze,
        "silver": silver,
        "gold": gold,
        "observability": observability,
    }.items():
        layer_dir = output_dir / layer_name
        layer_dir.mkdir(parents=True, exist_ok=True)
        for name, frame in datasets.items():
            frame.to_parquet(layer_dir / f"{name}.parquet", index=False)


def quality_result(run_id: str, layer: str, table: str, check: str, category: str, failed_count: int, severity: str = "critical") -> dict[str, Any]:
    """Build a local data quality result record."""
    status = "passed" if failed_count == 0 else "failed"
    return {
        "check_id": f"{run_id}_{layer}_{table}_{check}",
        "run_id": run_id,
        "layer_name": layer,
        "table_name": table,
        "check_name": check,
        "check_category": category,
        "severity": severity,
        "status": status,
        "expected_value": "0 failed rows",
        "actual_value": f"{failed_count} failed rows",
        "failed_row_count": failed_count,
        "dq_issue_reason": None if status == "passed" else check,
        "checked_at": pd.Timestamp.now(tz=timezone.utc),
    }


def log_observability(
    run_id: str,
    start_time: pd.Timestamp,
    end_time: pd.Timestamp,
    sources: dict[str, pd.DataFrame],
    bronze: dict[str, pd.DataFrame],
    silver: dict[str, pd.DataFrame],
    gold: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """Build local observability outputs."""
    rows_read = sum(len(frame) for frame in sources.values())
    rows_written = sum(len(frame) for frame in bronze.values()) + sum(len(frame) for frame in silver.values()) + sum(len(frame) for frame in gold.values())
    pipeline_run_log = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "pipeline_name": "local_medallion_prototype",
                "layer_name": "local",
                "status": "succeeded",
                "start_time": start_time,
                "end_time": end_time,
                "duration_seconds": int((end_time - start_time).total_seconds()),
                "rows_read": rows_read,
                "rows_written": rows_written,
                "error_message": None,
                "triggered_by": "local_cli",
                "created_at": end_time,
            }
        ]
    )

    dq_rows: list[dict[str, Any]] = []
    for entity, frame in silver.items():
        dq_rows.append(quality_result(run_id, "silver", entity, "required_key_not_null", "completeness", int(frame[SOURCE_CONFIG[entity]["business_key"]].isna().sum())))
        dq_rows.append(quality_result(run_id, "silver", entity, "dq_status_valid_or_rejected", "validity", int((~frame["dq_status"].isin(["valid", "rejected"])).sum()), "warning"))
    for fact_name, key_columns in {
        "fact_orders": ["customer_key", "product_key"],
        "fact_ad_spend": ["campaign_key"],
        "fact_support_tickets": ["customer_key"],
    }.items():
        frame = gold[fact_name]
        failed_count = int(frame[key_columns].isna().any(axis=1).sum())
        dq_rows.append(quality_result(run_id, "gold", fact_name, "foreign_keys_not_null", "referential_integrity", failed_count))

    reconciliation_rows: list[dict[str, Any]] = []
    for entity in SOURCE_CONFIG:
        source_count = len(sources[entity])
        bronze_count = len(bronze[entity])
        reconciliation_rows.append(
            {
                "reconciliation_id": f"{run_id}_source_bronze_{entity}",
                "run_id": run_id,
                "source_layer": "source",
                "target_layer": "bronze",
                "source_table": f"{entity}.csv",
                "target_table": f"bronze_{entity}_raw",
                "source_row_count": source_count,
                "target_row_count": bronze_count,
                "row_count_difference": source_count - bronze_count,
                "reconciliation_status": "matched" if source_count == bronze_count else "mismatch",
                "checked_at": end_time,
            }
        )
        bronze_keys = bronze[entity][SOURCE_CONFIG[entity]["business_key"]].nunique(dropna=True)
        silver_count = len(silver[entity])
        reconciliation_rows.append(
            {
                "reconciliation_id": f"{run_id}_bronze_silver_{entity}",
                "run_id": run_id,
                "source_layer": "bronze",
                "target_layer": "silver",
                "source_table": f"bronze_{entity}_raw",
                "target_table": f"silver_{entity}",
                "source_row_count": bronze_keys,
                "target_row_count": silver_count,
                "row_count_difference": bronze_keys - silver_count,
                "reconciliation_status": "matched" if bronze_keys == silver_count else "mismatch",
                "checked_at": end_time,
            }
        )

    silver_to_gold = {
        "orders": "fact_orders",
        "ad_spend": "fact_ad_spend",
        "support_tickets": "fact_support_tickets",
    }
    for entity, fact_name in silver_to_gold.items():
        silver_valid_count = len(current_valid(silver, entity))
        gold_count = len(gold[fact_name])
        reconciliation_rows.append(
            {
                "reconciliation_id": f"{run_id}_silver_gold_{entity}",
                "run_id": run_id,
                "source_layer": "silver",
                "target_layer": "gold",
                "source_table": f"silver_{entity}",
                "target_table": fact_name,
                "source_row_count": silver_valid_count,
                "target_row_count": gold_count,
                "row_count_difference": silver_valid_count - gold_count,
                "reconciliation_status": "matched" if silver_valid_count == gold_count else "mismatch",
                "checked_at": end_time,
            }
        )

    return {
        "pipeline_run_log": pipeline_run_log,
        "data_quality_results": pd.DataFrame(dq_rows),
        "row_count_reconciliation": pd.DataFrame(reconciliation_rows),
    }


def main() -> None:
    """Run the local medallion prototype."""
    args = parse_args()
    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir)
    run_id = args.run_id or f"local-{uuid.uuid4()}"
    start_time = pd.Timestamp.now(tz=timezone.utc)

    sources = read_sources(source_dir)
    bronze = build_bronze(sources, source_dir, args.load_date, run_id, start_time)
    silver = build_silver(bronze, pd.Timestamp.now(tz=timezone.utc))
    gold = build_gold(silver, pd.Timestamp.now(tz=timezone.utc))
    end_time = pd.Timestamp.now(tz=timezone.utc)
    observability = log_observability(run_id, start_time, end_time, sources, bronze, silver, gold)
    write_outputs(output_dir, bronze, silver, gold, observability)

    print("Local medallion prototype completed successfully.")
    print(f"Run ID: {run_id}")
    print(f"Source path: {source_dir.resolve()}")
    print(f"Output path: {output_dir.resolve()}")
    for layer_name, datasets in [("bronze", bronze), ("silver", silver), ("gold", gold), ("observability", observability)]:
        print(f"{layer_name}:")
        for name, frame in datasets.items():
            print(f"  {name}: {len(frame):,} rows")


if __name__ == "__main__":
    main()
