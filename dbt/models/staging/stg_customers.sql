with source as (
    select * from {{ source('raw', 'customers') }}
),

cleaned as (
    select
        cast(customer_id as varchar)                      as customer_id,
        cast(account_id as varchar)                       as account_id,
        trim(customer_name)                               as customer_name,
        lower(trim(email))                                as email,
        trim(country)                                     as country,
        trim(city)                                        as city,
        cast(signup_date as date)                         as signup_date,
        trim(acquisition_channel)                         as acquisition_channel,
        trim(customer_segment)                            as customer_segment,
        trim(company_size)                                as company_size,
        trim(industry)                                    as industry,
        -- normalize status casing to Title Case (mirrors silver normalize_categories)
        {{ title_case('status') }}                        as status,
        cast(updated_at as timestamp)                     as source_updated_at
    from source
)

select * from cleaned
