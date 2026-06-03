# Fabric Workspace Setup

## Purpose

This guide describes the recommended Microsoft Fabric workspace setup for implementing the portfolio project after the local prototype has been validated.

## Create Or Select A Workspace

Create or select a development workspace for the project. A suggested name is:

`ws-fabric-sales-marketing-dev`

Use a workspace where you have permission to create Fabric items such as Lakehouses, notebooks, pipelines, and SQL endpoint or Warehouse validation assets.

## Capacity And License Note

Microsoft Fabric availability depends on the tenant configuration, licensing, capacity, and workspace settings available to the user. Review current Microsoft Fabric requirements in your environment before implementation. This repository does not include tenant-specific configuration, capacity IDs, workspace IDs, or credentials.

## Suggested Workspace Organization

Recommended workspace items for the first Fabric implementation phase:

- Lakehouse: `lh_sales_marketing_bronze`
- Lakehouse: `lh_sales_marketing_silver`
- Lakehouse: `lh_sales_marketing_gold`
- Notebook: `nb_01_bronze_ingestion`
- Optional pipeline: `pl_bronze_ingestion`
- Optional environment item for notebook dependencies
- Optional Warehouse or SQL endpoint validation artifacts

For a compact portfolio demo, these items can remain in one development workspace. For a production implementation, separate workspaces or deployment stages should be considered.

## Git Integration Note

If Fabric Git integration is enabled in the workspace, connect it carefully to the repository branch intended for Fabric assets. Keep generated data, credentials, personal workspace IDs, and environment-specific settings out of Git.

## Environment Separation

For future dev/test/prod separation, use clear naming conventions and avoid hard-coded workspace or Lakehouse references in notebooks. Parameterize paths, load dates, and run identifiers where possible.

## Security Note

Do not store secrets, tenant IDs, workspace IDs, connection strings, service principal credentials, or personal access tokens in this repository. Use Fabric-supported secure configuration patterns when the implementation requires protected values.
