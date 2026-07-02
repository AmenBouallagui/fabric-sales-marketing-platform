with products as (
    select * from {{ ref('int_products_validated') }}
    where dq_status = 'valid'
),

members as (
    select
        {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,
        product_id,
        product_name,
        category,
        plan_tier,
        unit_price,
        unit_cost,
        is_subscription,
        valid_from,
        valid_to
    from products
),

unknown_member as (
    select
        '-1'        as product_key,
        'UNKNOWN'   as product_id,
        'Unknown'   as product_name,
        'Unknown'   as category,
        'Unknown'   as plan_tier,
        cast(0 as double)  as unit_price,
        cast(0 as double)  as unit_cost,
        false       as is_subscription,
        null        as valid_from,
        null        as valid_to
)

select * from members
union all
select * from unknown_member
