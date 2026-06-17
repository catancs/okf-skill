"""Query OKF bundles — find concepts by type, tags, search text, or links."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from okf.parse import Concept, list_concepts, read_bundle


def query_concepts(
    bundle_path: str | Path,
    type: str | None = None,
    tags: list[str] | None = None,
    search: str | None = None,
    has_resource: bool | None = None,
) -> list[dict[str, Any]]:
    """Query concepts in a bundle with optional filters.

    Args:
        bundle_path: Path to the OKF bundle directory.
        type: Filter by concept type (exact match, case-insensitive).
        tags: Filter by tags (all must match).
        search: Full-text search across title, description, and body.
        has_resource: If True, only concepts with a resource URI. If False, only without.

    Returns:
        List of matching concept dicts with id, type, title, description, tags, links.
    """
    _, concepts = read_bundle(bundle_path)
    results = []

    for concept in concepts:
        # Type filter
        if type and (concept.type or "").lower() != type.lower():
            continue

        # Tags filter (all must match)
        if tags:
            concept_tags = {t.lower() for t in concept.tags}
            if not all(t.lower() in concept_tags for t in tags):
                continue

        # Resource filter
        if has_resource is True and not concept.resource:
            continue
        if has_resource is False and concept.resource:
            continue

        # Full-text search
        if search:
            searchable = " ".join([
                concept.title or "",
                concept.description or "",
                concept.body,
                " ".join(concept.tags),
            ]).lower()
            if search.lower() not in searchable:
                continue

        results.append({
            "concept_id": concept.concept_id,
            "type": concept.type,
            "title": concept.title,
            "description": concept.description,
            "resource": concept.resource,
            "tags": concept.tags,
            "timestamp": concept.timestamp,
            "links": concept.links,
            "file": str(concept.path),
        })

    return results


def get_concept(bundle_path: str | Path, concept_id: str) -> dict[str, Any] | None:
    """Get a single concept by its ID (path without .md extension).

    Returns full concept details including body content, or None if not found.
    """
    _, concepts = read_bundle(bundle_path)
    for concept in concepts:
        if concept.concept_id == concept_id:
            return {
                "concept_id": concept.concept_id,
                "type": concept.type,
                "title": concept.title,
                "description": concept.description,
                "resource": concept.resource,
                "tags": concept.tags,
                "timestamp": concept.timestamp,
                "body": concept.body,
                "links": concept.links,
                "citations": concept.citations,
                "file": str(concept.path),
            }
    return None


def find_backlinks(bundle_path: str | Path, concept_id: str) -> list[dict[str, str]]:
    """Find all concepts that link to the given concept.

    Returns list of {concept_id, title, link_text} for inbound links.
    """
    _, concepts = read_bundle(bundle_path)
    backlinks = []

    # Normalize the target ID
    target_ids = {concept_id}
    if concept_id.endswith(".md"):
        target_ids.add(concept_id[:-3])

    for concept in concepts:
        for link in concept.links:
            # Normalize link target
            if link.startswith("/"):
                link_id = link.lstrip("/").replace(".md", "")
            else:
                link_id = link.replace(".md", "")

            if link_id in target_ids:
                backlinks.append({
                    "concept_id": concept.concept_id,
                    "title": concept.title or concept.concept_id,
                    "type": concept.type,
                })

    return backlinks


def get_graph(bundle_path: str | Path) -> dict[str, Any]:
    """Get the full concept graph — nodes and edges for visualization.

    Returns {"nodes": [...], "edges": [...]} suitable for graph rendering.
    """
    _, concepts = read_bundle(bundle_path)

    nodes = []
    for concept in concepts:
        nodes.append({
            "id": concept.concept_id,
            "type": concept.type,
            "title": concept.title or concept.concept_id,
            "description": concept.description,
            "tags": concept.tags,
        })

    edges = []
    for concept in concepts:
        for link in concept.links:
            if link.startswith("/"):
                target = link.lstrip("/").replace(".md", "")
            else:
                # Resolve relative
                concept_dir = concept.path.parent
                from okf.parse import read_bundle as _rb
                root, _ = _rb(bundle_path)
                target_path = (concept_dir / link).resolve()
                try:
                    target = str(target_path.relative_to(root)).replace(".md", "")
                except ValueError:
                    continue

            edges.append({
                "source": concept.concept_id,
                "target": target,
            })

    return {"nodes": nodes, "edges": edges}


def query(bundle_path: str | Path, **kwargs: Any) -> list[dict[str, Any]]:
    """Convenience wrapper for agents — query with keyword args."""
    return query_concepts(bundle_path, **kwargs)
