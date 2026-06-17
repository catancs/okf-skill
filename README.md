<div align="center">

# 🧠 OKF Skill

**The Open Knowledge Format skill for coding agents.**

Teaches AI agents to store, retrieve, and manage knowledge using [OKF](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing), an open specification from Google.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Open Knowledge Format](https://img.shields.io/badge/Format-OKF_v0.1-green.svg)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-purple.svg)](#install)
[![Open Source](https://img.shields.io/badge/Open_Source-%E2%9C%93-brightgreen.svg)](#contributing)

<img src="https://www.gstatic.com/images/branding/product/1x/gsa_512dp.png" alt="Google" width="64" style="margin: 16px 0">

</div>

---

## Why this exists

Foundation models are powerful, but they lack **context**. The knowledge agents need (table schemas, API docs, runbooks, metrics) lives in fragmented, incompatible systems. Every agent builder solves the same context-assembly problem from scratch.

**[OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)** is Google's answer: a minimal, vendor-neutral format where knowledge lives as **markdown files with YAML frontmatter**, organized in directories, cross-linked, version-controllable, and readable by both humans and agents.

This skill makes your coding agent **use OKF by default**, so knowledge is structured, portable, and compounds across sessions.

---

## How it works

```mermaid
flowchart LR
    subgraph WITHOUT[" Without OKF"]
        direction TB
        A1[Agent documents database] --> A2[random markdown, no conventions]
        A2 --> A3[next agent starts from scratch]
        A3 --> A4[knowledge lost across sessions]
    end

    subgraph WITH[" With OKF"]
        direction TB
        B1[Agent documents database] --> B2[OKF bundle with structured frontmatter]
        B2 --> B3[next agent reads the bundle]
        B3 --> B4[knowledge versioned, reviewable, portable]
    end

    style WITHOUT fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style WITH fill:#1a1a2e,stroke:#2ecc71,color:#fff
```

---

## OKF in action

**You say:**

> *"Document my Postgres orders table as an OKF bundle"*

**Your agent produces:**

```
knowledge/
├── index.md
├── datasets/
│   ├── index.md
│   └── sales.md
└── tables/
    ├── index.md
    ├── orders.md        <-- this file
    └── customers.md
```

```markdown
---
type:        Table
title:       Orders
description: One row per completed customer order
tags:        [sales, orders]
timestamp:   2026-06-17T00:00:00Z
---

# Schema

| Column       | Type   | Description                          |
|--------------|--------|--------------------------------------|
| order_id     | STRING | Unique order identifier              |
| customer_id  | STRING | FK to customers                      |
| total_usd    | NUMERIC| Order total in USD                   |
| placed_at    | TIMESTAMP | When the order was placed         |

# Related

See customers.md for the join key.
```

**What just happened:**

```mermaid
flowchart LR
    S1["1. Create directory"] --> S2["2. Generate YAML frontmatter"]
    S2 --> S3["3. Write schema table"]
    S3 --> S4["4. Cross-link concepts"]
    S4 --> S5["5. Ready for any agent"]

    style S1 fill:#2d3436,stroke:#0984e3,color:#fff
    style S2 fill:#2d3436,stroke:#0984e3,color:#fff
    style S3 fill:#2d3436,stroke:#0984e3,color:#fff
    style S4 fill:#2d3436,stroke:#0984e3,color:#fff
    style S5 fill:#2d3436,stroke:#00b894,color:#fff
```

---

## Install

From within Claude Code:

```
/plugin marketplace add catancs/okf-skill
/plugin install okf-skill@okf-skill
```

---

## Resources

- **[OKF Specification (v0.1)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)** (the full spec, it's short)
- **[Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)** (the announcement post)
- **[Reference Agent & Samples](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)** (Google's proof-of-concept implementation)
- **[Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** (the pattern that inspired OKF)

---

## Contributing

Open source. Use it, fork it, improve it.

If the OKF spec evolves, update the skill. If you find patterns that work better, share them. The value of a knowledge format comes from adoption, not ownership.

---

<div align="center">

Built by [@catancs](https://github.com/catancs) . MIT licensed

</div>
