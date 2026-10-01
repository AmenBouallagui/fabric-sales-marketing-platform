# Portfolio review checklist

1. Read the [README](../README.md) for project scope and executable quick start.
2. Inspect the [architecture diagram](../assets/architecture_diagram.md), which separates pandas from dbt inputs and outputs.
3. Run the README commands, including **dbt seed before dbt build**, then pytest.
4. Review [metric definitions](business_metrics.md) and run [SQL metric queries](../sql/business_metric_queries.sql) against the DuckDB marts.
5. Open the primary [Power BI project](../powerbi/SalesMarketing.pbip) in Desktop after configuring its Snowflake parameters; see the [build guide](../powerbi/report_build_guide.md).
6. Review [quality limitations](data_quality_observability.md) and the [roadmap](project_roadmap.md).

CI verifies the DuckDB warehouse and Python pipeline. Power BI Desktop rendering, cloud refresh, DAX execution, access controls, and live telemetry are separate validation steps; source inspection does not establish that these work in a fresh deployment.
