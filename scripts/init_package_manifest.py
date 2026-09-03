#!/usr/bin/env python3
"""Initialize a canonical rearchitecture package manifest."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    if len(sys.argv) not in {5, 6} or sys.argv[2] not in {"orientation", "design", "implementation", "promotion"}:
        print("usage: init_package_manifest.py <package-dir> <profile> <package-id> <baseline-revision> [current-revision]", file=sys.stderr)
        return 2
    package = Path(sys.argv[1]).resolve()
    profile, package_id, baseline = sys.argv[2:5]
    current = sys.argv[5] if len(sys.argv) == 6 else baseline
    package.mkdir(parents=True, exist_ok=True)
    manifest = {"package_id": package_id, "profile": profile, "validation_mode": "layered", "status": "draft", "baseline_revision": baseline, "current_revision": current, "documents": {"scope": "00-scope-and-authority.md"}, "gates": {}, "reviewer": {"id": None, "independent": False, "report_status": "pending"}, "review_state": "draft", "review_round": 0, "max_review_rounds": 2, "review_rounds": [], "state_history": [{"state": "draft", "actor": "package-initializer", "timestamp": datetime.now(timezone.utc).isoformat(), "input_revision": baseline, "evidence_ref": "manifest-created"}], "advancement_trigger": "complete the minimum design closed loop", "stop_rule": "stop and preserve the current path if scope or ownership cannot be established", "next_task": {"id": "TBD", "owner": "TBD"}}
    if profile != "orientation":
        manifest["documents"].update({"positioning": "01-positioning-and-complexity.md", "l1": "02-l1-target-architecture.md", "mapping": "03-current-to-target-map.md", "l2": ["04-l2-contracts.md"], "migration": "05-migration-and-evidence.md", "adr": ["06-adr.md"], "review": "07-review-consumption.md", "review_reports": ["review-report.json"], "review_request": "review-request.json", "review_ledger": "review-ledger.json", "evidence_registry": "evidence-registry.json", "maintenance": "08-maintenance-and-catalog.md", "handoff": "handoff.md"})
        if profile in {"implementation", "promotion"}:
            manifest["documents"].update({"l3": "04b-task-l3-contract.md", "fixtures": "fixtures/README.md", "acceptance": "acceptance.md", "rollback": "rollback.md"})
        if profile == "promotion":
            manifest["documents"]["authority_merge"] = "authority-merge.md"
    (package / ".rearchitecture-package.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"initialized {package / '.rearchitecture-package.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
