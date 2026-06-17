"""Create and scaffold OKF concepts and index files."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from okf.parse import list_concepts, read_bundle


def create_concept(
    bundle_path: str | Path,
    concept_path: str,
    type: str,
    title: str | None = None,
    description: str | None = None,
    resource: str | None = None,
    tags: list[str] | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    """Create a new OKF concept file.

    Args:
        bundle_path: Path to the bundle root.
        concept_path: Path relative to bundle root (without .md), e.g. "tables/orders".
        type: Concept type (required). E.g. "BigQuery Table", "Playbook", "Metric".
        title: Display name. Defaults to filename-based title.
        description: One-line summary.
        resource: Canonical URI for the underlying asset.
        tags: List of tags.
        body: Markdown body content. Defaults to a basic template.

    Returns:
        Dict with file path, frontmatter, and content.
    """
    root = Path(bundle_path).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Bundle directory not found: {root}")

    # Ensure .md extension
    if not concept_path.endswith(".md"):
        concept_path = concept_path + ".md"

    filepath = root / concept_path
    if filepath.exists():
        raise FileExistsError(f"Concept already exists: {concept_path}")

    # Build frontmatter
    fm: dict[str, Any] = {"type": type}
    if title:
        fm["title"] = title
    else:
        # Derive title from filename
        name = Path(concept_path).stem
        fm["title"] = name.replace("_", " ").replace("-", " ").title()

    if description:
        fm["description"] = description
    if resource:
        fm["resource"] = resource
    if tags:
        fm["tags"] = tags

    fm["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build file content
    lines = ["---"]
    for key, value in fm.items():
        if isinstance(value, list):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")

    if body:
        lines.append(body)
    else:
        # Basic template
        display_title = fm.get("title", Path(concept_path).stem)
        lines.append(f"# {display_title}")
        lines.append("")
        lines.append("TODO: Add content to this concept.")
        lines.append("")

    content = "\n".join(lines)

    # Create parent directories
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")

    return {
        "path": str(filepath),
        "concept_path": concept_path,
        "frontmatter": fm,
        "content": content,
    }


def scaffold_index(bundle_path: str | Path, directory: str = ".") -> dict[str, Any]:
    """Generate or update an index.md for a directory in the bundle.

    Scans the directory for concept files and generates an index.md
    with links and descriptions grouped by type.

    Args:
        bundle_path: Path to the bundle root.
        directory: Subdirectory to index (relative to bundle root). "." for root.

    Returns:
        Dict with the generated index content and file path.
    """
    root = Path(bundle_path).resolve()
    if directory == ".":
        target_dir = root
    else:
        target_dir = root / directory

    if not target_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {target_dir}")

    concepts = list_concepts(target_dir)

    # Group by type
    by_type: dict[str, list] = {}
    for concept in concepts:
        if concept.is_index or concept.is_log:
            continue
        t = concept.type or "Other"
        by_type.setdefault(t, []).append(concept)

    # Also list subdirectories
    subdirs = []
    for item in sorted(target_dir.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            subdir_index = item / "index.md"
            desc = ""
            if subdir_index.exists():
                raw = subdir_index.read_text(encoding="utf-8")
                # Extract first non-heading, non-empty line as description
                for line in raw.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("---"):
                        desc = line
                        break
            rel = item.relative_to(root)
            subdirs.append({"path": str(rel) + "/", "description": desc})

    # Build index content
    lines = []
    if directory == ".":
        lines.append("# Knowledge Bundle Index")
        lines.append("")

    for type_name, type_concepts in sorted(by_type.items()):
        lines.append(f"# {type_name}")
        lines.append("")
        for concept in sorted(type_concepts, key=lambda c: c.title or c.concept_id):
            rel_path = concept.path.relative_to(target_dir)
            display = concept.title or concept.concept_id.split("/")[-1]
            desc = f" — {concept.description}" if concept.description else ""
            lines.append(f"* [{display}]({rel_path}){desc}")
        lines.append("")

    if subdirs:
        lines.append("# Subdirectories")
        lines.append("")
        for subdir in subdirs:
            display = subdir["path"].rstrip("/").split("/")[-1].replace("_", " ").replace("-", " ").title()
            desc = f" — {subdir['description']}" if subdir["description"] else ""
            lines.append(f"* [{display}]({subdir['path']}){desc}")
        lines.append("")

    content = "\n".join(lines)

    # Write index.md
    index_path = target_dir / "index.md"
    index_path.write_text(content, encoding="utf-8")

    return {
        "path": str(index_path),
        "directory": directory,
        "concept_count": len(concepts),
        "content": content,
    }
