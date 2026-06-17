# 🧠 OKF Skill

> **The Open Knowledge Format skill for coding agents.**

Teaches AI agents to store, retrieve, and manage knowledge using the
[Open Knowledge Format (OKF)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) — an open specification from Google for representing knowledge as portable, agent-friendly markdown bundles.

---

## Why this exists

Foundation models are powerful, but they lack **context**. The knowledge
agents need — table schemas, API docs, runbooks, metrics — lives in
fragmented, incompatible systems. Every agent builder solves the same
context-assembly problem from scratch.

[OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
is Google's answer: a minimal, vendor-neutral format where knowledge lives
as **markdown files with YAML frontmatter**, organized in directories,
cross-linked, version-controllable, and readable by both humans and agents.

This skill makes your coding agent **use OKF by default** — so knowledge
is structured, portable, and compounds across sessions.

## What it does

With this skill loaded, your agent will:

- **Document** data systems as OKF bundles (databases, APIs, pipelines, metrics)
- **Read** existing OKF bundles for context before answering questions
- **Update** knowledge when schemas change, keeping timestamps and cross-links fresh
- **Produce** portable knowledge that works across agents, tools, and teams

## Install

Copy `SKILL.md` into your agent's skill directory:

```bash
# Claude Code
cp SKILL.md ~/.claude/skills/okf/SKILL.md

# OpenCode
cp SKILL.md ~/.config/opencode/skills/okf/SKILL.md

# Or paste it into your CLAUDE.md / AGENTS.md
```

That's it. No dependencies, no install, no framework.

## How it works

The skill is a concise instruction file (~70 lines) that teaches your agent
the OKF conventions — the frontmatter structure, cross-linking rules,
directory organization, and when to use the format.

It doesn't dump the full spec. It gives the agent just enough to produce
conformant bundles and read existing ones.

### Before

```
Agent documents your database → random markdown files, no conventions
Next agent starts from scratch → no context carries over
Knowledge scattered across sessions → lost forever
```

### After

```
Agent documents your database → OKF bundle with structured frontmatter
Next agent reads the bundle → full context, cross-linked
Knowledge lives in git → versioned, reviewable, portable
```

## Example

Ask your agent to document a database:

> "Document my Postgres orders table as an OKF bundle"

The agent produces:

```markdown
---
type: Table
title: Orders
description: One row per completed customer order
tags: [sales, orders]
timestamp: 2026-06-17T00:00:00Z
---

# Schema

| Column     | Type   | Description                     |
|------------|--------|---------------------------------|
| `order_id` | STRING | Unique order identifier         |
| `customer_id` | STRING | FK to [customers](./customers.md) |

# Related

See [customers](./customers.md) for the join key.
```

Cross-linked, typed, timestamped. Ready for any agent to consume.

## Resources

- [OKF Specification (v0.1)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — the full spec (it's short!)
- [Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) — the announcement post
- [Reference Agent & Samples](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) — Google's proof-of-concept implementation
- [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the pattern that inspired OKF

## Contributing

Open source. Use it, fork it, improve it.

If the OKF spec evolves, update the skill. If you find patterns that work
better, share them. The value of a knowledge format comes from adoption,
not ownership.

## License

MIT
