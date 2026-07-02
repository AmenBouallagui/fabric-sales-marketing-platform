with source as (
    select * from {{ source('raw', 'campaigns') }}
),

cleaned as (
    select
        cast(campaign_id as varchar)                      as campaign_id,
        trim(campaign_name)                               as campaign_name,
        trim(channel)                                     as channel,
        cast(campaign_start_date as date)                 as campaign_start_date,
        cast(campaign_end_date as date)                   as campaign_end_date,
        trim(target_segment)                              as target_segment,
        trim(objective)                                   as objective,
        cast(updated_at as timestamp)                     as source_updated_at
    from source
)

select * from cleaned
