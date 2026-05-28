# Notebooks

This folder will contain Microsoft Fabric notebook examples for ingestion, transformation, validation, and curated table creation.

## Planned Notebooks

- `01_bronze_ingestion.md`: future Fabric notebook outline for reading source CSVs, adding ingestion metadata, validating required columns, and writing Bronze Delta tables.
- Silver standardization and cleansing.
- Data quality validation.
- Gold dimensional model creation.
- Exploratory analytics checks.

## Development Notes

Notebook logic should be easy to map to Fabric Lakehouse tables and should avoid embedding secrets or workspace-specific identifiers.
