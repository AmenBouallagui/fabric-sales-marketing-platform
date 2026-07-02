-- Singular data test: net revenue (total minus tax) should never be negative
-- for a paid, non-refunded order. Returns offending rows; the test fails if any.
select
    order_id,
    total_amount,
    tax_amount,
    net_revenue
from {{ ref('fct_orders') }}
where net_revenue < 0
  and payment_status = 'Paid'
  and not refund_flag
