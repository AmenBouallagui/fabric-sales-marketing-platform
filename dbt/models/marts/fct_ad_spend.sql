with ad_spend as (
    select * from {{ ref('int_ad_spend_validated') }}
    where dq_status = 'valid'
)

select
    {{ dbt_utils.generate_surrogate_key(['a.spend_id']) }} as ad_spend_key,
    a.spend_id,
    coalesce(cmp.campaign_key, '-1')                   as campaign_key,
    coalesce(ch.channel_key, '-1')                     as channel_key,
    coalesce(cast(strftime(a.spend_date, '%Y%m%d') as integer), -1) as spend_date_key,
    a.impressions,
    a.clicks,
    a.conversions,
    a.spend_amount
from ad_spend a
left join {{ ref('dim_campaign') }} cmp on a.campaign_id = cmp.campaign_id
left join {{ ref('dim_channel') }} ch on a.channel = ch.channel
