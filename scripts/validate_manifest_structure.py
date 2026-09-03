#!/usr/bin/env python3
"""Validate only the package manifest and basic artifact structure."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROFILES = {"orientation", "design", "implementation", "promotion"}


def validate(package: Path) -> list[str]:
    errors: list[str] = []
    manifest = package / ".rearchitecture-package.json"
    if not manifest.is_file():
        return ["missing .rearchitecture-package.json"]
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid manifest: {exc}"]
    if not isinstance(data, dict):
        return ["manifest must be an object"]
    profile = data.get("profile")
    if profile not in PROFILES:
        errors.append("profile must be orientation, design, implementation or promotion")
    package_id = data.get("package_id")
    if not isinstance(package_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", package_id):
        errors.append("package_id is missing or invalid")
    for field in ("baseline_revision", "current_revision"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} is required")
    documents = data.get("documents")
    if not isinstance(documents, dict):
        errors.append("documents must be an object")
        documents = {}
    scope = documents.get("scope")
    if not isinstance(scope, str) or not scope.strip():
        errors.append("missing document mapping: scope")
    elif Path(scope).is_absolute() or package.resolve() not in (package / scope).resolve().parents:
        errors.append(f"document escapes package directory: {scope}")
    elif not (package / scope).resolve().is_file():
        errors.append(f"missing document: {scope}")
    gates = data.get("gates", {})
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
    next_task = data.get("next_task")
    if next_task is not None and (not isinstance(next_task, dict) or not next_task.get("id") or not next_task.get("owner")):
        errors.append("next_task must include id and owner")
    return errors


def main() -> int:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate(package)
    if errors:
        print("Manifest structure: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Manifest structure: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
