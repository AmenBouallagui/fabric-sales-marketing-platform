# SQL

[business_metric_queries.sql](business_metric_queries.sql) validates the current dbt `marts.fct_*` model and observability seeds. Run after dbt seed/build in DuckDB or Snowflake. It uses string campaign keys, paid non-refunded sales, and separate fact aggregation before campaign joins.

[reference/fabric/](reference/fabric/) preserves future Fabric Warehouse T-SQL designs (DDL and validation). Those scripts use `fact_*` naming and BIGINT surrogate keys to match the independent pandas prototype. They are reference designs, not migrations for the dbt model and are not executed by CI.
