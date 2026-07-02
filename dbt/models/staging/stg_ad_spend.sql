with source as (
    select * from {{ source('raw', 'ad_spend') }}
),

cleaned as (
    select
        cast(spend_id as varchar)                         as spend_id,
        cast(campaign_id as varchar)                      as campaign_id,
        cast(spend_date as date)                          as spend_date,
        trim(channel)                                     as channel,
        cast(impressions as integer)                      as impressions,
        cast(clicks as integer)                           as clicks,
        cast(conversions as integer)                      as conversions,
        round(cast(spend_amount as double), 2)            as spend_amount,
        cast(updated_at as timestamp)                     as source_updated_at
    from source
)

select * from cleaned
