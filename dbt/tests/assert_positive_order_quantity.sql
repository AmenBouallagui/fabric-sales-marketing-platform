-- Validated orders must have a usable quantity and transaction date.
select order_id
from {{ ref('int_orders_validated') }}
where dq_status = 'valid'
  and (quantity is null or quantity <= 0 or order_date is null)
