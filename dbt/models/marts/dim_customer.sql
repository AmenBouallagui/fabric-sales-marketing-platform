-- Customer dimension. Only current, valid Silver records become real members;
-- an "unknown" member (key = '-1') absorbs facts whose FK cannot be resolved,
-- which keeps referential-integrity tests green without dropping fact rows.
with customers as (
    select * from {{ ref('int_customers_validated') }}
    where dq_status = 'valid'
),

members as (
    select
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,
        customer_id,
        customer_name,
        email,
        country,
        city,
        customer_segment,
        company_size,
        industry,
        acquisition_channel,
        status,
        signup_date
    from customers
),

unknown_member as (
    select
        '-1'        as customer_key,
        'UNKNOWN'   as customer_id,
        'Unknown'   as customer_name,
        null        as email,
        'Unknown'   as country,
        'Unknown'   as city,
        'Unknown'   as customer_segment,
        'Unknown'   as company_size,
        'Unknown'   as industry,
        'Unknown'   as acquisition_channel,
        'Unknown'   as status,
        null        as signup_date
)

select * from members
union all
select * from unknown_member
