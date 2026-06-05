# Project Roadmap

## Project Vision

This project demonstrates an Analytics Engineering and BI platform pattern using a Microsoft Fabric-style medallion architecture. It combines an executable local prototype with practical design and implementation guides for future Fabric, Power BI, and AI/Data Agent work.

The project is designed for portfolio review: it shows local working code today and a realistic path toward Fabric lakehouse implementation later.

## Completed Milestones

- Initial repository scaffold.
- Synthetic data generator.
- Local medallion prototype.
- Bronze ingestion design.
- Silver transformation design.
- Gold dimensional model design.
- Data quality and observability design.
- Power BI semantic model and report design.
- GitHub Actions CI.
- Portfolio roadmap, review checklist, and architecture diagram.
- Microsoft Fabric implementation setup guides.
- Repo-friendly Fabric notebook source for Bronze, Silver, and Gold.

## Current Capabilities

- Generate deterministic synthetic source CSVs.
- Run a local medallion pipeline with Bronze, Silver, Gold, and observability outputs.
- Validate the local prototype with pytest.
- Run CI on pull requests and pushes to main.
- Review Fabric setup guides for workspace, Lakehouse, source upload, notebook setup, and SQL validation.
- Review repo-friendly Fabric notebook source under fabric_notebooks/.
- Review Power BI semantic model and report design documentation.

## Prepared But Not Executed In Fabric

- Fabric workspace setup guide.
- Lakehouse setup guide.
- Source file upload guide.
- Bronze notebook setup guide.
- SQL endpoint validation guide.
- Fabric Bronze notebook source.
- Fabric Silver notebook source.
- Fabric Gold notebook source.

Actual Fabric execution remains future/planned unless documented later.

## Planned Fabric Implementation Milestones

- Create Fabric workspace and Lakehouses.
- Land generated source CSVs into Lakehouse Files.
- Implement and execute Fabric Bronze ingestion notebook.
- Validate Bronze tables using the SQL endpoint and sql/bronze_validation_queries.sql.
- Evaluate Data Factory orchestration for repeatable Bronze ingestion.
- Implement and execute Fabric Silver transformation notebook with validation and deduplication.
- Implement and execute Fabric Gold dimensional modeling notebook or Warehouse objects.
- Add observability tables and validation result logging.
- Orchestrate layer execution with Data Factory pipelines.

## Planned Power BI Milestones

- Build Power BI semantic model over Gold tables.
- Create measures for revenue, margin, marketing, customer, support, and data health KPIs.
- Build report pages for executive overview, revenue, marketing, customer, product, support, and operations.
- Capture report screenshots for portfolio presentation.
- Add a short demo walkthrough.

## Planned AI/Data Agent Extension

- Document business glossary and metric definitions.
- Create a question-and-answer evaluation set.
- Connect an AI/Data Agent to curated Gold data once Fabric implementation exists.
- Validate natural-language answers against SQL or Power BI measures.
- Document limitations, permissions, and governance assumptions.

## Recommended Next Portfolio Tasks

- Record a 3-5 minute demo video.
- Add terminal output examples or screenshots showing the local prototype running.
- Add future Power BI mockup or screenshots once available.
- Document real Fabric execution once completed.
- Prepare outreach materials for Analytics Engineer, BI Developer, and Data Analyst roles.

## Suggested Next Engineering Tasks

- Execute the Bronze notebook in an actual Fabric workspace.
- Validate Bronze tables using SQL endpoint queries.
- Execute Silver and Gold notebook sources in Fabric.
- Add observability notebook sources.
- Add Data Factory orchestration design or implementation notes.
