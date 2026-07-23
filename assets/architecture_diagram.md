# Architecture Diagram

This Mermaid diagram summarizes the two working implementations of the medallion pattern in this repo — a local pandas prototype and a dbt warehouse that runs on DuckDB or Snowflake — both feeding a Power BI report connected live to Snowflake.

```mermaid
flowchart LR
    subgraph Sources["Synthetic Source Extracts"]
        CSV["Source CSVs<br/>customers, products, campaigns,<br/>orders, ad spend, support tickets"]
    end

    subgraph Local["Local Executable Prototype"]
        Generator["Synthetic Data Generator"]
        LocalPipeline["Local Medallion Pipeline<br/>pandas + parquet"]
        Bronze["Bronze Outputs<br/>raw records + ingestion metadata"]
        Silver["Silver Outputs<br/>cleaned, typed, deduplicated records"]
        Gold["Gold Outputs<br/>dimensions, facts, KPIs"]
        Obs["Observability Outputs<br/>run log, quality results,<br/>row count reconciliation"]
    end

    subgraph Warehouse["dbt Warehouse<br/>DuckDB (local) or Snowflake (dbt Cloud)"]
        Staging["Staging Views"]
        Intermediate["Intermediate Views<br/>Silver logic"]
        Marts["Marts Tables<br/>Gold star schema"]
    end

    subgraph Reporting["Power BI"]
        Semantic["Semantic Model (TMDL)<br/>8 tables, ~22 DAX measures"]
        Reports["6 Report Pages<br/>live-connected to Snowflake"]
    end

    Generator --> CSV
    CSV --> LocalPipeline
    LocalPipeline --> Bronze
    Bronze --> Silver
    Silver --> Gold
    LocalPipeline --> Obs

    CSV --> Staging
    Staging --> Intermediate
    Intermediate --> Marts

    Marts --> Semantic
    Semantic --> Reports

    
---

## `assets/demo/architecture_overview.md` — replace entirely

```markdown
# Demo Architecture Overview

This diagram shows the local pandas prototype alongside the dbt warehouse path (DuckDB or Snowflake) that feeds the live-connected Power BI report.

```mermaid
flowchart LR
    subgraph LocalToday["Local Prototype"]
        Sources["Synthetic CSV sources<br/>customers, products, campaigns,<br/>orders, ad spend, support tickets"]
        Generator["Local data generation<br/>Python + Faker"]
        Bronze["Local Bronze parquet outputs<br/>source records + ingestion metadata"]
        Silver["Local Silver parquet outputs<br/>standardized, typed, deduplicated,<br/>validated current records"]
        Gold["Local Gold parquet outputs<br/>dimensions, facts, KPI-ready fields"]
        Observability["Local observability outputs<br/>run logs, quality results,<br/>row count reconciliation"]
    end

    subgraph DbtWarehouse["dbt Warehouse<br/>DuckDB or Snowflake"]
        Staging["Staging views"]
        Intermediate["Intermediate views"]
        Marts["Marts tables"]
    end

    subgraph Consumption["Power BI"]
        SemanticModel["Semantic model (TMDL)"]
        Reports["6 report pages<br/>live-connected to Snowflake"]
    end

    Sources --> Generator
    Generator --> Bronze
    Bronze --> Silver
    Silver --> Gold
    Bronze --> Observability
    Silver --> Observability
    Gold --> Observability

    Sources --> Staging
    Staging --> Intermediate
    Intermediate --> Marts

    Marts --> SemanticModel
    SemanticModel --> Reports