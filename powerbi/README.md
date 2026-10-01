# Power BI

Open [SalesMarketing.pbip](SalesMarketing.pbip), the single supported project. Its [report](SalesMarketing.Report/) contains seven pages; the [semantic model](SalesMarketing.SemanticModel/) contains 11 imported data tables and a disconnected measure table.

Configure the Snowflake parameters and authenticate in Power BI Desktop before refreshing. Eight business tables come from marts, and three operations tables come from seeded observability fixtures. See the [build guide](report_build_guide.md), [model notes](semantic_model_notes.md), and [metric definitions](../docs/business_metrics.md).

Earlier ExecutiveStyle and Redesign projects and the obsolete parquet exporter are preserved in Git history. The supported model uses Snowflake Import. The [historical screenshot](report_screenshots/executive_overview.webp) and existing [demo recording](report_screenshots/executive_overview.mp4) shows an earlier refresh; KPI definitions have since been corrected.
