-- Silver-equivalent: dedupe to the latest record per business key, then flag
-- data-quality status. Marts consume only dq_status = 'valid' rows.
with deduplicated as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by customer_id
                order by source_updated_at desc nulls last,
                         {{ dbt_utils.generate_surrogate_key(['customer_id', 'account_id', 'customer_name', 'email', 'country', 'city', 'signup_date', 'acquisition_channel', 'customer_segment', 'company_size', 'industry', 'status', 'source_updated_at']) }} desc
            ) as _rn
        from {{ ref('stg_customers') }}
    )
    where _rn = 1
),

flagged as (
    select
        * exclude (_rn),
        case
            when customer_id is null then 'missing customer_id'
            when customer_name is null then 'missing customer_name'
            when signup_date is null then 'missing signup_date'
            when status not in ('Active', 'Inactive', 'Churned') then 'invalid customer status'
        end as dq_issue_reason
    from deduplicated
)

select
    *,
    case when dq_issue_reason is null then 'valid' else 'rejected' end as dq_status
from flagged
