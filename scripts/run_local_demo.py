"""Build a fresh credential-free demo and retain evidence under ignored outputs/."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import hashlib
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
QUERY_NAMES = ["monthly_revenue", "category_margin", "campaign_roas", "channel_spend",
               "customer_segments", "support_quality", "demo_failed_checks", "demo_pipeline_runs"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'outputs/local_demo')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    database = output / 'warehouse.duckdb'
    if database.exists():
        parser.error('Choose a new --output-dir; an existing warehouse would not prove a fresh build.')
    output.mkdir(parents=True, exist_ok=True)
    logs = output / 'logs'
    logs.mkdir(exist_ok=True)
    env = dict(os.environ, DBT_PROFILES_DIR=str(ROOT / 'dbt'), DBT_DUCKDB_PATH=str(database))
    dbt = [sys.executable, '-c', 'from dbt.cli.main import cli; cli()']
    steps = [
        ('generate', [sys.executable, 'data_generation/generate_source_data.py', '--output-dir', str(output / 'source'), '--customers', '50', '--orders', '250', '--seed', '123', '--start-date', '2024-01-01', '--end-date', '2024-03-31']),
        ('pandas', [sys.executable, 'local_pipeline/run_local_medallion.py', '--source-dir', str(output / 'source'), '--output-dir', str(output / 'pandas'), '--load-date', '2024-04-01', '--run-id', 'local-demo']),
        ('dbt_deps', dbt + ['deps', '--project-dir', 'dbt']),
        ('dbt_seed', dbt + ['seed', '--project-dir', 'dbt']),
        ('dbt_build', dbt + ['build', '--project-dir', 'dbt']),
        ('pytest', [sys.executable, '-m', 'pytest', '-q']),
    ]
    fixture_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / 'dbt/seeds').rglob('*.csv'))}
    evidence = {'fixture_sha256': fixture_hashes, 'started_at_utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(), 'steps': []}
    for name, command in steps:
        print(f'Running {name}...', flush=True)
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        (logs / f'{name}.log').write_text(result.stdout + result.stderr)
        evidence['steps'].append({'name': name, 'returncode': result.returncode})
        (output / 'execution.json').write_text(json.dumps(evidence, indent=2))
        if result.returncode:
            print((result.stdout + result.stderr)[-6000:], file=sys.stderr)
            raise SystemExit(result.returncode)

    import duckdb
    connection = duckdb.connect(str(database), read_only=True)
    statements = connection.extract_statements((ROOT / 'sql/business_metric_queries.sql').read_text())
    if len(statements) != len(QUERY_NAMES):
        raise RuntimeError('Update QUERY_NAMES to match the metric query file.')
    query_results = {}
    for name, statement in zip(QUERY_NAMES, statements):
        cursor = connection.execute(statement)
        columns = [column[0] for column in cursor.description]
        query_results[name] = [dict(zip(columns, row)) for row in cursor.fetchall()]
    totals = connection.execute("""
        SELECT COUNT(DISTINCT order_id) AS orders,
               ROUND(SUM(total_amount), 2) AS revenue,
               ROUND(SUM(net_revenue), 2) AS net_revenue
        FROM marts.fct_orders WHERE payment_status = 'Paid' AND refund_flag = false
    """).fetchone()
    run_results = json.loads((ROOT / 'dbt/target/run_results.json').read_text())
    nodes = run_results['results']
    assert all(node['status'] in ('success', 'pass', 'no-op') for node in nodes), 'Unexpected dbt result status'
    model_count = sum(node['unique_id'].startswith('model.') for node in nodes)
    test_count = sum(node['unique_id'].startswith('test.') for node in nodes)
    connection.close()
    (output / 'metrics.json').write_text(json.dumps(query_results, indent=2, default=str))
    evidence.update({'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'dbt_models': model_count,
                     'dbt_data_tests': test_count, 'metric_queries': len(statements),
                     'paid_non_refunded_orders': totals[0], 'revenue': totals[1], 'net_revenue': totals[2],
                     'query_row_counts': {name: len(rows) for name, rows in query_results.items()}})
    (output / 'execution.json').write_text(json.dumps(evidence, indent=2))
    lines = ['# Local demo verification', '', f"Completed UTC: {evidence['completed_at_utc']}", '',
             'Synthetic demonstration data. No cloud or report refresh was performed.', '',
             f'- Python: {evidence["python"]}', f'- dbt models built: {model_count}',
             f'- dbt data tests passed: {test_count}', f'- Metric queries executed: {len(statements)}',
             '- Python regression results: see logs/pytest.log.', '',
             '## Warehouse totals', '', 'All committed fixture dates; Paid orders with refund_flag = false. Revenue includes tax.', '',
             f'- Orders: {totals[0]}', f'- Revenue: {totals[1]:,.2f}', f'- Net revenue: {totals[2]:,.2f}', '',
             '## Metric query coverage', '', '| Query | Rows |', '| --- | ---: |']
    lines += [f'| {name} | {len(rows)} |' for name, rows in query_results.items()]
    lines += ['', '## Scope and limitations', '',
              'pandas consumes generated source CSVs; dbt uses separate committed fixtures. Their totals are not expected to match.',
              'Operations metrics describe seeded demonstration telemetry, not the current run.',
              'Power BI rendering, DAX execution, Snowflake deployment/refresh, access controls, and new screenshots remain unverified.',
              'See metrics.json for complete query outputs and logs/ for execution evidence.']
    (output / 'verification.md').write_text('\n'.join(lines) + '\n')
    print((logs / 'pytest.log').read_text())
    print('\n'.join(lines))
    print(f'Verified local demo: {output / "verification.md"}')


if __name__ == '__main__':
    main()
