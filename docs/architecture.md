# Architecture

## Overview

The AI-Ready Sales & Marketing Data Platform is designed as a Microsoft Fabric portfolio implementation that turns fragmented commercial data into governed analytics products. The architecture uses a lakehouse-first pattern so raw files, transformed tables, curated metrics, and Power BI consumption can be managed in one coherent environment.

## Target Flow

1. Source-like synthetic files are generated locally for CRM, marketing, product, and revenue domains.
2. Raw files are landed into a Bronze area with minimal transformation.
3. Silver transformations standardize schemas, clean values, enforce keys, and apply data quality checks.
4. Gold tables expose dimensional models and business metrics for reporting.
5. Power BI consumes curated Gold tables through a semantic model.
6. AI-ready documentation, metadata, and quality rules make curated data easier to search, explain, and safely reuse.

## Logical Layers

### Bronze

Bronze stores raw source extracts in their original shape. Files should be partitioned by domain and load date where useful. This layer preserves traceability and supports replaying transformations.

### Silver

Silver stores conformed business entities. It standardizes identifiers, dates, status values, currencies, and relationships across sales and marketing processes.

### Gold

Gold stores analytics-ready facts and dimensions. These tables are designed for Power BI, KPI definitions, and future AI-assisted analysis.

## Key Design Principles

- Separate raw, cleaned, and curated data responsibilities.
- Keep business metric definitions close to the semantic model.
- Treat data quality as a first-class platform capability.
- Avoid secrets and environment-specific configuration in the repository.
- Make every dataset explainable enough for portfolio review and AI grounding.
