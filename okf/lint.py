"""Lint OKF bundles — find orphans, stale content, missing structure, health issues."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from okf.parse import RESERVED_FILENAMES, Concept, list_concepts, read_bundle


@dataclass
class LintIssue:
    """A lint finding."""

    severity: str  # "error" | "warning" | "info"
    category: str  # "orphan", "broken_link", "missing_index", "stale", "structure"
    message: str
    concept_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
        }
        if self.concept_id:
            d["concept_id"] = self.concept_id
        return d


@dataclass
class LintResult:
    """Result of linting an OKF bundle."""

    clean: bool
    concept_count: int
    issues: list[LintIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "clean": self.clean,
            "concept_count": self.concept_count,
            "issue_count": len(self.issues),
            "issues": [i.to_dict() for i in self.issues],
        }


def lint_bundle(bundle_path: str | Path) -> LintResult:
    """Lint an OKF bundle for common health issues.

    Checks:
    - Orphan concepts (no inbound links from other concepts)
    - Directories without index.md
    - Missing timestamps (staleness risk)
    - Concepts without descriptions (poor discoverability)
    - Duplicate concept IDs
    - Unused tags (tags used only once)
    """
    root = Path(bundle_path).resolve()
    concepts = list_concepts(root)
    issues: list[LintIssue] = []

    # Build link graph
    inbound_links: dict[str, list[str]] = defaultdict(list)
    all_tags: dict[str, list[str]] = defaultdict(list)

    for concept in concepts:
        for link in concept.links:
            if link.startswith("/"):
                target = link.lstrip("/").replace(".md", "")
            else:
                concept_dir = concept.path.parent
                target_path = (concept_dir / link).resolve()
                try:
                    target = str(target_path.relative_to(root)).replace(".md", "")
                except ValueError:
                    continue
            inbound_links[target].append(concept.concept_id)

        for tag in concept.tags:
            all_tags[tag.lower()].append(concept.concept_id)

    # 1. Find orphan concepts (no inbound links, not root index)
    for concept in concepts:
        if concept.is_index or concept.is_log:
            continue
        if concept.concept_id not in inbound_links:
            # Root-level concepts without inbound links are orphans
            # unless they're referenced from index.md
            index_path = root / "index.md"
            if index_path.exists():
                index_content = index_path.read_text(encoding="utf-8")
                if concept.concept_id in index_content or (concept.title or "") in index_content:
                    continue
            issues.append(LintIssue(
                severity="warning",
                category="orphan",
                message=f"No inbound links to '{concept.title or concept.concept_id}'",
                concept_id=concept.concept_id,
            ))

    # 2. Check for directories without index.md
    dirs_with_concepts = set()
    for concept in concepts:
        rel = concept.path.relative_to(root)
        for parent in rel.parents:
            if parent != Path("."):
                dirs_with_concepts.add(root / parent)

    for dir_path in dirs_with_concepts:
        index_file = dir_path / "index.md"
        if not index_file.exists():
            rel_dir = dir_path.relative_to(root)
            issues.append(LintIssue(
                severity="info",
                category="missing_index",
                message=f"Directory '{rel_dir}' has concepts but no index.md",
            ))

    # 3. Missing timestamps
    for concept in concepts:
        if concept.is_index or concept.is_log:
            continue
        if not concept.timestamp:
            issues.append(LintIssue(
                severity="info",
                category="stale",
                message=f"Missing timestamp — cannot determine freshness",
                concept_id=concept.concept_id,
            ))

    # 4. Missing descriptions
    for concept in concepts:
        if concept.is_index or concept.is_log:
            continue
        if not concept.description:
            issues.append(LintIssue(
                severity="info",
                category="structure",
                message=f"Missing description — poor discoverability in index/search",
                concept_id=concept.concept_id,
            ))

    # 5. Duplicate concept IDs
    seen_ids: dict[str, str] = {}
    for concept in concepts:
        if concept.concept_id in seen_ids:
            issues.append(LintIssue(
                severity="error",
                category="structure",
                message=f"Duplicate concept ID: '{concept.concept_id}' (first at {seen_ids[concept.concept_id]})",
                concept_id=concept.concept_id,
            ))
        else:
            seen_ids[concept.concept_id] = str(concept.path)

    # 6. Unused tags (tags on only one concept — might be typos or too specific)
    for tag, concept_ids in all_tags.items():
        if len(concept_ids) == 1:
            issues.append(LintIssue(
                severity="info",
                category="structure",
                message=f"Tag '{tag}' used on only 1 concept — consider if it should be broader",
                concept_id=concept_ids[0],
            ))

    return LintResult(
        clean=not any(i.severity == "error" for i in issues),
        concept_count=len(concepts),
        issues=issues,
    )


def lint(bundle_path: str | Path) -> dict[str, Any]:
    """Lint a bundle and return a dict result.

    Convenience wrapper for agents that want dict output.
    """
    return lint_bundle(bundle_path).to_dict()
