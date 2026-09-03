#!/usr/bin/env python3
"""Derive an external dispatch receipt from host hook events and a report."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: finalize_dispatch_receipt.py <package-dir> <review-report.json>", file=sys.stderr)
        return 2
    package = Path(sys.argv[1]).resolve()
    report_path = (package / sys.argv[2]).resolve()
    manifest_path = package / ".rearchitecture-package.json"
    if not manifest_path.is_file() or not report_path.is_file():
        print("FAIL: package manifest or report missing", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    request_id = report.get("review_run_id")
    reviewer_id = report.get("reviewer", {}).get("agent_id")
    host_log = Path(manifest.get("host_dispatch_log_ref", str(Path.home() / ".rearchitecture" / "dispatch-log" / "host-events.jsonl"))).expanduser()
    if not host_log.is_absolute():
        host_log = (package / host_log).resolve()
    if not host_log.is_file():
        print("FAIL: host dispatch log missing", file=sys.stderr)
        return 1
    events = [json.loads(line) for line in host_log.read_text(encoding="utf-8").splitlines() if line.strip()]
    matching = [event for event in events if event.get("request_id") == request_id and event.get("package_id") == manifest.get("package_id")]
    starts = [event for event in matching if event.get("event") in {"SubagentStart", "PreToolUse"}]
    stops = [event for event in matching if event.get("event") == "SubagentStop"]
    if not starts or not stops:
        print("FAIL: matching host start/stop pair missing", file=sys.stderr)
        return 1
    start, stop = starts[-1], stops[-1]
    if start.get("agent_id") != stop.get("agent_id"):
        print("FAIL: host start/stop agent mismatch", file=sys.stderr)
        return 1
    repo_root = next((parent for parent in (package, *package.parents) if (parent / ".git").exists()), package)
    receipt_dir = repo_root / ".rearchitecture" / "dispatch-log"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / f"{request_id}.json"
    receipt = {"request_id": request_id, "package_id": manifest.get("package_id"), "source_thread_id": start.get("session_id"), "reviewer_thread_id": stop.get("session_id"), "reviewer_id": reviewer_id, "runtime_agent_id": start.get("agent_id"), "input_revision": report.get("reviewer", {}).get("input_revision"), "report_ref": report_path.relative_to(package).as_posix(), "dispatch_status": "completed", "producer": "host-runtime", "derived_from_host_log": str(host_log), "started_at": start.get("timestamp"), "completed_at": stop.get("timestamp"), "finalized_at": datetime.now(timezone.utc).isoformat()}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    manifest["dispatch_receipt_ref"] = receipt_path.relative_to(repo_root).as_posix()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(receipt_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
