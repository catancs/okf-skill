"""Validate OKF bundles against the v0.1 specification."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from okf.parse import RESERVED_FILENAMES, Concept, list_concepts, parse_frontmatter


@dataclass
class Issue:
    """A validation issue."""

    level: str  # "error" | "warning" | "info"
    message: str
    file: str | None = None
    concept_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"level": self.level, "message": self.message}
        if self.file:
            d["file"] = self.file
        if self.concept_id:
            d["concept_id"] = self.concept_id
        return d


@dataclass
class ValidationResult:
    """Result of validating an OKF bundle."""

    valid: bool
    concept_count: int
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    infos: list[Issue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "concept_count": self.concept_count,
            "errors": [i.to_dict() for i in self.errors],
            "warnings": [i.to_dict() for i in self.warnings],
            "infos": [i.to_dict() for i in self.infos],
        }


def validate_concept(concept: Concept) -> list[Issue]:
    """Validate a single concept against OKF v0.1 rules."""
    issues: list[Issue] = []
    loc = concept.concept_id

    # Reserved filenames should not be concept documents
    if concept.path.name in RESERVED_FILENAMES:
        issues.append(Issue("error", f"Reserved filename '{concept.path.name}' used as concept", file=str(concept.path), concept_id=loc))
        return issues

    # Must have parseable frontmatter (if file starts with ---)
    raw = concept.raw
    if raw.startswith("---"):
        fm, _ = parse_frontmatter(raw)
        if not fm:
            issues.append(Issue("error", "Frontmatter block is empty or unparseable", file=str(concept.path), concept_id=loc))
    else:
        issues.append(Issue("warning", "No YAML frontmatter block found", file=str(concept.path), concept_id=loc))
        fm = {}

    # Required: type field
    concept_type = fm.get("type")
    if not concept_type:
        issues.append(Issue("error", "Missing required 'type' field in frontmatter", file=str(concept.path), concept_id=loc))
    elif not isinstance(concept_type, str):
        issues.append(Issue("error", f"'type' must be a string, got {type(concept_type).__name__}", file=str(concept.path), concept_id=loc))

    # Recommended fields
    if not fm.get("title"):
        issues.append(Issue("warning", "Missing recommended 'title' field", file=str(concept.path), concept_id=loc))

    if not fm.get("description"):
        issues.append(Issue("warning", "Missing recommended 'description' field", file=str(concept.path), concept_id=loc))

    if not fm.get("timestamp"):
        issues.append(Issue("info", "Missing optional 'timestamp' field", file=str(concept.path), concept_id=loc))

    return issues


def validate_bundle(bundle_path: str | Path) -> ValidationResult:
    """Validate an entire OKF bundle.

    Checks:
    - All .md files have parseable frontmatter (except reserved)
    - All concepts have required 'type' field
    - Reserved filenames follow correct structure
    - Cross-links resolve to existing concepts
    """
    root = Path(bundle_path).resolve()
    if not root.is_dir():
        return ValidationResult(
            valid=False,
            concept_count=0,
            errors=[Issue("error", f"Not a directory: {root}")],
        )

    concepts = list_concepts(root)
    all_concept_ids = {c.concept_id for c in concepts}
    all_errors: list[Issue] = []
    all_warnings: list[Issue] = []
    all_infos: list[Issue] = []

    # Validate each concept
    for concept in concepts:
        for issue in validate_concept(concept):
            if issue.level == "error":
                all_errors.append(issue)
            elif issue.level == "warning":
                all_warnings.append(issue)
            else:
                all_infos.append(issue)

    # Check reserved files at root level
    for reserved in RESERVED_FILENAMES:
        reserved_path = root / reserved
        if reserved_path.exists():
            raw = reserved_path.read_text(encoding="utf-8")
            if reserved == "index.md" and raw.startswith("---"):
                # index.md MAY have frontmatter (for okf_version)
                fm, _ = parse_frontmatter(raw)
                if "type" in fm:
                    all_warnings.append(Issue("warning", f"{reserved} has 'type' field — reserved for concept documents only", file=str(reserved_path)))

    # Validate cross-links
    for concept in concepts:
        for link in concept.links:
            # Resolve link relative to concept's directory
            if link.startswith("/"):
                # Bundle-relative
                target_id = link.lstrip("/").replace(".md", "")
            else:
                # Relative
                concept_dir = concept.path.parent
                target_path = (concept_dir / link).resolve()
                try:
                    target_id = str(target_path.relative_to(root)).replace(".md", "")
                except ValueError:
                    all_warnings.append(Issue("warning", f"Cross-link escapes bundle: {link}", file=str(concept.path), concept_id=concept.concept_id))
                    continue

            if target_id not in all_concept_ids:
                all_warnings.append(Issue("warning", f"Broken cross-link: {link} (target not found)", file=str(concept.path), concept_id=concept.concept_id))

    return ValidationResult(
        valid=len(all_errors) == 0,
        concept_count=len(concepts),
        errors=all_errors,
        warnings=all_warnings,
        infos=all_infos,
    )


def validate(bundle_path: str | Path) -> dict[str, Any]:
    """Validate a bundle and return a dict result.

    Convenience wrapper for agents that want dict output.
    """
    return validate_bundle(bundle_path).to_dict()
