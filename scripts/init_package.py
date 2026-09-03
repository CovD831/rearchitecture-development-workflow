#!/usr/bin/env python3
"""Initialize a minimal rearchitecture package manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DOCS = {
    "scope": "00-scope.md",
    "positioning": "01-positioning.md",
    "l1": "02-l1-target.md",
    "mapping": "03-current-to-target-map.md",
    "l2": ["04-l2-contracts.md"],
    "adr": ["05-adr.md"],
    "handoff": "06-handoff.md",
}
IMPLEMENTATION_DOCS = {
    "l3": "07-l3-task-contract.md",
    "fixtures": "fixtures/README.md",
    "acceptance": "acceptance.md",
    "rollback": "rollback.md",
}


def main() -> int:
    if len(sys.argv) not in {5, 6} or sys.argv[2] not in {"orientation", "design", "implementation"}:
        print("usage: init_package.py <package-dir> <size> <package-id> <baseline-revision> [current-revision]", file=sys.stderr)
        return 2
    package = Path(sys.argv[1])
    size, package_id, baseline = sys.argv[2], sys.argv[3], sys.argv[4]
    current = sys.argv[5] if len(sys.argv) == 6 else baseline
    documents = {"scope": BASE_DOCS["scope"]} if size == "orientation" else dict(BASE_DOCS)
    if size == "implementation":
        documents.update(IMPLEMENTATION_DOCS)
    manifest = {
        "package_id": package_id,
        "size": size,
        "baseline_revision": baseline,
        "current_revision": current,
        "documents": documents,
        "review": {"status": "pending", "reviewer": ""},
        "next_task": {"id": "TBD", "owner": "TBD"},
        "advancement_trigger": "TBD",
        "stop_rule": "TBD",
    }
    package.mkdir(parents=True, exist_ok=True)
    (package / ".rearchitecture-package.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"initialized {package / '.rearchitecture-package.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
