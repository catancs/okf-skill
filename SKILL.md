# Open Knowledge Format (OKF) Skill

You are an AI agent working with the **Open Knowledge Format (OKF)** — an open specification for representing knowledge as plain markdown files with YAML frontmatter. OKF bundles are portable, version-controllable, human-readable, and agent-friendly.

## When to Use This Skill

Use OKF whenever you need to:
- **Document data systems** — tables, datasets, APIs, metrics, schemas
- **Build or maintain a knowledge base** — wikis, documentation, runbooks
- **Create agent-consumable context** — structured knowledge for LLMs
- **Exchange knowledge across tools** — Obsidian, Notion, GitHub, agents

## The OKF Spec (v0.1) — Quick Reference

### Bundle Structure

An OKF bundle is a directory of markdown files:

```
my-bundle/
├── index.md              # Optional. Directory listing for progressive disclosure.
├── log.md                # Optional. Chronological update history.
├── concept.md            # A concept at the bundle root.
└── subdirectory/
    ├── index.md
    └── concept.md
```

### Concept Document Format

Every `.md` file (except `index.md` and `log.md`) is a **concept**. Each has YAML frontmatter + markdown body:

```markdown
---
type: BigQuery Table            # REQUIRED — the concept type
title: Customer Orders          # Recommended — display name
description: One row per order  # Recommended — one-line summary
resource: https://...           # Optional — canonical URI for the asset
tags: [sales, orders]           # Optional — cross-cutting tags
timestamp: 2026-05-28T14:30:00Z # Optional — last modified ISO 8601
---

# Schema

| Column     | Type   | Description                     |
|------------|--------|---------------------------------|
| `order_id` | STRING | Unique order identifier.        |
| `customer_id` | STRING | FK to [customers](/tables/customers.md). |

# Joins

Joined with [customers](/tables/customers.md) on `customer_id`.

# Citations

[1] [BigQuery docs](https://console.cloud.google.com/...)
```

### Rules

1. **`type` is the only required field.** Everything else is recommended.
2. **Reserved filenames**: `index.md` and `log.md` — do not use as concept names.
3. **Cross-links** use standard markdown: `[text](/path/to/concept.md)` (absolute) or `[text](./relative.md)` (relative).
4. **Consumers must be tolerant** — broken links, missing fields, unknown types are all allowed. Don't reject bundles, handle gracefully.
5. **Tags are freeform** — no central registry. Pick descriptive strings.
6. **Timestamps use ISO 8601** — `YYYY-MM-DDTHH:MM:SSZ` format.

### Concept Types (suggested, not exhaustive)

| Type | Use For |
|------|---------|
| `Dataset` | A collection of related tables/views |
| `Table` | A database table or view |
| `API Endpoint` | A REST/gRPC endpoint |
| `Metric` | A business or technical metric |
| `Playbook` | An operational procedure |
| `Runbook` | Incident response steps |
| `Reference` | External documentation or glossary |
| `Concept` | An abstract idea or definition |
| `Pipeline` | A data processing pipeline |
| `Dashboard` | A monitoring or analytics dashboard |

Producers may define any type. Consumers must tolerate unknown types.

## Python Module Usage

Import the `okf` module for programmatic access:

```python
import okf

# Read a bundle
root, concepts = okf.read_bundle("./my-bundle")

# Validate
result = okf.validate("./my-bundle")
# Returns: {"valid": True, "concept_count": 12, "errors": [], "warnings": [...]}

# Query
results = okf.query("./my-bundle", type="Table", tags=["revenue"])
# Returns: [{"concept_id": "tables/orders", "type": "Table", ...}]

# Lint
report = okf.lint("./my-bundle")
# Returns: {"clean": True, "concept_count": 12, "issues": [...]}

# Get a single concept
concept = okf.get_concept("./my-bundle", "tables/orders")
# Returns: {"concept_id": "tables/orders", "type": "Table", "body": "...", ...}

# Find backlinks
backlinks = okf.find_backlinks("./my-bundle", "tables/orders")

# Get graph for visualization
graph = okf.get_graph("./my-bundle")
# Returns: {"nodes": [...], "edges": [...]}

# Create a new concept
okf.create_concept(
    "./my-bundle",
    "tables/events",
    type="Table",
    title="Events",
    description="Raw event stream",
    tags=["events", "streaming"],
)

# Generate/update index.md
okf.scaffold_index("./my-bundle", directory=".")
```

## CLI Usage

Shell out for structured JSON output:

```bash
# Validate
okf validate ./my-bundle

# Lint
okf lint ./my-bundle

# Query
okf query ./my-bundle --type Table --tag revenue

# Show a concept
okf show ./my-bundle tables/orders

# Get the concept graph
okf graph ./my-bundle

# Create a new concept
okf create ./my-bundle tables/events --type Table --title "Events"

# Generate index.md
okf index ./my-bundle
```

All commands output JSON by default.

## Workflows

### Producing an OKF Bundle (from scratch)

1. Create the bundle directory.
2. Create `index.md` at the root.
3. Organize concepts into subdirectories by domain.
4. Write each concept with frontmatter + body.
5. Cross-link concepts using markdown links.
6. Run `okf validate` and `okf lint` to check health.

```python
import okf

# Create concepts
okf.create_concept("./my-bundle", "datasets/sales", type="Dataset", title="Sales", description="Sales data")
okf.create_concept("./my-bundle", "tables/orders", type="Table", title="Orders", description="Order records")
okf.create_concept("./my-bundle", "metrics/revenue", type="Metric", title="Revenue", description="Total revenue")

# Generate indexes
okf.scaffold_index("./my-bundle")
okf.scaffold_index("./my-bundle", directory="datasets")
okf.scaffold_index("./my-bundle", directory="tables")

# Validate
result = okf.validate("./my-bundle")
print(f"Valid: {result['valid']}, Concepts: {result['concept_count']}")
```

### Enriching an Existing Bundle

When adding knowledge from external sources:

1. Read the existing bundle to understand structure.
2. Check if the concept already exists (query by type + title).
3. If exists: update frontmatter fields, append new body content, add citations.
4. If new: create with `okf.create_concept()`.
5. Update cross-links in related concepts.
6. Run `okf lint` to check for orphans or broken links.

### Consuming a Bundle (agent context)

When an agent needs to understand a knowledge base:

1. Read `index.md` for the top-level overview.
2. Drill into relevant subdirectories.
3. Read specific concepts for detailed information.
4. Follow cross-links to related concepts.
5. Check `# Citations` for source material.

### Linting / Health Checks

Run periodically to keep the bundle healthy:

```python
report = okf.lint("./my-bundle")
for issue in report["issues"]:
    print(f"[{issue['severity']}] {issue['category']}: {issue['message']}")
```

Common issues:
- **Orphan**: No inbound links — add from index or related concepts
- **Missing index**: Directory has concepts but no `index.md`
- **Stale**: No timestamp — add `timestamp` to frontmatter
- **Structure**: Missing description — add for discoverability

## Integration Patterns

### With Obsidian

OKF bundles are Obsidian-compatible. Open the bundle directory as an Obsidian vault. Cross-links become Obsidian links. Graph view shows the knowledge graph.

### With Notion

Export Notion databases to markdown, then add OKF frontmatter. Use `okf.create_concept()` to wrap each page.

### With GitHub

Commit bundles to repos. Use GitHub Actions to run `okf validate` and `okf lint` on PRs. Knowledge changes go through code review.

### With Agent Pipelines

```python
import okf

# Agent reads bundle for context
_, concepts = okf.read_bundle("./knowledge")
relevant = [c for c in concepts if c.type == "Table" and "orders" in (c.description or "").lower()]

# Agent produces new knowledge
okf.create_concept("./knowledge", "tables/new_analysis", type="Table", title="New Analysis", description="...")

# Agent validates its output
result = okf.validate("./knowledge")
assert result["valid"], f"Bundle invalid: {result['errors']}"
```

## Tips for Agents

1. **Always validate after writing** — run `okf.validate()` or `okf validate` to catch issues.
2. **Use descriptive types** — "BigQuery Table" is better than "Table" when context matters.
3. **Cross-link liberally** — links are how agents navigate knowledge.
4. **Add descriptions** — they're used in indexes and search.
5. **Timestamps matter** — without them, consumers can't tell if knowledge is stale.
6. **Keep body content structured** — headings, tables, and lists are easier for agents to parse than prose.
7. **Use `index.md` for progressive disclosure** — agents shouldn't need to load the entire bundle.
8. **Don't fight the format** — OKF is intentionally minimal. Work with markdown, not against it.
