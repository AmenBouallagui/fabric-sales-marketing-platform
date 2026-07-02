# dbt Warehouse (DuckDB)

A dbt project that transforms the synthetic sales & marketing extracts into a
tested, documented star schema. It is the warehouse-native counterpart to the
Microsoft Fabric medallion design in this repo: the same Bronze → Silver → Gold
logic, expressed in dbt with sources, staging, intermediate, and marts layers.

DuckDB is used as the warehouse so the whole project runs locally and in CI with
**no cloud account or credentials**. The modeling patterns (sources, layered
refs, surrogate keys, schema/relationship/accepted-value tests, exposures, docs)
transfer directly to Snowflake, BigQuery, or Databricks — see *Portability* below.

## Layers

| Layer | Path | Materialization | Purpose |
|-------|------|-----------------|---------|
| Sources | `models/staging/_sources.yml` | external CSV | The six generated extracts read directly via dbt-duckdb |
| Staging | `models/staging/` | view | Type casting, trimming, category/boolean normalization (one model per source) |
| Intermediate | `models/intermediate/` | view | Silver: dedupe to latest record per business key + data-quality flagging (`dq_status`) |
| Marts | `models/marts/` | table | Gold: conformed dimensions (with unknown members), a date dimension, and order / ad-spend / support fact tables with derived measures |

## Run it

From the **repository root** (so the `data/source/*.csv` paths resolve):

```bash
pip install -r requirements.txt
python data_generation/generate_source_data.py        # produce the source CSVs
export DBT_PROFILES_DIR=dbt                            # Windows PowerShell: $env:DBT_PROFILES_DIR='dbt'
dbt deps   --project-dir dbt
dbt build  --project-dir dbt                           # run + test all models
dbt docs generate --project-dir dbt && dbt docs serve --project-dir dbt   # lineage graph
```

`dbt build` runs all models and the full test suite (uniqueness, not-null,
referential integrity between facts and dimensions, accepted values, and a
singular net-revenue test). The DuckDB file and `target/` artifacts are gitignored.

## Tests

- **Generic tests** in `models/**/_*.yml`: `unique`, `not_null`, `relationships`
  (fact → dimension foreign keys), `accepted_values` (status / payment-status domains).
- **Singular test** in `tests/`: asserts paid, non-refunded orders never have
  negative net revenue.

## Portability

- Surrogate keys use `dbt_utils.generate_surrogate_key` (warehouse-agnostic).
- `dim_date` uses DuckDB's `generate_series`; swap for `dbt_utils.date_spine` on
  cloud warehouses.
- Title-case normalization uses the `title_case` macro (`macros/title_case.sql`)
  because DuckDB lacks `initcap()`; replace its body with `initcap()` /
  `INITCAP()` on Postgres/Snowflake/BigQuery.
- To target a cloud warehouse, add an output to `profiles.yml` and run with
  `--target`. No model changes are required beyond the two notes above.

## Relationship to the rest of the repo

- `data_generation/` produces the source CSVs this project reads.
- `local_pipeline/run_local_medallion.py` is the pandas reference implementation
  of the same Bronze/Silver/Gold logic.
- `fabric_notebooks/` holds the PySpark equivalent for a Microsoft Fabric Lakehouse.
- The `sales_marketing_powerbi` exposure documents the planned Power BI semantic
  model that consumes these gold tables.
