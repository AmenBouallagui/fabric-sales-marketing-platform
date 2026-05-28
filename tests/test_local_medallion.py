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
