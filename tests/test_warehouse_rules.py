"""Exercise intermediate rules against the built warehouse inside a rollback."""
import os
from pathlib import Path
import duckdb
import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def warehouse():
    path = Path(os.environ.get('DBT_DUCKDB_PATH', str(ROOT / 'dbt/target/sales_marketing.duckdb')))
    if not path.exists():
        pytest.skip('Run dbt seed/build first to exercise warehouse regressions')
    con = duckdb.connect(str(path))
    con.execute('BEGIN TRANSACTION')
    try:
        yield con
    finally:
        con.execute('ROLLBACK')
        con.close()


def test_invalid_orders_are_rejected_by_warehouse(warehouse):
    for key, expression in [('REG-ZERO', '0 AS quantity'), ('REG-NEGATIVE', '-1 AS quantity'), ('REG-DATE', 'NULL AS order_date')]:
        warehouse.execute(f"INSERT INTO raw.orders SELECT * REPLACE ('{key}' AS order_id, {expression}) FROM raw.orders LIMIT 1")
    rows = warehouse.execute("SELECT order_id, dq_status, dq_issue_reason FROM intermediate.int_orders_validated WHERE order_id LIKE 'REG-%' ORDER BY order_id").fetchall()
    assert rows == [('REG-DATE', 'rejected', 'missing order_date'), ('REG-NEGATIVE', 'rejected', 'invalid quantity'), ('REG-ZERO', 'rejected', 'invalid quantity')]


def test_tied_updates_choose_same_record_regardless_of_input_order(warehouse):
    def insert(amounts):
        for amount in amounts:
            warehouse.execute(f"INSERT INTO raw.orders SELECT * REPLACE ('REG-TIE' AS order_id, '2099-01-01 00:00:00' AS updated_at, {amount} AS total_amount) FROM raw.orders WHERE order_id <> 'REG-TIE' LIMIT 1")
    insert([10, 20])
    first = warehouse.execute("SELECT total_amount FROM intermediate.int_orders_validated WHERE order_id = 'REG-TIE'").fetchall()
    warehouse.execute("DELETE FROM raw.orders WHERE order_id = 'REG-TIE'")
    insert([20, 10])
    second = warehouse.execute("SELECT total_amount FROM intermediate.int_orders_validated WHERE order_id = 'REG-TIE'").fetchall()
    assert first == second
    assert first in [[(10.0,)], [(20.0,)]]
