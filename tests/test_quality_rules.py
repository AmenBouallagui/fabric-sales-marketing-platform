"""Invalid source values must not reach Gold; orphan keys must still resolve."""
import importlib.util
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('medallion', ROOT / 'local_pipeline/run_local_medallion.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


def test_orders_reject_missing_dates_and_nonpositive_quantities():
    frame = pd.DataFrame({'order_id':['a','b','c','d'], 'customer_id':['c']*4,
                          'product_id':['p']*4, 'payment_status':['Paid']*4,
                          'order_date':[pd.Timestamp('2024-01-01')]*3+[pd.NaT],
                          'quantity':[1,0,-2,1], 'total_amount':[10]*4,
                          'unit_price':[10]*4, 'discount_amount':[0]*4, 'tax_amount':[0]*4})
    issues = pipeline.validation_issues('orders', frame)
    assert issues.tolist() == ['', 'invalid quantity', 'invalid quantity', 'missing order_date']
