with deduplicated as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by campaign_id
                order by source_updated_at desc nulls last,
                         {{ dbt_utils.generate_surrogate_key(['campaign_id', 'campaign_name', 'channel', 'campaign_start_date', 'campaign_end_date', 'target_segment', 'objective', 'source_updated_at']) }} desc
            ) as _rn
        from {{ ref('stg_campaigns') }}
    )
    where _rn = 1
),

flagged as (
    select
        * exclude (_rn),
        case
            when campaign_id is null then 'missing campaign_id'
            when channel is null then 'missing channel'
            when campaign_start_date is null then 'missing campaign_start_date'
            when channel not in (
                'Paid Search', 'Paid Social', 'Organic', 'Email', 'Referral', 'Partner', 'Direct'
            ) then 'invalid campaign channel'
        end as dq_issue_reason
    from deduplicated
)

select
    *,
    case when dq_issue_reason is null then 'valid' else 'rejected' end as dq_status
from flagged
