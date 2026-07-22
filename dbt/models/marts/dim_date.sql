-- Date dimension covering the full span of business dates in the data.
-- Generates the calendar-day spine with DuckDB's generate_series locally,
-- or Snowflake's GENERATOR/SEQ4 pattern when targeting Snowflake.
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
{% if target.type == 'duckdb' %}
    select cast(unnest(generate_series(min_date, max_date, interval 1 day)) as date) as calendar_date
    from bounds
{% else %}
    select calendar_date
    from (
        select cast(dateadd(day, seq4(), min_date) as date) as calendar_date
        from bounds, table(generator(rowcount => 100000))
    )
    where calendar_date <= (select max_date from bounds)
{% endif %}
)

select
{% if target.type == 'duckdb' %}
    cast(strftime(calendar_date, '%Y%m%d') as integer) as date_key,
    calendar_date,
    extract(year from calendar_date)                   as calendar_year,
    extract(quarter from calendar_date)                 as calendar_quarter,
    extract(month from calendar_date)                   as calendar_month,
    strftime(calendar_date, '%B')                       as month_name,
    extract(day from calendar_date)                     as day_of_month,
    strftime(calendar_date, '%A')                       as day_of_week,
    extract(dow from calendar_date) in (0, 6)           as is_weekend
{% else %}
    cast(to_char(calendar_date, 'YYYYMMDD') as integer) as date_key,
    calendar_date,
    extract(year from calendar_date)                    as calendar_year,
    extract(quarter from calendar_date)                 as calendar_quarter,
    extract(month from calendar_date)                   as calendar_month,
    case extract(month from calendar_date)
        when 1 then 'January' when 2 then 'February' when 3 then 'March'
        when 4 then 'April' when 5 then 'May' when 6 then 'June'
        when 7 then 'July' when 8 then 'August' when 9 then 'September'
        when 10 then 'October' when 11 then 'November' when 12 then 'December'
    end                                                  as month_name,
    extract(day from calendar_date)                      as day_of_month,
    case dayofweek(calendar_date)
        when 0 then 'Sunday' when 1 then 'Monday' when 2 then 'Tuesday'
        when 3 then 'Wednesday' when 4 then 'Thursday' when 5 then 'Friday'
        when 6 then 'Saturday'
    end                                                   as day_of_week,
    dayofweek(calendar_date) in (0, 6)                   as is_weekend
{% endif %}
from spine

union all

-- unknown date member for facts with missing/unparseable dates
select -1, null, null, null, null, 'Unknown', null, 'Unknown', false