with deduplicated as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by product_id
                order by source_updated_at desc nulls last
            ) as _rn
        from {{ ref('stg_products') }}
    )
    where _rn = 1
),

flagged as (
    select
        * exclude (_rn),
        case
            when product_id is null then 'missing product_id'
            when product_name is null then 'missing product_name'
            when unit_price is null or unit_price <= 0 then 'invalid unit_price'
            when unit_cost is null or unit_cost < 0 then 'invalid unit_cost'
        end as dq_issue_reason
    from deduplicated
)

select
    *,
    case when dq_issue_reason is null then 'valid' else 'rejected' end as dq_status
from flagged
