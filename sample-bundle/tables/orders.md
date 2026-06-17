---
type: Table
title: Orders
description: One row per completed customer order across all sales channels.
resource: https://console.cloud.google.com/bigquery?project=demo&dataset=sales&table=orders
tags: [orders, sales, transactions]
timestamp: 2026-06-15T10:00:00Z
---

# Schema

| Column        | Type      | Description                                    |
|---------------|-----------|------------------------------------------------|
| `order_id`    | STRING    | Globally unique order identifier.              |
| `customer_id` | STRING    | FK to [customers](/tables/customers.md).       |
| `product_id`  | STRING    | FK to [products](/tables/products.md).         |
| `quantity`    | INT64     | Number of units ordered.                       |
| `total_usd`   | NUMERIC   | Order total in US dollars.                     |
| `placed_at`   | TIMESTAMP | When the customer submitted the order.         |
| `status`      | STRING    | Order status: `pending`, `shipped`, `delivered`. |

# Joins

- Joined with [customers](/tables/customers.md) on `customer_id`
- Joined with [products](/tables/products.md) on `product_id`

# Example

```sql
SELECT customer_id, SUM(total_usd) AS lifetime_value
FROM `demo.sales.orders`
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 10
```

# Citations

[1] [BigQuery e-commerce demo](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset)
