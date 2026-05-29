# Architecture

## Overview

The AI-Ready Sales & Marketing Data Platform is designed as a Microsoft Fabric portfolio implementation that turns synthetic customers, products, campaigns, orders, ad spend, and support tickets into governed analytics products. The architecture uses a lakehouse-first pattern so raw files, transformed tables, curated metrics, and Power BI consumption can be managed in one coherent environment.

See `assets/architecture_diagram.md` for the Mermaid architecture diagram.

## Target Flow

1. Synthetic source files are generated locally for customers, products, campaigns, orders, ad spend, and support tickets.
2. Raw files are landed into a Bronze area with minimal transformation.
3. Silver transformations standardize schemas, clean values, enforce keys, and apply data quality checks.
4. Gold tables expose dimensional models and business metrics for reporting.
5. Power BI consumes curated Gold tables through a semantic model.
6. AI-ready documentation, metadata, and quality rules make curated data easier to search, explain, and safely reuse.

## Logical Layers

### Bronze

Bronze stores raw source extracts in their original shape. Files should be partitioned by domain and load date where useful. This layer preserves traceability and supports replaying transformations.

### Silver

Silver stores conformed business entities. It standardizes identifiers, dates, status values, monetary values, categorical fields, and relationships across customers, products, campaigns, orders, ad spend, and support tickets.

### Gold

Gold stores analytics-ready facts and dimensions. These tables are designed for Power BI, KPI definitions, and future AI-assisted analysis.

### Observability

Observability outputs capture pipeline run status, data quality results, freshness signals, and row count reconciliation. These outputs support production-style monitoring and future operations reporting.

## Key Design Principles

- Separate raw, cleaned, and curated data responsibilities.
- Keep business metric definitions close to the semantic model.
- Treat data quality as a first-class platform capability.
- Avoid secrets and environment-specific configuration in the repository.
- Make every dataset explainable enough for portfolio review and AI grounding.
