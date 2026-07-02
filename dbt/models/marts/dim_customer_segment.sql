-- Conformed segment dimension built from distinct valid customer segments.
with segments as (
    select distinct customer_segment
    from {{ ref('int_customers_validated') }}
    where dq_status = 'valid'
      and customer_segment is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_segment']) }} as customer_segment_key,
    customer_segment
from segments
