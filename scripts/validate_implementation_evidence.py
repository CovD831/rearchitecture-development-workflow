#!/usr/bin/env python3
"""Validate implementation-layer artifacts and evidence references."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_manifest_structure import validate as validate_manifest


def _paths(package: Path, value: object, key: str, errors: list[str]) -> list[Path]:
    values = value if isinstance(value, list) else [value]
    paths: list[Path] = []
    for item in values:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"missing document mapping: {key}")
            continue
        path = (package / item).resolve()
        if package.resolve() not in path.parents or not path.is_file():
            errors.append(f"missing document: {item}")
        else:
            paths.append(path)
    return paths


def validate(package: Path) -> list[str]:
    errors = validate_manifest(package)
    manifest = package / ".rearchitecture-package.json"
    if errors or not manifest.is_file():
        return errors
    data = json.loads(manifest.read_text(encoding="utf-8"))
    profile = data.get("profile")
    if profile not in {"implementation", "promotion"}:
        return ["implementation evidence is only active for implementation or promotion profiles"]
    documents = data.get("documents", {})
    for key in ("l3", "fixtures", "acceptance", "rollback"):
        _paths(package, documents.get(key), key, errors)
    registry_paths = _paths(package, documents.get("evidence_registry"), "evidence_registry", errors)
    entries: list[dict] = []
    for path in registry_paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid evidence registry {path.name}: {exc}")
            continue
        if not isinstance(payload, list):
            errors.append("evidence registry must be an array")
            continue
        entries.extend(item for item in payload if isinstance(item, dict))
    if not entries:
        errors.append("implementation layer requires at least one evidence entry")
    evidence_ids: set[str] = set()
    current_revision = str(data.get("current_revision", data.get("baseline_revision", "")))
    for entry in entries:
        evidence_id = entry.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id.strip() or evidence_id in evidence_ids:
            errors.append(f"evidence_id must be unique and non-empty: {evidence_id}")
        evidence_ids.add(str(evidence_id))
        for field in ("kind", "input_revision", "result_artifact", "scope"):
            if not entry.get(field):
                errors.append(f"evidence entry missing {field}: {evidence_id}")
        if entry.get("input_revision") not in {current_revision, data.get("baseline_revision")}:
            errors.append(f"evidence revision is not bound to the package revision: {evidence_id}")
        result = entry.get("result_artifact")
        if isinstance(result, str):
            result_path = (package / result).resolve()
            if package.resolve() not in result_path.parents or not result_path.is_file():
                errors.append(f"evidence result artifact does not exist: {result}")
    if profile == "promotion":
        _paths(package, documents.get("authority_merge"), "authority_merge", errors)
    return errors


def main() -> int:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate(package)
    if errors:
        print("Implementation evidence: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Implementation evidence: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
