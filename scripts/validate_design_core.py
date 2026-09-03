#!/usr/bin/env python3
"""Validate the minimum Layer 1 design closed loop.

This intentionally does not require review reports, fixtures, L3 contracts,
promotion evidence or host provenance. Those belong to later validators.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_manifest_structure import validate as validate_manifest


def validate(package: Path) -> list[str]:
    errors = validate_manifest(package)
    manifest = package / ".rearchitecture-package.json"
    if errors or not manifest.is_file():
        return errors
    data = json.loads(manifest.read_text(encoding="utf-8"))
    documents = data.get("documents", {})
    for key in ("positioning", "l1", "mapping", "l2", "adr"):
        value = documents.get(key)
        values = value if isinstance(value, list) else [value]
        if not values or any(not isinstance(item, str) or not item.strip() for item in values):
            errors.append(f"missing document mapping: {key}")
            continue
        for item in values:
            if not (package / item).resolve().is_file():
                errors.append(f"missing document: {item}")
    if not isinstance(data.get("advancement_trigger"), str) or not data["advancement_trigger"].strip():
        errors.append("advancement_trigger is required")
    if not isinstance(data.get("stop_rule"), str) or not data["stop_rule"].strip():
        errors.append("stop_rule is required")
    return errors


def main() -> int:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate(package)
    if errors:
        print("Design core: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Design core: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
