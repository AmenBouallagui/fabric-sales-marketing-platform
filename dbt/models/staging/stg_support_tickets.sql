with source as (
    select * from {{ source('raw', 'support_tickets') }}
),

cleaned as (
    select
        cast(ticket_id as varchar)                        as ticket_id,
        cast(customer_id as varchar)                      as customer_id,
        cast(created_at as timestamp)                     as created_at,
        cast(closed_at as timestamp)                      as closed_at,
        trim(priority)                                    as priority,
        trim(category)                                    as category,
        {{ title_case('status') }}                        as status,
        cast(satisfaction_score as integer)               as satisfaction_score,
        cast(first_response_minutes as integer)           as first_response_minutes,
        cast(resolution_minutes as integer)               as resolution_minutes,
        cast(updated_at as timestamp)                     as source_updated_at
    from source
)

select * from cleaned
