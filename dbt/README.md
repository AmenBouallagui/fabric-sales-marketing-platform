# dbt Warehouse (DuckDB)

A dbt project that transforms committed synthetic sales & marketing fixtures into a
tested, documented star schema. It expresses the same Bronze → Silver → Gold
logic as the repo's local pandas prototype, with sources, staging, intermediate,
and marts layers.

DuckDB is used as the warehouse so the whole project runs locally and in CI with
**no cloud account or credentials**. The modeling patterns (sources, layered
refs, surrogate keys, schema/relationship/accepted-value tests, exposures, docs)
can be adapted to other warehouses — see *Portability* below.

## Layers

| Layer | Path | Materialization | Purpose |
|-------|------|-----------------|---------|
| Sources | `models/staging/_sources.yml` | seeded tables | Six committed CSV fixtures loaded into the `raw` schema by `dbt seed` |
| Staging | `models/staging/` | view | Type casting, trimming, category/boolean normalization (one model per source) |
| Intermediate | `models/intermediate/` | view | Silver: dedupe to latest record per business key + data-quality flagging (`dq_status`) |
| Marts | `models/marts/` | table | Gold: conformed dimensions (with unknown members), a date dimension, and order / ad-spend / support fact tables with derived measures |

## Run it

From the **repository root**:

```bash
pip install -r requirements.txt
export DBT_PROFILES_DIR=dbt                            # Windows PowerShell: $env:DBT_PROFILES_DIR='dbt'
dbt deps   --project-dir dbt
dbt seed   --project-dir dbt                           # load raw and observability fixtures first
dbt build  --project-dir dbt                           # run + test all models
dbt docs generate --project-dir dbt && dbt docs serve --project-dir dbt   # lineage graph
```

`dbt build` runs all models and the full test suite (uniqueness, not-null,
referential integrity between facts and dimensions, accepted values, and a
singular net-revenue test). The DuckDB file and `target/` artifacts are gitignored.

### Why seeds run first

The `raw` sources refer to tables loaded from committed CSVs in `dbt/seeds/`.
Sources do not declare a dependency on their seed nodes. On an empty database,
`dbt build` alone can run source tests before seed loading finishes. Running
`dbt seed` separately ensures the source tables exist before any model or test
queries them. The same ordering applies to Snowflake deployments.

The generated CSVs in `data/source/` feed the pandas prototype, not this dbt
project. Observability seeds are demonstration fixtures, not a live feed of
local pipeline runs.

## Tests

- **Generic tests** in `models/**/_*.yml`: `unique`, `not_null`, `relationships`
  (fact → dimension foreign keys), `accepted_values` (status / payment-status domains).
- **Singular test** in `tests/`: asserts paid, non-refunded orders never have
  negative net revenue.

## Portability

DuckDB is the credential-free target configured in `profiles.yml`. Snowflake
requires its adapter, a configured dbt Cloud environment or local profile, and
the same seed-before-build sequence. Snowflake branches are present in the date
and normalization macros. Other warehouses require dialect and adapter review;
they are not validated targets merely because dbt supports them.

Surrogate keys use `dbt_utils.generate_surrogate_key`. Cross-target portability
should be checked with a successful build and tests in each actual environment.

## Relationship to the rest of the repo

- `dbt/seeds/` supplies this project's committed synthetic inputs.
- `data_generation/` produces a separate dataset for the pandas pipeline.
- `local_pipeline/run_local_medallion.py` is the pandas reference implementation
  of the same Bronze/Silver/Gold logic.
- The `sales_marketing_powerbi` exposure documents the Power BI semantic
  model that consumes these gold tables.
