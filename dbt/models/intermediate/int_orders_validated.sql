with deduplicated as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by order_id
                order by source_updated_at desc nulls last
            ) as _rn
        from {{ ref('stg_orders') }}
    )
    where _rn = 1
),

flagged as (
    select
        * exclude (_rn),
        case
            when order_id is null then 'missing order_id'
            when customer_id is null then 'missing customer_id'
            when product_id is null then 'missing product_id'
            when payment_status is null then 'missing payment_status'
            when payment_status not in ('Paid', 'Failed', 'Pending') then 'invalid payment_status'
            when total_amount is null or total_amount < 0 then 'invalid total_amount'
            when unit_price is null or unit_price < 0 then 'invalid unit_price'
            when discount_amount is null or discount_amount < 0 then 'invalid discount_amount'
            when tax_amount is null or tax_amount < 0 then 'invalid tax_amount'
        end as dq_issue_reason
    from deduplicated
)

select
    *,
    case when dq_issue_reason is null then 'valid' else 'rejected' end as dq_status
from flagged
