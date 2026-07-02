{#
  Portable Title Case for categorical normalization (e.g. "in PROGRESS" -> "In Progress").
  DuckDB has no initcap(), so we lower-case, split on spaces, and capitalize each word.
  Swap the body for initcap() on Snowflake/Postgres or INITCAP() on BigQuery.
#}
{% macro title_case(column) %}
    array_to_string(
        list_transform(
            string_split(lower(trim({{ column }})), ' '),
            w -> upper(w[1]) || w[2:]
        ),
        ' '
    )
{% endmacro %}
