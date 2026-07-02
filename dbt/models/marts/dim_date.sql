-- Date dimension covering the full span of business dates in the data.
-- Uses DuckDB's generate_series; on Snowflake/BigQuery swap for dbt_utils.date_spine.
with bounds as (
    select
        min(d) as min_date,
        max(d) as max_date
    from (
        select order_date as d from {{ ref('int_orders_validated') }} where order_date is not null
        union all
        select spend_date from {{ ref('int_ad_spend_validated') }} where spend_date is not null
        union all
        select signup_date from {{ ref('int_customers_validated') }} where signup_date is not null
        union all
        select campaign_start_date from {{ ref('int_campaigns_validated') }} where campaign_start_date is not null
        union all
        select campaign_end_date from {{ ref('int_campaigns_validated') }} where campaign_end_date is not null
        union all
        select cast(created_at as date) from {{ ref('int_support_tickets_validated') }} where created_at is not null
    )
),

spine as (
    select cast(unnest(generate_series(min_date, max_date, interval 1 day)) as date) as calendar_date
    from bounds
)

select
    cast(strftime(calendar_date, '%Y%m%d') as integer) as date_key,
    calendar_date,
    extract(year from calendar_date)                   as calendar_year,
    extract(quarter from calendar_date)                as calendar_quarter,
    extract(month from calendar_date)                  as calendar_month,
    strftime(calendar_date, '%B')                      as month_name,
    extract(day from calendar_date)                    as day_of_month,
    strftime(calendar_date, '%A')                      as day_of_week,
    extract(dow from calendar_date) in (0, 6)          as is_weekend
from spine

union all

-- unknown date member for facts with missing/unparseable dates
select -1, null, null, null, null, 'Unknown', null, 'Unknown', false
