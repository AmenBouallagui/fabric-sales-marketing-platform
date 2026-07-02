with source as (
    select * from {{ source('raw', 'orders') }}
),

cleaned as (
    select
        cast(order_id as varchar)                         as order_id,
        cast(customer_id as varchar)                      as customer_id,
        cast(product_id as varchar)                       as product_id,
        cast(campaign_id as varchar)                      as campaign_id,
        cast(order_date as date)                          as order_date,
        cast(quantity as integer)                         as quantity,
        round(cast(unit_price as double), 2)              as unit_price,
        round(cast(discount_amount as double), 2)         as discount_amount,
        round(cast(tax_amount as double), 2)              as tax_amount,
        round(cast(total_amount as double), 2)            as total_amount,
        {{ title_case('payment_status') }}                as payment_status,
        lower(trim(cast(refund_flag as varchar))) in ('true', '1', 'yes', 'y', 't') as refund_flag,
        cast(updated_at as timestamp)                     as source_updated_at
    from source
)

select * from cleaned
