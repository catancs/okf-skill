---
type: Table
title: Products
description: Product catalog with names, categories, and pricing.
resource: https://console.cloud.google.com/bigquery?project=demo&dataset=sales&table=products
tags: [products, catalog, inventory]
timestamp: 2026-06-15T10:00:00Z
---

# Schema

| Column         | Type      | Description                                    |
|----------------|-----------|------------------------------------------------|
| `product_id`   | STRING    | Globally unique product identifier.            |
| `name`         | STRING    | Product display name.                          |
| `category`     | STRING    | Product category (e.g. `electronics`, `apparel`). |
| `price_usd`    | NUMERIC   | Unit price in US dollars.                      |
| `in_stock`     | BOOL      | Whether the product is currently available.    |

# Relationships

- Referenced by [orders](/tables/orders.md) via `product_id`

# Citations

[1] [BigQuery e-commerce demo](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset)
