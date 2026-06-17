# okf — Open Knowledge Format Toolkit

A Python toolkit for creating, validating, querying, and linting [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) bundles.

## Install

```bash
uv venv .venv --python 3.12
uv pip install -e ".[dev]"
```

## Usage

### As a Python module

```python
import okf

# Validate
result = okf.validate("./my-bundle")

# Query
results = okf.query("./my-bundle", type="Table", tags=["revenue"])

# Lint
report = okf.lint("./my-bundle")

# Create
okf.create_concept("./my-bundle", "tables/orders", type="Table", title="Orders")

# Generate index
okf.scaffold_index("./my-bundle")
```

### As a CLI

```bash
okf validate ./my-bundle
okf lint ./my-bundle
okf query ./my-bundle --type Table
okf show ./my-bundle tables/orders
okf create ./my-bundle tables/events --type Table --title "Events"
okf index ./my-bundle
```

## SKILL.md

See [SKILL.md](SKILL.md) for the comprehensive agent guide — the OKF spec, workflows, and integration patterns.

## Sample Bundle

See [sample-bundle/](sample-bundle/) for a working OKF bundle documenting an e-commerce data system.

## License

MIT
