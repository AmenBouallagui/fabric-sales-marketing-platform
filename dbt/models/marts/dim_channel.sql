-- Conformed channel dimension unioning every channel seen across customer
-- acquisition, campaigns, and ad spend.
with channels as (
    select acquisition_channel as channel
    from {{ ref('int_customers_validated') }}
    where dq_status = 'valid' and acquisition_channel is not null

    union
    select channel
    from {{ ref('int_campaigns_validated') }}
    where dq_status = 'valid' and channel is not null

    union
    select channel
    from {{ ref('int_ad_spend_validated') }}
    where dq_status = 'valid' and channel is not null
),

members as (
    select
        {{ dbt_utils.generate_surrogate_key(['channel']) }} as channel_key,
        channel,
        channel as channel_group
    from channels
),

unknown_member as (
    select '-1' as channel_key, 'Unknown' as channel, 'Unknown' as channel_group
)

select * from members
union all
select * from unknown_member
