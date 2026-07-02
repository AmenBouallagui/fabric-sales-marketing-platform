"""Export the dbt gold marts from DuckDB to Parquet files for Power BI.

This gives Power BI a driver-free data source: the semantic model reads these
Parquet files directly (no ODBC driver, no credentials), so the project opens and
refreshes on any machine that has run the pipeline.

Usage (from the repository root, after `dbt build --project-dir dbt`):

    python powerbi/export_gold.py

Outputs land in data/powerbi/ (gitignored), one Parquet file per gold table.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

# All gold marts. dim_customer_segment is exported for completeness even though the
# current semantic model does not use it.
MARTS = [
    "dim_customer",
    "dim_product",
    "dim_campaign",
    "dim_channel",
    "dim_customer_segment",
    "dim_date",
    "fct_orders",
    "fct_ad_spend",
    "fct_support_tickets",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export gold marts to Parquet for Power BI.")
    parser.add_argument("--duckdb-path", default="dbt/target/sales_marketing.duckdb", help="Path to the dbt DuckDB database.")
    parser.add_argument("--out-dir", default="data/powerbi", help="Output folder for Parquet files.")
    parser.add_argument("--schema", default="main_marts", help="DuckDB schema holding the marts.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(args.duckdb_path, read_only=True)
    try:
        for mart in MARTS:
            # Drop the unknown date member (-1) so dim_date can be marked as a date table.
            where = " WHERE date_key <> -1" if mart == "dim_date" else ""
            target = (out_dir / f"{mart}.parquet").as_posix()
            con.execute(f"COPY (SELECT * FROM {args.schema}.{mart}{where}) TO '{target}' (FORMAT PARQUET)")
            rows = con.execute(f"SELECT count(*) FROM {args.schema}.{mart}{where}").fetchone()[0]
            print(f"{mart:24s} {rows:6d} rows -> {target}")
    finally:
        con.close()

    print(f"\nExported {len(MARTS)} marts to {out_dir.resolve()}")


if __name__ == "__main__":
    main()
