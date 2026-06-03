# Source File Upload Guide

## Purpose

This guide explains how to generate local synthetic source files and map them to future Microsoft Fabric Lakehouse Files paths for Bronze ingestion.

## Generate Local Source Files

Run the local data generator from the repository root:

```bash
python data_generation/generate_source_data.py
```

The generator writes source CSV extracts under:

```text
data/source/
```

Generated files are intentionally ignored by Git.

## Upload Mapping

Use the selected load date in each target path.

| Local file | Target Lakehouse Files path |
| --- | --- |
| `data/source/customers.csv` | `Files/source/synthetic_crm/customers/load_date=YYYY-MM-DD/customers.csv` |
| `data/source/products.csv` | `Files/source/synthetic_crm/products/load_date=YYYY-MM-DD/products.csv` |
| `data/source/orders.csv` | `Files/source/synthetic_crm/orders/load_date=YYYY-MM-DD/orders.csv` |
| `data/source/support_tickets.csv` | `Files/source/synthetic_crm/support_tickets/load_date=YYYY-MM-DD/support_tickets.csv` |
| `data/source/campaigns.csv` | `Files/source/synthetic_marketing/campaigns/load_date=YYYY-MM-DD/campaigns.csv` |
| `data/source/ad_spend.csv` | `Files/source/synthetic_marketing/ad_spend/load_date=YYYY-MM-DD/ad_spend.csv` |

## Manual Upload Option

For the first Fabric implementation pass, manually upload the generated CSVs through the Fabric Lakehouse Files interface. This keeps the setup simple and makes it easy to inspect paths before the Bronze notebook is built.

## Future Automated Upload Option

Later iterations can automate file landing with a pipeline, OneLake file copy process, or deployment script. Automation should preserve the same source system, entity, and load date path conventions.

## Verification Checklist

- Each expected CSV file exists under `data/source/`.
- Each file is uploaded to the correct source system and entity folder.
- The `load_date=YYYY-MM-DD` folder matches the intended load date.
- File names are unchanged from the generator output.
- No generated CSV files are committed to Git.
- The Bronze notebook parameters match the uploaded load date and base source path.
