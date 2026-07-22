{#
  Portable Title Case for categorical normalization (e.g. "in PROGRESS" -> "In Progress").
  DuckDB has no initcap(), so we lower-case, split on spaces, and capitalize each word.
  Snowflake, Postgres, and BigQuery all have a native INITCAP()/initcap(), so use that
  directly there instead.
#}
{% macro title_case(column) %}
  {% if target.type == 'duckdb' %}
    array_to_string(
        list_transform(
            string_split(lower(trim({{ column }})), ' '),
            w -> upper(w[1]) || w[2:]
        ),
        ' '
    )
  {% else %}
    initcap(trim({{ column }}))
  {% endif %}
{% endmacro %}