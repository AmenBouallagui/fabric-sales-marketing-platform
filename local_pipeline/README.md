# Local Medallion Prototype

This folder contains a local Python prototype for the AI-Ready Sales & Marketing Data Platform medallion flow.

The prototype runs locally with pandas. Its purpose is to validate the Bronze, Silver, Gold, and observability logic independently of the dbt implementation.

## Inputs

The pipeline reads generated source CSV files from `data/source/`:

- `customers.csv`
- `products.csv`
- `campaigns.csv`
- `orders.csv`
- `ad_spend.csv`
- `support_tickets.csv`

Generate the source files first:

```bash
python data_generation/generate_source_data.py
```

## Outputs

The pipeline writes local parquet outputs under:

- `data/bronze/`
- `data/silver/`
- `data/gold/`
- `data/observability/`

The `data/` folder is ignored by Git, so generated outputs should not be committed.

The local prototype is also validated by GitHub Actions CI using a small generated dataset.

## Run

```bash
python local_pipeline/run_local_medallion.py
```

Optional arguments:

- `--source-dir`: source CSV folder. Defaults to `data/source`.
- `--output-dir`: base output folder. Defaults to `data`.
- `--load-date`: load date in `YYYY-MM-DD` format. Defaults to today.
- `--run-id`: optional run identifier. A local UUID is generated when omitted.

## What It Does

- Builds Bronze parquet files with ingestion metadata and row hashes.
- Builds Silver parquet files with cleaned, typed, deduplicated, validated records.
- Builds Gold dimensions and facts with deterministic surrogate keys.
- Writes local observability outputs for run logging, quality results, and row count reconciliation.
