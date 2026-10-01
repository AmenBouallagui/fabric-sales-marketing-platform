"""Regression for campaign fact fanout and the public sales KPI contract."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]


def test_campaign_roas_filters_and_fact_grains():
    con = duckdb.connect()
    con.execute('CREATE SCHEMA marts')
    con.execute('CREATE TABLE marts.dim_campaign (campaign_key VARCHAR, campaign_id VARCHAR, campaign_name VARCHAR, channel VARCHAR)')
    con.execute("INSERT INTO marts.dim_campaign VALUES ('a', 'A', 'Same name', 'Email'), ('b', 'B', 'Same name', 'Email'), ('z', 'Z', 'Zero spend', 'Email'), ('-1', 'UNKNOWN', 'Unknown', 'Unknown')")
    con.execute('CREATE TABLE marts.fct_orders (campaign_key VARCHAR, total_amount DOUBLE, payment_status VARCHAR, refund_flag BOOLEAN)')
    con.execute("INSERT INTO marts.fct_orders VALUES ('a',100,'Paid',false),('a',200,'Paid',false),('a',500,'Failed',false),('a',600,'Pending',false),('a',700,'Paid',true),('b',20,'Paid',false),('-1',999,'Paid',false)")
    con.execute('CREATE TABLE marts.fct_ad_spend (campaign_key VARCHAR, spend_amount DOUBLE)')
    con.execute("INSERT INTO marts.fct_ad_spend VALUES ('a',10),('a',20),('a',30),('b',10),('z',0)")
    sql = (ROOT / 'sql/business_metric_queries.sql').read_text()
    query = sql[sql.index('WITH campaign_revenue'):sql.index('-- Ad spend and conversions')]
    rows = {r[0]: r for r in con.execute(query).fetchall()}
    assert rows['a'][3:] == (300.0, 60.0, 5.0)
    assert rows['b'][3:] == (20.0, 10.0, 2.0)
    assert rows['z'][5] is None
    assert '-1' not in rows
    con.close()
