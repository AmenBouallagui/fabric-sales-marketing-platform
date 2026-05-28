# Notebooks

This folder will contain Microsoft Fabric notebook examples for ingestion, transformation, validation, and curated table creation.

## Planned Notebooks

- `01_bronze_ingestion.md`: future Fabric notebook outline for reading source CSVs, adding ingestion metadata, validating required columns, and writing Bronze Delta tables.
- `02_silver_transformations.md`: future Fabric notebook outline for cleaning, standardizing, type-casting, deduplicating, validating, and writing Silver Delta tables.
- `03_gold_modeling.md`: future Fabric notebook outline for building Gold dimensions, facts, surrogate keys, date dimension, and validation summaries.
- Data quality validation.
- Exploratory analytics checks.

## Development Notes

Notebook logic should be easy to map to Fabric Lakehouse tables and should avoid embedding secrets or workspace-specific identifiers.
