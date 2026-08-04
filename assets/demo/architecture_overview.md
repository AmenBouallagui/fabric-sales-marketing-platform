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
        Reports["7 report pages<br/>live-connected to Snowflake"]
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
```

The local prototype and the dbt warehouse (both targets) are executable today; the Power BI report is built and connected live.
