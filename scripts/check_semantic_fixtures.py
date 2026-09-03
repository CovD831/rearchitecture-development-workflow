#!/usr/bin/env python3
"""Regression checks for semantic review/evidence validation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def build_package(root: Path, broken: str = "") -> None:
    names = {"scope": "scope.md", "positioning": "positioning.md", "l1": "l1.md", "mapping": "mapping.md", "l2": ["l2.md"], "migration": "migration.md", "adr": ["adr.md"], "review": "review.md", "review_reports": ["report.json"], "review_request": "request.json", "review_ledger": "ledger.json", "evidence_registry": "evidence.json", "maintenance": "maintenance.md", "handoff": "handoff.md"}
    for value in names.values():
        for item in value if isinstance(value, list) else [value]:
            path = root / item
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# artifact\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_x.py").write_text("def test_x(): pass\n", encoding="utf-8")
    (root / "evidence").mkdir()
    (root / "evidence" / "ev.json").write_text("{}\n", encoding="utf-8")
    report = {"package_id": "FIXTURE", "round": 1, "review_run_id": "R1", "reviewer": {"agent_id": "reviewer", "independent": True, "input_revision": "r1"}, "findings": [{"id": "AR-001", "statement": "fixture finding", "severity": "non-blocking", "recommendation": "record", "evidence_refs": [{"kind": "path", "ref": "l2.md"}]}], "steelman": {"decision_refs": ["adr.md"]}, "overall": "pass", "closure_confirmation": True}
    ledger = [{"finding_id": "AR-001", "severity": "non-blocking", "consumer_refs": [{"kind": "path", "ref": "l2.md", "anchor": "artifact", "decision_ref": "adr.md"}], "task_ref": "T1", "test_or_evidence_refs": [{"kind": "path", "ref": "tests/test_x.py::test_x"}], "owner": "owner", "gate": "G1", "status": "pending"}]
    evidence = [{"evidence_id": "EV-1", "kind": "test_result", "input_revision": "r1", "result_artifact": "evidence/ev.json", "scope": "AR-001"}]
    if broken == "missing":
        ledger[0]["test_or_evidence_refs"] = [{"kind": "path", "ref": "missing.py"}]
    elif broken == "duplicate":
        report["findings"].append(dict(report["findings"][0]))
    elif broken == "blocked":
        report["overall"] = "blocked"
        report["closure_confirmation"] = False
    (root / "report.json").write_text(json.dumps(report), encoding="utf-8")
    (root / "request.json").write_text(json.dumps({"review_run_id": "R1", "package_id": "FIXTURE", "input_revision": "r1", "role": "adversarial-reviewer", "write_policy": "read-only", "required_output": "report.json"}), encoding="utf-8")
    dispatch = root.parent / ".rearchitecture" / "dispatch-log"
    dispatch.mkdir(parents=True, exist_ok=True)
    (dispatch / "R1.json").write_text(json.dumps({"request_id": "R1", "package_id": "FIXTURE", "source_thread_id": "main", "reviewer_thread_id": "reviewer-thread", "reviewer_id": "reviewer", "runtime_agent_id": "runtime-1", "input_revision": "r1", "report_ref": "report.json", "dispatch_status": "completed", "producer": "codex-runtime"}), encoding="utf-8")
    (root.parent / "host-events.jsonl").write_text("\n".join(json.dumps({"event": event, "request_id": "R1", "agent_id": "runtime-1", "package_id": "FIXTURE"}) for event in ("SubagentStart", "SubagentStop")) + "\n", encoding="utf-8")
    (root / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
    (root / "evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
    history = [{"state": state, "actor": "test", "timestamp": "now", "input_revision": "r1", "evidence_ref": "report.json"} for state in ("draft", "review_requested", "review_received", "consumption_pending", "review_resolved")]
    manifest = {"package_id": "FIXTURE", "profile": "design", "status": "ready", "baseline_revision": "r1", "documents": names, "gates": {"authority": "pass", "user_decisions": "pass", "l1": "pass", "mapping": "pass", "l2": "pass", "review": "pass"}, "user_decisions": [{"id": "UD-1", "decision": "fixture", "decided_by": "user", "timestamp": "now", "scope": "fixture", "record_ref": "scope.md"}], "reviewer": {"id": "reviewer", "independent": True}, "dispatch_receipt": {"request_id": "R1", "source_thread": "main", "reviewer_thread": "reviewer", "started_at": "now", "completed_at": "now", "report_ref": "report.json"}, "dispatch_receipt_ref": ".rearchitecture/dispatch-log/R1.json", "host_dispatch_log_ref": "host-events.jsonl", "review_state": "review_resolved", "review_round": 1, "max_review_rounds": 3, "review_rounds": [{"round": 1, "review_run_id": "R1", "input_revision": "r1", "trigger": "fixture"}], "state_history": history, "advancement_trigger": "trigger", "promotion_evidence": ["evidence.json"], "stop_rule": "stop", "next_task": {"id": "T1", "owner": "owner"}}
    (root / ".rearchitecture-package.json").write_text(json.dumps(manifest), encoding="utf-8")


def main() -> int:
    checker = Path(__file__).with_name("check_package_completeness.py")
    with tempfile.TemporaryDirectory() as temp:
        repo = Path(temp) / "repo"
        (repo / ".git").mkdir(parents=True)
        good = repo / "good"
        good.mkdir()
        build_package(good)
        if subprocess.run([sys.executable, str(checker), str(good)]).returncode != 0:
            raise RuntimeError("healthy semantic fixture unexpectedly failed")
        bad = repo / "bad"
        bad.mkdir()
        build_package(bad, broken="missing")
        if subprocess.run([sys.executable, str(checker), str(bad)]).returncode == 0:
            raise RuntimeError("missing evidence fixture unexpectedly passed")
        for mode in ("duplicate", "blocked"):
            case = repo / mode
            case.mkdir()
            build_package(case, broken=mode)
            if subprocess.run([sys.executable, str(checker), str(case)]).returncode == 0:
                raise RuntimeError(f"{mode} fixture unexpectedly passed")
    print("semantic fixture checks: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
