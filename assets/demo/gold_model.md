# Demo Gold Model

This diagram summarizes the planned Gold dimensional model used by the local prototype and intended for a future Power BI semantic model.

```mermaid
flowchart TB
    subgraph Dimensions["Gold Dimensions"]
        dim_customer["dim_customer"]
        dim_product["dim_product"]
        dim_campaign["dim_campaign"]
        dim_date["dim_date"]
        dim_customer_segment["dim_customer_segment"]
        dim_channel["dim_channel"]
    end

    subgraph Facts["Gold Facts"]
        fact_orders["fact_orders"]
        fact_ad_spend["fact_ad_spend"]
        fact_support_tickets["fact_support_tickets"]
    end

    fact_orders --> dim_customer
    fact_orders --> dim_product
    fact_orders --> dim_campaign
    fact_orders --> dim_date

    fact_ad_spend --> dim_campaign
    fact_ad_spend --> dim_channel
    fact_ad_spend --> dim_date

    fact_support_tickets --> dim_customer
    fact_support_tickets --> dim_date

    dim_customer --> dim_customer_segment
```

The Gold model supports business-ready measures for revenue, margin, marketing performance, customer analysis, support quality, and data health. Power BI execution is planned unless documented later.
