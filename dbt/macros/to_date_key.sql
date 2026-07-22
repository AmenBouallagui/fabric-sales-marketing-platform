{#
  Portable YYYYMMDD date-key formatting. DuckDB uses strftime; Snowflake/Postgres/
  BigQuery use to_char with a numeric format model (safe and unambiguous, unlike
  month/day name formatting).
#}
{% macro to_date_key(column) %}
  {% if target.type == 'duckdb' %}
    strftime({{ column }}, '%Y%m%d')
  {% else %}
    to_char({{ column }}, 'YYYYMMDD')
  {% endif %}
{% endmacro %}