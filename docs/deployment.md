# Deployment

## Overview

This project is intended to be portable between local development and a Microsoft Fabric workspace. The repository should contain code, documentation, and lightweight configuration patterns, while environment-specific settings remain outside source control.

## Local Development

Local work will focus on:

- Generating synthetic source data.
- Running transformation logic in notebooks or scripts.
- Executing tests.
- Reviewing documentation and SQL assets.

Generated files should stay out of Git unless explicitly approved for a small sample dataset.

## Fabric Workspace Setup

Planned Fabric setup steps:

1. Create or select a Fabric workspace.
2. Create a Lakehouse for the project.
3. Create logical folders for Bronze, Silver, and Gold data.
4. Upload or ingest synthetic source data into Bronze.
5. Import notebooks and SQL scripts.
6. Configure pipelines for repeatable orchestration.
7. Build or connect a Power BI semantic model to Gold tables.

## Configuration

Do not commit secrets, connection strings, tokens, or tenant-specific identifiers. Use Fabric workspace settings, environment variables, or secure deployment parameters where needed.

## Release Readiness Checklist

- Documentation is up to date.
- Data generator can recreate test inputs.
- Transformations are repeatable.
- Data quality checks pass.
- Power BI screenshots reflect current metrics.
- No secrets or generated large data files are committed.
