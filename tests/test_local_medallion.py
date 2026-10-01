from pathlib import Path
import subprocess
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = PROJECT_ROOT / "data_generation" / "generate_source_data.py"
PIPELINE = PROJECT_ROOT / "local_pipeline" / "run_local_medallion.py"


def run_command(args: list[str]) -> None:
    """Run a project command and fail the test with useful output."""
    result = subprocess.run(args, cwd=PROJECT_ROOT, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_local_medallion_pipeline_outputs(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    output_dir = tmp_path / "medallion"

    run_command(
        [
            sys.executable,
            str(GENERATOR),
            "--output-dir",
            str(source_dir),
            "--seed",
            "123",
            "--customers",
            "30",
            "--orders",
            "120",
            "--start-date",
            "2024-01-01",
            "--end-date",
            "2024-03-31",
        ]
    )
    # A valid order with unresolved dimension IDs must survive with unknown keys.
    orders = pd.read_csv(source_dir / "orders.csv")
    orphan = orders.iloc[0].copy()
    orphan.update(pd.Series({"order_id": "ORPHAN-TEST", "customer_id": "MISSING-C", "product_id": "MISSING-P", "campaign_id": "MISSING-CMP", "order_date": "2024-02-01", "quantity": 1, "unit_price": 10, "discount_amount": 0, "tax_amount": 0, "total_amount": 10, "payment_status": "Paid", "refund_flag": False}))
    pd.concat([orders, orphan.to_frame().T], ignore_index=True).to_csv(source_dir / "orders.csv", index=False)

    run_command(
        [
            sys.executable,
            str(PIPELINE),
            "--source-dir",
            str(source_dir),
            "--output-dir",
            str(output_dir),
            "--load-date",
            "2024-04-01",
            "--run-id",
            "pytest-run",
        ]
    )

    expected_outputs = [
        output_dir / "bronze" / "customers.parquet",
        output_dir / "silver" / "customers.parquet",
        output_dir / "gold" / "fact_orders.parquet",
        output_dir / "gold" / "fact_ad_spend.parquet",
        output_dir / "gold" / "fact_support_tickets.parquet",
        output_dir / "observability" / "pipeline_run_log.parquet",
        output_dir / "observability" / "data_quality_results.parquet",
        output_dir / "observability" / "row_count_reconciliation.parquet",
    ]
    for path in expected_outputs:
        assert path.exists(), f"Expected output missing: {path}"

    fact_orders = pd.read_parquet(output_dir / "gold" / "fact_orders.parquet")
    fact_ad_spend = pd.read_parquet(output_dir / "gold" / "fact_ad_spend.parquet")
    fact_support_tickets = pd.read_parquet(output_dir / "gold" / "fact_support_tickets.parquet")

    orphan_fact = fact_orders.loc[fact_orders["order_id"] == "ORPHAN-TEST"].iloc[0]
    assert all(orphan_fact[key] == -1 for key in ["customer_key", "product_key", "campaign_key"])
    assert pd.isna(orphan_fact["estimated_cost"])
    assert len(fact_orders) > 0
    assert len(fact_ad_spend) > 0
    assert len(fact_support_tickets) > 0

    assert {"customer_key", "product_key"}.issubset(fact_orders.columns)
    assert "campaign_key" in fact_ad_spend.columns
    assert "customer_key" in fact_support_tickets.columns

    tracked_generated = subprocess.run(
        ["git", "ls-files", "data"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert tracked_generated.returncode == 0
    assert tracked_generated.stdout.strip() == ""

    # Every unresolved FK has a real unknown member, rather than a dangling -1.
    for fact, dimension, key in [
        (fact_orders, 'dim_customer', 'customer_key'),
        (fact_orders, 'dim_product', 'product_key'),
        (fact_orders, 'dim_campaign', 'campaign_key'),
        (fact_orders, 'dim_date', 'order_date_key'),
        (fact_ad_spend, 'dim_campaign', 'campaign_key'),
        (fact_ad_spend, 'dim_channel', 'channel_key'),
        (fact_support_tickets, 'dim_customer', 'customer_key'),
    ]:
        members = pd.read_parquet(output_dir / 'gold' / f'{dimension}.parquet')
        dim_key = 'date_key' if dimension == 'dim_date' else key
        assert -1 in set(members[dim_key])
        assert set(fact[key]).issubset(set(members[dim_key]))
