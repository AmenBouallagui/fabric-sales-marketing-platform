-- Order fact. Surrogate FKs resolve against dimensions; unresolved keys fall back
-- to the '-1' unknown member. Measures mirror the local pipeline's build_gold.
with orders as (
    select * from {{ ref('int_orders_validated') }}
    where dq_status = 'valid'
),

product_cost as (
    select product_id, product_key, unit_cost
    from {{ ref('dim_product') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} as order_key,
    o.order_id,
    coalesce(c.customer_key, '-1')                     as customer_key,
    coalesce(p.product_key, '-1')                      as product_key,
    coalesce(cmp.campaign_key, '-1')                   as campaign_key,
    coalesce(cast({{ to_date_key('o.order_date') }} as integer), -1) as order_date_key,
    o.quantity,
    o.unit_price,
    o.discount_amount,
    o.tax_amount,
    o.total_amount,
    round(o.total_amount - o.tax_amount, 2)            as net_revenue,
    round(o.quantity * p.unit_cost, 2)                 as estimated_cost,
    round((o.total_amount - o.tax_amount) - (o.quantity * p.unit_cost), 2) as gross_margin,
    o.payment_status,
    o.refund_flag
from orders o
left join {{ ref('dim_customer') }} c on o.customer_id = c.customer_id
left join product_cost p on o.product_id = p.product_id
left join {{ ref('dim_campaign') }} cmp on o.campaign_id = cmp.campaign_id
