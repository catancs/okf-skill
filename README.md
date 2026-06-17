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

<table>
<tr>
<td width="50%" align="center">

**Without OKF**

</td>
<td width="50%" align="center">

**With OKF**

</td>
</tr>
<tr>
<td>

```
Agent documents your database
  -> random markdown, no conventions

Next agent starts from scratch
  -> no context carries over

Knowledge scattered across sessions
  -> lost forever
```

</td>
<td>

```
Agent documents your database
  -> OKF bundle, structured frontmatter

Next agent reads the bundle
  -> full context, cross-linked

Knowledge lives in git
  -> versioned, reviewable, portable
```

</td>
</tr>
</table>

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

| Step | What the agent did |
|------|--------------------|
| 1 | Created a structured directory with `index.md` at root |
| 2 | Generated YAML frontmatter with `type`, `title`, `description`, `tags`, `timestamp` |
| 3 | Wrote a schema table with column names, types, and descriptions |
| 4 | Cross-linked to the `customers` concept via markdown link |
| 5 | Ready for any agent (yours or a teammate's) to read and build on |

---

## Install

**Claude Code plugin** (recommended):

```
/plugin marketplace add catancs/okf-skill
/plugin install okf-skill@catancs
```

**Manual** (copy `skills/okf/SKILL.md` into your agent's skill directory):

```bash
# Claude Code
cp skills/okf/SKILL.md ~/.claude/skills/okf/SKILL.md

# OpenCode
cp skills/okf/SKILL.md ~/.config/opencode/skills/okf/SKILL.md

# Or paste into your CLAUDE.md / AGENTS.md
```

That's it. No dependencies, no install, no framework.

---

## Concept types

| Type | Use for |
|------|---------|
| `Dataset` | Collection of tables or views |
| `Table` | A database table or view |
| `API` | REST/gRPC endpoint |
| `Metric` | Business or technical metric |
| `Playbook` | Operational procedure |
| `Pipeline` | Data processing pipeline |
| `Reference` | External docs or glossary |

Define your own types as needed. Consumers handle unknown types gracefully.

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
