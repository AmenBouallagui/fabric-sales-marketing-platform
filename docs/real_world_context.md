# Professional Context

This portfolio project is built on top of real professional experience. The patterns used here — medallion ingestion, metadata-driven pipelines, Power BI semantic modeling — come from hands-on client work, not purely from tutorials.

## Background

2 years of part-time work (20 h/week) at a small BI consulting firm providing architecture and reporting solutions to enterprise clients. Primary technology stack: Microsoft Fabric, Power BI, Azure, Dataverse.

## Representative Work

### Metadata-Driven Data Migration (Largest Project)

Migrated data from a client's Dataverse environment and Azure Data Lake into a Microsoft Fabric workspace.

- **Access granted:** SQL endpoints for both Dataverse and the Fabric lakehouse
- **Migration scope:** Views and tables from Dataverse → Fabric-managed lakehouse tables
- **Approach:** Metadata-driven pipeline — a single parameterized pipeline driven by a configuration table listing source objects, target names, transformation rules, and load strategies. Adding a new entity to migrate required only a new config row, not a new pipeline
- **Deliverables:** Fully documented pipeline, migration validation queries, reconciliation outputs confirming row counts and key field integrity across environments

This is the direct real-world analogue to the metadata patterns and observability outputs in this portfolio project's local pipeline.

### Power BI Development

Worked across multiple client Power BI reports from data source to published visual:

- Connected and shaped sources using Power Query (M)
- Authored DAX measures for business KPIs (revenue, margin, activity metrics)
- Fixed and implemented custom visuals, drill-throughs, bookmarks, and filters
- Diagnosed performance issues and corrected broken relationships and filter contexts

### View Rebuilding & Diagnostics

- Rebuilt and maintained SQL views in client Azure SQL and Fabric SQL endpoint environments
- Ran diagnostic queries on data quality issues, identified root causes, and proposed fixes
- Supported data validation during migration checkpoints

## How This Relates to the Portfolio Project

| Portfolio Component | Real-World Foundation |
|---|---|
| Local medallion pipeline observability | Reconciliation and run logging used in the Dataverse migration |
| Metadata-driven pipeline pattern | Parameterized migration pipeline design |
| Power BI semantic model (TMDL) | Hands-on Power Query, DAX, and report development |
| Fabric notebook source + setup guides | Direct experience with Fabric workspace, SQL endpoints, lakehouse access |
| SQL validation queries | Diagnostic queries used in production migration validation |

The portfolio extends these patterns into a clean, runnable, fully documented reference implementation.
