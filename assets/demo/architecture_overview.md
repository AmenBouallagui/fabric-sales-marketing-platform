# Demo Architecture Overview

This diagram separates what runs locally today from the planned Microsoft Fabric, Power BI, and AI/Data Agent implementation path.

```mermaid
flowchart LR
    subgraph LocalToday["Runs Locally Today"]
        Sources["Synthetic CSV sources<br/>customers, products, campaigns,<br/>orders, ad spend, support tickets"]
        Generator["Local data generation<br/>Python + Faker"]
        Bronze["Local Bronze parquet outputs<br/>source records + ingestion metadata"]
        Silver["Local Silver parquet outputs<br/>standardized, typed, deduplicated,<br/>validated current records"]
        Gold["Local Gold parquet outputs<br/>dimensions, facts, KPI-ready fields"]
        Observability["Local observability outputs<br/>run logs, quality results,<br/>row count reconciliation"]
    end

    subgraph PlannedFabric["Planned Microsoft Fabric Implementation"]
        Lakehouse["Microsoft Fabric Lakehouse<br/>Files + Delta tables"]
        FabricBronze["Planned Bronze Delta tables"]
        FabricSilver["Planned Silver Delta tables"]
        FabricGold["Planned Gold tables or Warehouse objects"]
        FabricObs["Planned observability tables"]
    end

    subgraph PlannedConsumption["Planned Consumption"]
        SemanticModel["Planned Power BI semantic model"]
        Reports["Planned Power BI report pages"]
        Agent["Planned AI/Data Agent extension"]
    end

    Sources --> Generator
    Generator --> Bronze
    Bronze --> Silver
    Silver --> Gold
    Bronze --> Observability
    Silver --> Observability
    Gold --> Observability

    Sources -.planned upload.-> Lakehouse
    Lakehouse --> FabricBronze
    FabricBronze --> FabricSilver
    FabricSilver --> FabricGold
    FabricBronze --> FabricObs
    FabricSilver --> FabricObs
    FabricGold --> FabricObs

    FabricGold --> SemanticModel
    FabricObs --> SemanticModel
    SemanticModel --> Reports
    SemanticModel --> Agent
```

The local prototype is executable today. Microsoft Fabric execution, Power BI report creation, and the AI/Data Agent extension are planned unless a later implementation note documents otherwise.
