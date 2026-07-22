with tickets as (
    select * from {{ ref('int_support_tickets_validated') }}
    where dq_status = 'valid'
)

select
    {{ dbt_utils.generate_surrogate_key(['t.ticket_id']) }} as ticket_key,
    t.ticket_id,
    coalesce(c.customer_key, '-1')                     as customer_key,
    coalesce(cast({{ to_date_key('t.created_at') }} as integer), -1) as created_date_key,
    cast({{ to_date_key('t.closed_at') }} as integer)   as closed_date_key,
    t.priority,
    t.category,
    t.status,
    t.satisfaction_score,
    t.first_response_minutes,
    t.resolution_minutes
from tickets t
left join {{ ref('dim_customer') }} c on t.customer_id = c.customer_id
