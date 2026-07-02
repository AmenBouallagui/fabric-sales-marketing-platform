with campaigns as (
    select * from {{ ref('int_campaigns_validated') }}
    where dq_status = 'valid'
),

members as (
    select
        {{ dbt_utils.generate_surrogate_key(['campaign_id']) }} as campaign_key,
        campaign_id,
        campaign_name,
        channel,
        campaign_start_date,
        campaign_end_date,
        target_segment,
        objective
    from campaigns
),

unknown_member as (
    select
        '-1'        as campaign_key,
        'UNKNOWN'   as campaign_id,
        'Unknown'   as campaign_name,
        'Unknown'   as channel,
        null        as campaign_start_date,
        null        as campaign_end_date,
        'Unknown'   as target_segment,
        'Unknown'   as objective
)

select * from members
union all
select * from unknown_member
