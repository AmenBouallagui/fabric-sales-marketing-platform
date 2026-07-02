with deduplicated as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by spend_id
                order by source_updated_at desc nulls last
            ) as _rn
        from {{ ref('stg_ad_spend') }}
    )
    where _rn = 1
),

flagged as (
    select
        * exclude (_rn),
        case
            when spend_id is null then 'missing spend_id'
            when campaign_id is null then 'missing campaign_id'
            when spend_amount is null or spend_amount < 0 then 'invalid spend_amount'
            when impressions is null or impressions < 0 then 'invalid impressions'
            when clicks is null or clicks < 0 then 'invalid clicks'
            when conversions is null or conversions < 0 then 'invalid conversions'
        end as dq_issue_reason
    from deduplicated
)

select
    *,
    case when dq_issue_reason is null then 'valid' else 'rejected' end as dq_status
from flagged
