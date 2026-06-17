"""Parse OKF bundles — read frontmatter, list concepts, walk directory trees."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

RESERVED_FILENAMES = {"index.md", "log.md"}


@dataclass
class Concept:
    """A single OKF concept document."""

    path: Path
    concept_id: str
    frontmatter: dict[str, Any]
    body: str
    raw: str

    @property
    def type(self) -> str | None:
        return self.frontmatter.get("type")

    @property
    def title(self) -> str | None:
        return self.frontmatter.get("title")

    @property
    def description(self) -> str | None:
        return self.frontmatter.get("description")

    @property
    def resource(self) -> str | None:
        return self.frontmatter.get("resource")

    @property
    def tags(self) -> list[str]:
        return self.frontmatter.get("tags", [])

    @property
    def timestamp(self) -> str | None:
        return self.frontmatter.get("timestamp")

    @property
    def links(self) -> list[str]:
        """Extract markdown links to other concepts in the bundle."""
        import re

        # Match [text](/path/to/concept.md) and [text](./relative.md)
        pattern = r"\[([^\]]*)\]\(([^)]+\.md)\)"
        return [m.group(2) for m in re.finditer(pattern, self.body)]

    @property
    def citations(self) -> list[str]:
        """Extract citation URLs from # Citations section."""
        import re

        # Find the Citations section
        match = re.search(r"^#\s+Citations\s*\n(.*?)(?=\n#|\Z)", self.body, re.MULTILINE | re.DOTALL)
        if not match:
            return []
        section = match.group(1)
        url_pattern = r"\[?\[?\d*\]?\]?\((https?://[^)]+)\)"
        return [m.group(1) for m in re.finditer(url_pattern, section)]

    @property
    def is_index(self) -> bool:
        return self.path.name == "index.md"

    @property
    def is_log(self) -> bool:
        return self.path.name == "log.md"


def parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from raw markdown content.

    Returns (frontmatter_dict, body).
    """
    if not raw.startswith("---"):
        return {}, raw

    # Find closing ---
    end = raw.find("---", 3)
    if end == -1:
        return {}, raw

    fm_text = raw[3:end].strip()
    body = raw[end + 3 :].strip()

    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}

    return fm, body


def parse_concept(filepath: Path, bundle_root: Path) -> Concept:
    """Parse a single OKF concept file."""
    raw = filepath.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)

    # Concept ID is path relative to bundle root, without .md
    rel = filepath.relative_to(bundle_root)
    concept_id = str(rel.with_suffix(""))

    return Concept(
        path=filepath,
        concept_id=concept_id,
        frontmatter=fm,
        body=body,
        raw=raw,
    )


def list_concepts(bundle_root: Path) -> list[Concept]:
    """List all concept documents in a bundle (excludes reserved filenames)."""
    concepts = []
    for md_file in sorted(bundle_root.rglob("*.md")):
        if md_file.name in RESERVED_FILENAMES:
            continue
        concepts.append(parse_concept(md_file, bundle_root))
    return concepts


def read_bundle(bundle_path: str | Path) -> tuple[Path, list[Concept]]:
    """Read an OKF bundle and return (root_path, concepts).

    This is the main entry point for agents wanting to work with a bundle.
    """
    root = Path(bundle_path).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Bundle directory not found: {root}")
    return root, list_concepts(root)
