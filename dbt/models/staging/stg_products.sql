with source as (
    select * from {{ source('raw', 'products') }}
),

cleaned as (
    select
        cast(product_id as varchar)                       as product_id,
        trim(product_name)                                as product_name,
        trim(category)                                    as category,
        trim(plan_tier)                                   as plan_tier,
        round(cast(unit_price as double), 2)              as unit_price,
        round(cast(unit_cost as double), 2)               as unit_cost,
        -- normalize boolean-like values (true/1/yes/y/t)
        lower(trim(cast(is_subscription as varchar))) in ('true', '1', 'yes', 'y', 't') as is_subscription,
        cast(valid_from as date)                          as valid_from,
        cast(valid_to as date)                            as valid_to,
        cast(updated_at as timestamp)                     as source_updated_at
    from source
)

select * from cleaned
