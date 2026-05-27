# Data Generation

## Purpose

This folder contains the deterministic synthetic source data generator for the AI-Ready Sales & Marketing Data Platform. The generated files simulate operational source extracts that can be landed into a Microsoft Fabric Bronze layer.

The data is fully synthetic and designed for portfolio demonstration, local development, and repeatable ingestion testing.

## Output Files

By default, the generator writes CSV files to `data/source/`:

- `customers.csv`
- `products.csv`
- `campaigns.csv`
- `orders.csv`
- `ad_spend.csv`
- `support_tickets.csv`

Generated CSV files are ignored by Git through `.gitignore`. Do not commit generated data files.

## How To Run

Install dependencies from the repository root:

```bash
pip install -r requirements.txt
```

Run the generator with default settings:

```bash
python data_generation/generate_source_data.py
```

## Example Command

```bash
python data_generation/generate_source_data.py --output-dir data/source --seed 42 --customers 1000 --orders 10000 --start-date 2024-01-01 --end-date 2025-12-31
```

## CLI Options

- `--output-dir`: output folder for generated CSV files. Defaults to `data/source`.
- `--seed`: deterministic random seed. Defaults to `42`.
- `--customers`: number of customer rows. Defaults to `1000`.
- `--orders`: number of order rows. Defaults to `10000`.
- `--start-date`: inclusive data start date. Defaults to `2024-01-01`.
- `--end-date`: inclusive data end date. Defaults to `2025-12-31`.

## Fabric Usage Notes

The files are shaped as source-system extracts for Bronze ingestion. They include stable IDs, related business entities, event dates, and `updated_at` timestamps to support future incremental loading patterns in Microsoft Fabric.

The generator intentionally includes realistic imperfect patterns such as refunded orders, failed payments, inactive customers, open support tickets, ended campaigns, and ongoing campaigns.
