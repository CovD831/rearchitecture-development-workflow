#!/usr/bin/env python3
"""Create a frozen, auditable review request for an architecture package."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: create_review_request.py <package-dir>", file=sys.stderr)
        return 2
    package = Path(sys.argv[1]).resolve()
    manifest_path = package / ".rearchitecture-package.json"
    if not manifest_path.is_file():
        print("FAIL: missing manifest", file=sys.stderr)
        return 1
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    state = data.get("review_state", "draft")
    if state not in {"draft", "blocked"}:
        print(f"FAIL: cannot request review from state {state}", file=sys.stderr)
        return 1
    now = datetime.now(timezone.utc).isoformat()
    history = data.setdefault("state_history", [])
    if not history:
        history.append({"state": "draft", "actor": "review-orchestrator", "timestamp": now, "input_revision": data.get("current_revision", data["baseline_revision"]), "evidence_ref": "manifest-created"})
    round_no = max([record.get("round", 0) for record in data.get("review_rounds", []) if isinstance(record, dict)] + [0]) + 1
    filename = "review-request.json" if round_no == 1 else f"review-request-round{round_no}.json"
    request = {"review_run_id": f"{data['package_id']}-review-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}", "package_id": data["package_id"], "input_revision": data.get("current_revision", data["baseline_revision"]), "round": round_no, "role": "adversarial-reviewer", "write_policy": "read-only", "must_not_edit": [".rearchitecture-package.json", "canonical architecture documents"], "required_output": "review-report.json", "dispatch_status": "pending", "requested_at": now}
    (package / filename).write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
    data["review_state"] = "review_requested"
    data["review_round"] = round_no
    data.setdefault("documents", {})["review_request"] = filename
    data.setdefault("review_rounds", []).append({"round": round_no, "review_run_id": request["review_run_id"], "input_revision": request["input_revision"], "trigger": "review request created"})
    data.setdefault("state_history", []).append({"state": "review_requested", "actor": "review-orchestrator", "timestamp": now, "input_revision": request["input_revision"], "evidence_ref": filename})
    manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(request, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
