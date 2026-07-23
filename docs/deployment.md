# Deployment

## Overview

This project runs in two environments: locally (DuckDB, zero credentials) and in the cloud (dbt Cloud + Snowflake, Power BI Desktop connected live). The repository contains code, documentation, and configuration patterns; environment-specific secrets stay outside source control.

## Local Development

- Generate synthetic source data.
- Run the dbt project against the DuckDB target, or the pandas medallion pipeline.
- Execute tests (`dbt build`, `pytest`).
- Generated files stay out of Git (ignored under `data/`).

## Cloud Deployment (dbt Cloud + Snowflake)

1. Create a Snowflake account/database and a dbt Cloud project connected to it.
2. Add a Snowflake target/environment in dbt Cloud (see `dbt/profiles.yml` for the local equivalent).
3. Run `dbt seed` then `dbt build` in dbt Cloud against the Snowflake target.
4. Open `powerbi/SalesMarketing.pbip` in Power BI Desktop and refresh — it connects live to the `SALES_MARKETING.MARTS` schema via Power BI's native Snowflake connector.

## Configuration

Do not commit secrets, connection strings, tokens, or account identifiers. Snowflake credentials live in dbt Cloud's environment settings and Power BI Desktop's cached connection, not in source control.

## Release Readiness Checklist

- Documentation is up to date.
- Data generator can recreate test inputs.
- `dbt build` passes on both DuckDB and Snowflake targets.
- Power BI screenshots reflect current metrics.
- No secrets or generated large data files are committed.