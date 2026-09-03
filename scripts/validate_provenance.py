#!/usr/bin/env python3
"""Validate optional external reviewer-dispatch provenance."""

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
    if data.get("provenance_required") is not True:
        return []
    receipt_ref = data.get("dispatch_receipt_ref")
    if not isinstance(receipt_ref, str) or not receipt_ref.strip():
        return ["provenance_required needs dispatch_receipt_ref"]
    receipt_path = Path(receipt_ref).expanduser()
    if not receipt_path.is_absolute():
        receipt_path = (package / receipt_path).resolve()
    if package.resolve() in receipt_path.parents or not receipt_path.is_file():
        return ["provenance receipt must exist outside the package"]
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid provenance receipt: {exc}"]
    if not isinstance(receipt, dict):
        return ["provenance receipt must be an object"]
    required = ("request_id", "package_id", "reviewer_id", "runtime_agent_id", "input_revision", "report_ref", "dispatch_status", "producer")
    for field in required:
        if not receipt.get(field):
            errors.append(f"provenance receipt missing {field}")
    if receipt.get("package_id") != data.get("package_id"):
        errors.append("provenance receipt package_id mismatch")
    if receipt.get("dispatch_status") != "completed":
        errors.append("provenance receipt dispatch_status must be completed")
    if receipt.get("producer") not in {"codex-runtime", "host-runtime"}:
        errors.append("provenance receipt producer is not trusted")
    host_ref = data.get("host_dispatch_log_ref") or str(Path.home() / ".rearchitecture" / "dispatch-log" / "host-events.jsonl")
    host_path = Path(host_ref).expanduser()
    if not host_path.is_file():
        errors.append("host dispatch log does not exist")
        return errors
    try:
        events = [json.loads(line) for line in host_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"host dispatch log is not valid JSONL: {exc}")
        return errors
    matching = [event for event in events if isinstance(event, dict) and event.get("request_id") == receipt.get("request_id") and event.get("package_id") == receipt.get("package_id") and event.get("agent_id") == receipt.get("runtime_agent_id")]
    if not any(event.get("event") in {"SubagentStart", "PreToolUse"} for event in matching):
        errors.append("host dispatch log lacks matching reviewer start event")
    if not any(event.get("event") == "SubagentStop" for event in matching):
        errors.append("host dispatch log lacks matching reviewer stop event")
    return errors


def main() -> int:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate(package)
    if errors:
        print("Provenance: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Provenance: OK (proven or not required)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
