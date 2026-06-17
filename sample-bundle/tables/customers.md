---
type: Table
title: Customers
description: Customer account records with profile and contact information.
resource: https://console.cloud.google.com/bigquery?project=demo&dataset=sales&table=customers
tags: [customers, users, accounts]
timestamp: 2026-06-15T10:00:00Z
---

# Schema

| Column         | Type      | Description                                    |
|----------------|-----------|------------------------------------------------|
| `customer_id`  | STRING    | Globally unique customer identifier.           |
| `name`         | STRING    | Customer display name.                         |
| `email`        | STRING    | Customer email address (PII).                  |
| `created_at`   | TIMESTAMP | When the account was created.                  |
| `country`      | STRING    | Customer country code (ISO 3166-1 alpha-2).    |

# Relationships

- Has many [orders](/tables/orders.md) via `customer_id`
- Part of the [users](/datasets/users.md) dataset

# Citations

[1] [BigQuery e-commerce demo](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset)
