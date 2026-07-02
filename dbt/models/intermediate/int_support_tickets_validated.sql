with deduplicated as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by ticket_id
                order by source_updated_at desc nulls last
            ) as _rn
        from {{ ref('stg_support_tickets') }}
    )
    where _rn = 1
),

flagged as (
    select
        * exclude (_rn),
        case
            when ticket_id is null then 'missing ticket_id'
            when customer_id is null then 'missing customer_id'
            when created_at is null then 'missing created_at'
            when status is null then 'missing status'
            when status not in ('Closed', 'Resolved', 'Open', 'In Progress') then 'invalid support ticket status'
        end as dq_issue_reason
    from deduplicated
)

select
    *,
    case when dq_issue_reason is null then 'valid' else 'rejected' end as dq_status
from flagged
