"""CLI interface for okf — allows agents to shell out for structured output."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="okf",
        description="Open Knowledge Format (OKF) toolkit",
    )
    sub = parser.add_subparsers(dest="command")

    # validate
    p_val = sub.add_parser("validate", help="Validate an OKF bundle")
    p_val.add_argument("bundle", help="Path to bundle directory")
    p_val.add_argument("--json", action="store_true", help="Output as JSON")

    # lint
    p_lint = sub.add_parser("lint", help="Lint an OKF bundle for health issues")
    p_lint.add_argument("bundle", help="Path to bundle directory")
    p_lint.add_argument("--json", action="store_true", help="Output as JSON")

    # query
    p_query = sub.add_parser("query", help="Query concepts in a bundle")
    p_query.add_argument("bundle", help="Path to bundle directory")
    p_query.add_argument("--type", help="Filter by concept type")
    p_query.add_argument("--tag", action="append", help="Filter by tag (repeatable)")
    p_query.add_argument("--search", help="Full-text search")
    p_query.add_argument("--json", action="store_true", help="Output as JSON")

    # show
    p_show = sub.add_parser("show", help="Show a concept's details")
    p_show.add_argument("bundle", help="Path to bundle directory")
    p_show.add_argument("concept_id", help="Concept ID (path without .md)")
    p_show.add_argument("--json", action="store_true", help="Output as JSON")

    # graph
    p_graph = sub.add_parser("graph", help="Get the concept graph")
    p_graph.add_argument("bundle", help="Path to bundle directory")
    p_graph.add_argument("--json", action="store_true", help="Output as JSON")

    # create
    p_create = sub.add_parser("create", help="Create a new concept")
    p_create.add_argument("bundle", help="Path to bundle directory")
    p_create.add_argument("path", help="Concept path (e.g. tables/orders)")
    p_create.add_argument("--type", required=True, help="Concept type")
    p_create.add_argument("--title", help="Display title")
    p_create.add_argument("--description", help="One-line description")
    p_create.add_argument("--resource", help="Canonical URI")
    p_create.add_argument("--tag", action="append", help="Tag (repeatable)")
    p_create.add_argument("--json", action="store_true", help="Output as JSON")

    # index
    p_index = sub.add_parser("index", help="Generate/update index.md")
    p_index.add_argument("bundle", help="Path to bundle directory")
    p_index.add_argument("--dir", default=".", help="Subdirectory to index")
    p_index.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Lazy imports for faster startup
    if args.command == "validate":
        from okf.validate import validate
        result = validate(args.bundle)
    elif args.command == "lint":
        from okf.lint import lint
        result = lint(args.bundle)
    elif args.command == "query":
        from okf.query import query_concepts
        result = query_concepts(args.bundle, type=args.type, tags=args.tag, search=args.search)
    elif args.command == "show":
        from okf.query import get_concept
        result = get_concept(args.bundle, args.concept_id)
        if result is None:
            print(f"Concept not found: {args.concept_id}", file=sys.stderr)
            return 1
    elif args.command == "graph":
        from okf.query import get_graph
        result = get_graph(args.bundle)
    elif args.command == "create":
        from okf.create import create_concept
        result = create_concept(
            args.bundle,
            args.path,
            type=args.type,
            title=args.title,
            description=args.description,
            resource=args.resource,
            tags=args.tag,
        )
    elif args.command == "index":
        from okf.create import scaffold_index
        result = scaffold_index(args.bundle, directory=args.dir)
    else:
        parser.print_help()
        return 1

    print(json.dumps(result, indent=2, cls=_JSONEncoder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
