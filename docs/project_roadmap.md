# Project Roadmap

## Project Vision

A portfolio analytics platform showing end-to-end data engineering and BI skills: medallion architecture, dbt modeling, dimensional design, and Power BI semantic modeling. Built on a foundation of real professional experience (see [real_world_context.md](real_world_context.md)).

## Completed

- Synthetic data generator (6 sources, deterministic, relational integrity validated)
- Local medallion prototype in Python (Bronze / Silver / Gold + observability outputs)
- dbt warehouse: 21 models, ~38 tests, all passing — runs on DuckDB (CI) or Snowflake (dbt Cloud)
- Staging → intermediate → marts layering with surrogate keys and unknown members
- Power BI semantic model as code (PBIP / TMDL): 11 tables, ~28 DAX measures, relationships
- Power BI report: 7 pages built, connected live to Snowflake
- GitHub Actions CI (data generation → local pipeline → dbt build + tests → pytest)
- Medallion design, data quality and observability design, business metrics definitions

## Ongoing

- Learn dbt well enough to extend the existing models and explain design decisions in interviews
- Add German localization to README once German improves (broadens visibility on local job boards)