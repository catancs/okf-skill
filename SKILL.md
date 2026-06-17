# OKF — Open Knowledge Format Skill

Use the [Open Knowledge Format (OKF)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) when storing, retrieving, or documenting knowledge. OKF makes knowledge portable across agents, tools, and teams.

## What to do

When documenting data systems (databases, APIs, pipelines, metrics) or building a knowledge base, produce OKF-conformant bundles. When reading existing knowledge, prefer OKF bundles.

## File structure

```
knowledge/
├── index.md                  # Root listing of all concepts
├── datasets/
│   ├── index.md
│   └── sales.md
└── tables/
    ├── index.md
    └── orders.md
```

## Concept format

Every `.md` file (except `index.md`) is a concept. Required and recommended frontmatter:

```markdown
---
type: Table                    # REQUIRED — e.g. Table, Dataset, Metric, API, Playbook
title: Orders                  # Recommended — display name
description: Customer orders   # Recommended — one-line summary
resource: https://...          # Optional — canonical URI
tags: [sales, orders]          # Optional — cross-cutting tags
timestamp: 2026-06-17T00:00:00Z # Optional — ISO 8601
---

# Schema
| Column     | Type   | Description                |
|------------|--------|----------------------------|
| `order_id` | STRING | Unique identifier           |

# Related
See [customers](/tables/customers.md) for the join key.
```

## Rules

1. `type` is the only required field. All else is optional.
2. Reserved filenames: `index.md` (directory listing) and `log.md` (changelog). Never use as concept names.
3. Cross-link with markdown: `[text](/path/to/concept.md)` (absolute) or `[text](./relative.md)`.
4. Always add `description` — it's used in indexes and search.
5. Create `index.md` in each directory listing its contents.
6. After writing, verify the bundle is self-consistent — links resolve, types are set, index exists.

## Types (suggested)

| Type | Use for |
|------|---------|
| `Dataset` | Collection of tables or views |
| `Table` | A database table or view |
| `API` | REST/gRPC endpoint |
| `Metric` | Business or technical metric |
| `Playbook` | Operational procedure |
| `Pipeline` | Data processing pipeline |
| `Reference` | External docs or glossary |

Define your own types as needed. Consumers will handle unknown types gracefully.

## Workflow

1. **Document** — When asked to document a system, create an OKF bundle with `index.md` at root, organized by type.
2. **Read** — Before answering questions about a system, check if an OKF bundle exists. Read `index.md` first, then drill into relevant concepts.
3. **Update** — When schemas or systems change, update the relevant concept files and their timestamps.
4. **Cross-reference** — Link related concepts. The value of OKF is in the graph, not the individual files.
