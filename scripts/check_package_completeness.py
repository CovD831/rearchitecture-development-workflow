#!/usr/bin/env python3
"""Check a rearchitecture package manifest and its hard gates."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from validate_design_core import validate as validate_design_core
from validate_manifest_structure import validate as validate_manifest_structure
from validate_review_loop import validate as validate_review_loop
from validate_implementation_evidence import validate as validate_implementation_evidence
from validate_provenance import validate as validate_provenance


REQUIRED = {
    "orientation": ("scope",),
    "design": ("scope", "positioning", "l1", "mapping", "l2", "migration", "adr", "review", "review_reports", "review_request", "review_ledger", "evidence_registry", "maintenance", "handoff"),
    "implementation": ("scope", "positioning", "l1", "mapping", "l2", "migration", "adr", "review", "review_reports", "review_request", "review_ledger", "evidence_registry", "l3", "fixtures", "acceptance", "rollback", "maintenance", "handoff"),
    "promotion": ("scope", "positioning", "l1", "mapping", "l2", "migration", "adr", "review", "review_reports", "review_request", "review_ledger", "evidence_registry", "l3", "fixtures", "acceptance", "rollback", "authority_merge", "maintenance", "handoff"),
}
PASS = {"pass", "accepted", "complete"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def safe_path(root: Path, raw: str) -> Path | None:
    root = root.resolve()
    candidate = Path(raw)
    if candidate.is_absolute():
        return None
    resolved = (root / candidate).resolve()
    if root not in resolved.parents and resolved != root:
        return None
    return resolved


def package_or_repo_path(package: Path, repo_root: Path, raw: str) -> Path | None:
    direct = (repo_root.resolve() / raw).resolve()
    if not raw.startswith("/") and direct.is_file() and (repo_root.resolve() in direct.parents or direct == repo_root.resolve()):
        return direct
    for root in (package, repo_root):
        candidate = (root / raw).resolve()
        boundary = repo_root.resolve()
        if boundary in candidate.parents or candidate == boundary:
            return candidate
    return None


def main() -> int:
    args = sys.argv[1:]
    phase = None
    if "--phase" in args:
        index = args.index("--phase")
        if index + 1 >= len(args):
            print("FAIL: --phase requires a value", file=sys.stderr)
            return 1
        phase = args[index + 1]
        del args[index:index + 2]
    if len(args) > 1:
        print("FAIL: expected at most one package directory", file=sys.stderr)
        return 1
    package = Path(args[0]) if args else Path.cwd()
    if phase == "manifest":
        errors = validate_manifest_structure(package)
        if errors:
            print("Manifest structure: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Manifest structure: OK")
        return 0
    if phase == "design-core":
        errors = validate_design_core(package)
        if errors:
            print("Design core: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Design core: OK")
        return 0
    if phase == "review-loop":
        errors = validate_review_loop(package)
        if errors:
            print("Review loop: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Review loop: OK")
        return 0
    if phase == "implementation-evidence":
        errors = validate_implementation_evidence(package)
        if errors:
            print("Implementation evidence: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Implementation evidence: OK")
        return 0
    if phase == "provenance":
        errors = validate_provenance(package)
        if errors:
            print("Provenance: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Provenance: OK (proven or not required)")
        return 0
    manifest_path = package / ".rearchitecture-package.json"
    errors: list[str] = []
    if not manifest_path.is_file():
        print("FAIL: missing .rearchitecture-package.json", file=sys.stderr)
        return 1
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: invalid manifest: {exc}", file=sys.stderr)
        return 1
    if data.get("validation_mode") == "layered" and phase is None:
        errors: list[str] = []
        errors.extend(validate_manifest_structure(package))
        errors.extend(validate_design_core(package))
        review_state = data.get("review_state", "draft")
        if review_state not in {"draft", "not_started", "decision_pending"}:
            errors.extend(validate_review_loop(package))
        if data.get("profile") in {"implementation", "promotion"}:
            errors.extend(validate_implementation_evidence(package))
        if data.get("provenance_required") is True:
            errors.extend(validate_provenance(package))
        if errors:
            print("Package completeness: FAIL", file=sys.stderr)
            for error in dict.fromkeys(errors):
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Package completeness: OK (layered)")
        return 0
    profile = data.get("profile")
    if profile not in REQUIRED:
        fail(errors, "profile must be orientation, design, implementation or promotion")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", str(data.get("package_id", ""))):
        fail(errors, "package_id is missing or invalid")
    if profile == "design" and data.get("review_state", "draft") in {"draft", "not_started", "decision_pending"}:
        core_errors = validate_design_core(package)
        if core_errors:
            print("Package completeness: FAIL", file=sys.stderr)
            for error in core_errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Package completeness: OK (design core)")
        return 0
    documents = data.get("documents")
    if not isinstance(documents, dict):
        fail(errors, "documents must be an object")
        documents = {}
    report_payloads: list[dict] = []
    ledger_payload: list[dict] | None = None
    evidence_payload: list[dict] | None = None
    request_payload: dict | None = None
    special_json_keys = {"review_reports", "review_ledger", "evidence_registry", "review_request"}
    repo_root = package.resolve()
    try:
        discovered = subprocess.run(["git", "-C", str(package), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
        if discovered:
            repo_root = Path(discovered).resolve()
    except (OSError, subprocess.CalledProcessError):
        for parent in (package.resolve(), *package.resolve().parents):
            if (parent / ".git").exists():
                repo_root = parent
                break
    for key in REQUIRED.get(profile, ()):
        value = documents.get(key)
        values = value if isinstance(value, list) else [value]
        if key in {"review_ledger", "evidence_registry", "review_request"} and isinstance(value, list) and len(value) != 1:
            fail(errors, f"{key} must map to exactly one artifact")
        if not values or any(not isinstance(item, str) or not item.strip() for item in values):
            fail(errors, f"missing document mapping: {key}")
            continue
        for item in values:
            target = (package / item).resolve()
            if package.resolve() not in target.parents and target != package.resolve():
                fail(errors, f"document escapes package directory: {item}")
            elif not target.is_file():
                fail(errors, f"missing document: {item}")
            elif key in special_json_keys and target.suffix.lower() != ".json":
                fail(errors, f"{key} must use a .json artifact: {item}")
            elif target.suffix.lower() == ".md":
                text = target.read_text(encoding="utf-8")
                for link in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
                    link = link.split("#", 1)[0].strip()
                    if link and "://" not in link and not link.startswith("mailto:") and not (target.parent / link).resolve().exists():
                        fail(errors, f"broken link: {item} -> {link}")
            elif key == "review_reports":
                try:
                    parsed = json.loads(target.read_text(encoding="utf-8"))
                    if not isinstance(parsed, dict):
                        raise ValueError("report must be an object")
                    report_payloads.append(parsed)
                except (json.JSONDecodeError, ValueError) as exc:
                    fail(errors, f"invalid review report {item}: {exc}")
            elif key == "review_ledger":
                try:
                    parsed = json.loads(target.read_text(encoding="utf-8"))
                    if not isinstance(parsed, list):
                        raise ValueError("ledger must be an array")
                    ledger_payload = parsed
                except (json.JSONDecodeError, ValueError) as exc:
                    fail(errors, f"invalid review ledger {item}: {exc}")
            elif key == "evidence_registry":
                try:
                    parsed = json.loads(target.read_text(encoding="utf-8"))
                    if not isinstance(parsed, list):
                        raise ValueError("evidence registry must be an array")
                    evidence_payload = parsed
                except (json.JSONDecodeError, ValueError) as exc:
                    fail(errors, f"invalid evidence registry {item}: {exc}")
            elif key == "review_request":
                try:
                    request = json.loads(target.read_text(encoding="utf-8"))
                    request_payload = request
                    for field in ("review_run_id", "package_id", "input_revision", "role", "write_policy", "required_output"):
                        if not request.get(field):
                            fail(errors, f"review request missing {field}")
                    if request.get("package_id") != data.get("package_id"):
                        fail(errors, "review request package_id mismatch")
                    if request.get("input_revision") not in {data.get("baseline_revision"), data.get("current_revision")}:
                        fail(errors, "review request input_revision is not baseline/current revision")
                except (json.JSONDecodeError, AttributeError) as exc:
                    fail(errors, f"invalid review request {item}: {exc}")
    gates = data.get("gates", {})
    if not isinstance(gates, dict):
        fail(errors, "gates must be an object")
        gates = {}
    if not isinstance(gates.get("review", "pending"), str):
        fail(errors, "gates.review must be a string")
    if gates.get("user_decisions") in PASS:
        decisions = data.get("user_decisions")
        if not isinstance(decisions, list) or not decisions:
            fail(errors, "user_decisions=pass requires durable decision records")
        else:
            for decision in decisions:
                if not isinstance(decision, dict) or any(not decision.get(field) for field in ("id", "decision", "decided_by", "timestamp", "scope", "record_ref")):
                    fail(errors, "each user decision needs id, decision, decided_by, timestamp, scope and record_ref")
                elif safe_path(package, str(decision["record_ref"])) is None or not safe_path(package, str(decision["record_ref"])).is_file():
                    fail(errors, f"user decision record_ref does not exist: {decision['record_ref']}")
    if profile in {"design", "implementation", "promotion"} and gates.get("review") not in PASS:
        fail(errors, "review gate is not passed")
    reviewer = data.get("reviewer")
    if not isinstance(reviewer, dict):
        reviewer = {}
    if profile == "orientation" and gates.get("review") in PASS:
        fail(errors, "orientation packages cannot claim review=pass")
    if profile in {"design", "implementation", "promotion"}:
        if not isinstance(reviewer, dict) or not reviewer.get("id"):
            fail(errors, "reviewer.id is required")
        elif reviewer.get("independent") is not True:
            fail(errors, "reviewer must be an independent sub-agent; exceptions cannot auto-pass review")
        review_state = data.get("review_state")
        if review_state not in {"review_resolved", "blocked", "consumption_pending", "review_received", "review_requested"}:
            fail(errors, "invalid review_state")
        report_ids: set[str] = set()
        seen_report_ids: set[str] = set()
        blocking_report_ids: set[str] = set()
        report_rounds: dict[int, dict] = {}
        report_finding_ids: dict[int, set[str]] = {}
        report_revisions: set[str] = set()
        for report in report_payloads:
            reviewer_data = report.get("reviewer", {})
            if not isinstance(reviewer_data, dict):
                fail(errors, f"review report reviewer must be an object: {report.get('review_run_id')}")
                reviewer_data = {}
            if reviewer_data.get("independent") is not True:
                fail(errors, "review report is not from an independent reviewer")
            if report.get("package_id") != data.get("package_id"):
                fail(errors, f"review report package_id mismatch: {report.get('review_run_id')}")
            if reviewer_data.get("agent_id") != reviewer.get("id"):
                fail(errors, f"review report reviewer mismatch: {report.get('review_run_id')}")
            input_revision = str(reviewer_data.get("input_revision", ""))
            if report.get("package_id") and report.get("package_id") != data.get("package_id"):
                fail(errors, f"review report package_id mismatch: {report.get('review_run_id')}")
            if reviewer_data.get("agent_id") and reviewer_data.get("agent_id") != reviewer.get("id"):
                fail(errors, f"review report reviewer mismatch: {report.get('review_run_id')}")
            if request_payload is not None and report.get("review_run_id") == request_payload.get("review_run_id"):
                if reviewer_data.get("input_revision") != request_payload.get("input_revision"):
                    fail(errors, "review report input_revision differs from review request")
            report_revisions.add(input_revision)
            round_no = report.get("round")
            if not isinstance(round_no, int) or round_no < 1 or round_no in report_rounds:
                fail(errors, "each review report needs a unique positive round")
            else:
                report_rounds[round_no] = report
            findings = report.get("findings")
            if not isinstance(findings, list):
                fail(errors, "review report findings must be an array")
                continue
            for finding in findings:
                if not isinstance(finding, dict) or not finding.get("id"):
                    fail(errors, "review finding must have a stable id")
                else:
                    finding_id = str(finding["id"])
                    if finding_id in seen_report_ids and not (finding.get("continues_id") == finding_id):
                        fail(errors, f"duplicate finding id requires continues_id: {finding_id}")
                    if finding_id in seen_report_ids and finding.get("continues_id") == finding_id:
                        prior_rounds = [number for number, ids in report_finding_ids.items() if isinstance(number, int) and number < (round_no or 0) and finding_id in ids]
                        if not prior_rounds or not finding.get("parent_review_run_id"):
                            fail(errors, f"continued finding lacks prior lineage: {finding_id}")
                    seen_report_ids.add(finding_id)
                    report_ids.add(finding_id)
                    report_finding_ids.setdefault(round_no, set()).add(finding_id)
                    if finding.get("severity") == "blocking":
                        blocking_report_ids.add(finding_id)
                    if finding.get("severity") not in {"blocking", "non-blocking"}:
                        fail(errors, f"invalid finding severity: {finding_id}")
                    if not isinstance(finding.get("statement"), str) or not finding.get("statement"):
                        fail(errors, f"finding statement missing: {finding_id}")
                    if not isinstance(finding.get("recommendation"), str) or not finding.get("recommendation"):
                        fail(errors, f"finding recommendation missing: {finding_id}")
                    refs = finding.get("evidence_refs", [])
                    if not isinstance(refs, list):
                        fail(errors, f"finding evidence_refs must be a list: {finding_id}")
                    for ref in refs if isinstance(refs, list) else []:
                        if not isinstance(ref, dict) or ref.get("kind") not in {"path", "command", "record", "evidence"} or not ref.get("ref", ref.get("evidence_id")):
                            fail(errors, f"untyped finding evidence reference: {finding_id}")
                        elif ref.get("kind") == "path":
                            raw_path = str(ref["ref"]).split("::", 1)[0].split("#", 1)[0]
                            candidate = package_or_repo_path(package, repo_root, raw_path)
                            if candidate is None:
                                fail(errors, f"finding evidence path escapes repository: {ref['ref']}")
                            elif not candidate.is_file():
                                fail(errors, f"finding evidence path does not exist: {ref['ref']}")
                        elif ref.get("kind") == "evidence":
                            if evidence_payload is None or not any(entry.get("evidence_id") == ref.get("evidence_id") for entry in evidence_payload if isinstance(entry, dict)):
                                fail(errors, f"unknown finding evidence_id: {ref.get('evidence_id')}")
                        elif not ref.get("result_ref") or safe_path(repo_root, str(ref["result_ref"])) is None or not safe_path(repo_root, str(ref["result_ref"])).is_file():
                            fail(errors, f"finding evidence lacks existing result_ref: {finding_id}")
            steelman = report.get("steelman", {})
            if not isinstance(steelman, dict) or not steelman.get("decision_refs"):
                fail(errors, "steelman must include decision_refs")
        if report_revisions and str(data.get("baseline_revision")) not in report_revisions:
            fail(errors, "round 1 review report must match baseline_revision")
        raw_manifest_rounds = data.get("review_rounds")
        if not isinstance(raw_manifest_rounds, list) or any(not isinstance(record, dict) for record in raw_manifest_rounds):
            fail(errors, "review_rounds must contain only objects")
            raw_manifest_rounds = []
        manifest_rounds: dict[int, dict] = {}
        for record in raw_manifest_rounds:
            round_key = record.get("round")
            if round_key in manifest_rounds:
                fail(errors, f"duplicate manifest review round: {round_key}")
            manifest_rounds[round_key] = record
        if set(report_rounds) != set(manifest_rounds):
            fail(errors, "manifest review_rounds and report rounds differ")
        for round_no, report in report_rounds.items():
            record = manifest_rounds.get(round_no, {})
            if record.get("review_run_id") != report.get("review_run_id"):
                fail(errors, f"review run id mismatch for round {round_no}")
            if record.get("input_revision") != report.get("reviewer", {}).get("input_revision"):
                fail(errors, f"review input revision mismatch for round {round_no}")
        current_revision = str(data.get("current_revision", data.get("baseline_revision", "")))
        if current_revision not in report_revisions and data.get("review_state") != "blocked":
            fail(errors, "current_revision must match a review report input_revision unless blocked")
        if ledger_payload is not None:
            ledger_ids = {str(item.get("finding_id")) for item in ledger_payload if isinstance(item, dict) and item.get("finding_id")}
            if report_ids != ledger_ids:
                fail(errors, f"review findings and ledger IDs differ: reports={sorted(report_ids)} ledger={sorted(ledger_ids)}")
            for item in ledger_payload:
                if not isinstance(item, dict):
                    continue
                for field in ("consumer_refs", "owner", "gate", "test_or_evidence_refs"):
                    if not item.get(field):
                        fail(errors, f"review ledger entry missing {field}: {item.get('finding_id')}")
                for field in ("consumer_refs", "test_or_evidence_refs"):
                    refs = item.get(field, [])
                    if not isinstance(refs, list):
                        fail(errors, f"{field} must be a list: {item.get('finding_id')}")
                        continue
                    for ref in refs:
                        if not isinstance(ref, dict) or ref.get("kind") not in {"path", "command", "record", "evidence"} or not ref.get("ref", ref.get("evidence_id")):
                            fail(errors, f"untyped evidence/consumer reference: {item.get('finding_id')}")
                            continue
                        if ref["kind"] == "path":
                            raw_path = str(ref["ref"]).split("::", 1)[0].split("#", 1)[0]
                            candidate = package_or_repo_path(package, repo_root, raw_path)
                            if candidate is None:
                                fail(errors, f"referenced path escapes repository: {ref['ref']}")
                            elif not candidate.is_file():
                                fail(errors, f"referenced path does not exist: {ref['ref']}")
                        elif ref["kind"] == "evidence":
                            if evidence_payload is None or not any(entry.get("evidence_id") == ref.get("evidence_id") for entry in evidence_payload if isinstance(entry, dict)):
                                fail(errors, f"unknown evidence_id: {ref.get('evidence_id')}")
                        elif not ref.get("result_ref") or safe_path(repo_root, str(ref["result_ref"])) is None or not safe_path(repo_root, str(ref["result_ref"])).is_file():
                            fail(errors, f"command/record reference lacks an existing result_ref: {ref.get('ref')}")
                        if field == "consumer_refs" and ref.get("kind") == "path":
                            if not ref.get("anchor") or not ref.get("decision_ref"):
                                fail(errors, f"consumer reference needs anchor and decision_ref: {item.get('finding_id')}")
                            else:
                                raw_path = str(ref["ref"]).split("::", 1)[0].split("#", 1)[0]
                                artifact = (repo_root / raw_path) if (repo_root / raw_path).is_file() else (package / raw_path)
                                if artifact.is_file() and str(ref["anchor"]).lower() not in artifact.read_text(encoding="utf-8").lower():
                                    fail(errors, f"consumer anchor not found: {ref['ref']}#{ref['anchor']}")
                if item.get("status") == "resolved" and not isinstance(item.get("resolution_ref"), dict):
                    fail(errors, f"resolved finding lacks resolution_ref: {item.get('finding_id')}")
                if item.get("status") == "resolved" and isinstance(item.get("resolution_ref"), dict):
                    resolution = item["resolution_ref"]
                    if resolution.get("kind") != "evidence":
                        fail(errors, f"resolved finding must reference evidence_id: {item.get('finding_id')}")
                    elif evidence_payload is None or not any(entry.get("evidence_id") == resolution.get("evidence_id") and entry.get("scope") == item.get("finding_id") for entry in evidence_payload if isinstance(entry, dict)):
                        fail(errors, f"resolution evidence_id not found: {item.get('finding_id')}")
            ledger_by_id = {str(item.get("finding_id")): item for item in ledger_payload if isinstance(item, dict)}
            if len(ledger_by_id) != len(ledger_payload):
                fail(errors, "duplicate or invalid finding_id in review ledger")
            if gates.get("review") in PASS or data.get("review_state") == "review_resolved":
                for finding_id in blocking_report_ids:
                    item = ledger_by_id.get(finding_id, {})
                    if item.get("status") not in {"resolved", "accepted_exception"}:
                        fail(errors, f"blocking finding not closed: {finding_id}")
                    if item.get("status") == "accepted_exception" and not item.get("exception_approver"):
                        fail(errors, f"accepted exception lacks approver: {finding_id}")
            for round_no, report in report_rounds.items():
                if round_no > 1:
                    previous = report_rounds.get(round_no - 1, {})
                    previous_ids = report_finding_ids.get(round_no - 1, set())
                    if not report.get("parent_review_run_id") or report.get("parent_review_run_id") != previous.get("review_run_id") or not report.get("consumed_finding_ids") or not set(report.get("consumed_finding_ids", [])).issubset(previous_ids):
                        fail(errors, f"round {round_no} lacks parent_review_run_id or consumed_finding_ids")
                    if report.get("reviewer", {}).get("input_revision") == data.get("baseline_revision") and data.get("review_state") != "blocked":
                        fail(errors, f"round {round_no} must review a post-consumption revision")
        if evidence_payload is not None:
            evidence_ids: set[str] = set()
            for evidence in evidence_payload:
                if not isinstance(evidence, dict):
                    fail(errors, "evidence registry entries must be objects")
                    continue
                evidence_id = evidence.get("evidence_id")
                if not evidence_id or evidence_id in evidence_ids:
                    fail(errors, f"evidence_id must be unique and non-empty: {evidence_id}")
                evidence_ids.add(str(evidence_id))
                for field in ("kind", "input_revision", "result_artifact", "scope"):
                    if not evidence.get(field):
                        fail(errors, f"evidence entry missing {field}: {evidence_id}")
                if evidence.get("kind") not in {"test_result", "benchmark_result", "inventory", "decision_record", "runtime_trace"}:
                    fail(errors, f"invalid evidence kind: {evidence_id}")
                if evidence.get("input_revision") not in report_revisions and evidence.get("input_revision") != current_revision:
                    fail(errors, f"evidence revision is not bound to a reviewed/current revision: {evidence_id}")
                result_artifact = evidence.get("result_artifact")
                if result_artifact and (safe_path(repo_root, str(result_artifact)) is None or not safe_path(repo_root, str(result_artifact)).is_file()) and (safe_path(package, str(result_artifact)) is None or not safe_path(package, str(result_artifact)).is_file()):
                    fail(errors, f"evidence result artifact does not exist: {result_artifact}")
        if review_state == "review_resolved" and gates.get("review") not in PASS:
            fail(errors, "review_resolved requires review gate pass")
        if gates.get("review") in PASS and review_state != "review_resolved":
            fail(errors, "review gate pass requires review_state=review_resolved")
        if review_state == "review_resolved":
            latest = max(report_payloads, key=lambda item: item.get("round", 0), default={})
            if latest.get("overall") != "pass" or latest.get("closure_confirmation") is not True:
                fail(errors, "review_resolved requires latest report overall=pass and closure_confirmation=true")
            receipt = data.get("dispatch_receipt")
            if not isinstance(receipt, dict) or not all(receipt.get(field) for field in ("request_id", "source_thread", "reviewer_thread", "started_at", "completed_at", "report_ref")):
                fail(errors, "review_resolved requires dispatch_receipt provenance")
            elif str(receipt["report_ref"]) not in [item for value in [documents.get("review_reports", [])] for item in (value if isinstance(value, list) else [value])] or safe_path(package, str(receipt["report_ref"])) is None or not safe_path(package, str(receipt["report_ref"])).is_file():
                fail(errors, "dispatch_receipt report_ref does not exist")
            elif receipt.get("request_id") != latest.get("review_run_id"):
                fail(errors, "dispatch_receipt request_id must match latest review_run_id")
            elif receipt.get("package_id") not in {None, data.get("package_id")} or receipt.get("reviewer_agent_id") not in {None, reviewer.get("id")}:
                fail(errors, "dispatch_receipt package/reviewer binding mismatch")
            external_ref = data.get("dispatch_receipt_ref")
            external_path = safe_path(repo_root, str(external_ref)) if external_ref else None
            if not external_ref or external_path is None or package.resolve() in external_path.parents or not external_path.is_file():
                fail(errors, "review_resolved requires an existing out-of-package dispatch_receipt_ref")
            else:
                try:
                    external_receipt = json.loads(external_path.read_text(encoding="utf-8"))
                    required = ("request_id", "package_id", "source_thread_id", "reviewer_thread_id", "reviewer_id", "runtime_agent_id", "input_revision", "report_ref", "dispatch_status", "producer")
                    if any(not external_receipt.get(field) for field in required):
                        fail(errors, "external dispatch receipt missing required fields")
                    report_paths = [item for value in [documents.get("review_reports", [])] for item in (value if isinstance(value, list) else [value])]
                    if external_receipt.get("report_ref") not in report_paths:
                        fail(errors, "external receipt report_ref must be a canonical review report")
                    if external_receipt.get("request_id") != latest.get("review_run_id") or external_receipt.get("package_id") != data.get("package_id") or external_receipt.get("reviewer_id") != reviewer.get("id") or external_receipt.get("input_revision") != latest.get("reviewer", {}).get("input_revision") or external_receipt.get("dispatch_status") != "completed":
                        fail(errors, "external dispatch receipt does not match latest review")
                    if external_receipt.get("producer") not in {"codex-runtime", "host-runtime"}:
                        fail(errors, "external dispatch receipt producer is not trusted")
                    host_log = data.get("host_dispatch_log_ref") or str(Path.home() / ".rearchitecture" / "dispatch-log" / "host-events.jsonl")
                    host_log_path = Path(host_log).expanduser()
                    if not host_log_path.is_absolute():
                        host_log_path = safe_path(repo_root, str(host_log)) or safe_path(package, str(host_log)) or host_log_path
                    if not host_log_path.is_file():
                        fail(errors, "host dispatch log does not exist")
                    else:
                        try:
                            events = [json.loads(line) for line in host_log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
                            matching = [event for event in events if event.get("request_id") == latest.get("review_run_id") and event.get("agent_id") == external_receipt.get("runtime_agent_id") and event.get("package_id") == data.get("package_id")]
                            starts = [event for event in matching if event.get("event") in {"SubagentStart", "PreToolUse"}]
                            stops = [event for event in matching if event.get("event") == "SubagentStop"]
                            if not starts or not stops:
                                fail(errors, "host dispatch log lacks matching reviewer start/stop events")
                        except (OSError, json.JSONDecodeError):
                            fail(errors, "host dispatch log is not valid JSONL")
                except (json.JSONDecodeError, OSError):
                    fail(errors, "external dispatch receipt is not valid JSON")
        history = data.get("state_history")
        if not isinstance(history, list) or not history:
            fail(errors, "state_history must contain provenance entries")
        else:
            allowed = {"draft": {"review_requested", "blocked"}, "review_requested": {"review_received", "blocked"}, "review_received": {"consumption_pending", "blocked"}, "consumption_pending": {"review_resolved", "review_requested", "blocked"}, "review_resolved": {"handoff_allowed", "blocked"}, "handoff_allowed": set(), "blocked": {"review_requested", "blocked"}}
            states = [entry.get("state") for entry in history if isinstance(entry, dict)]
            if states and states[0] != "draft":
                fail(errors, "state_history must start at draft")
            if data.get("review_state") == "review_resolved" and (states[-1] != "review_resolved" or not all(state in states for state in ("review_requested", "review_received", "consumption_pending"))):
                fail(errors, "review_resolved requires complete review request/receipt/consumption history")
            for previous, current in zip(states, states[1:]):
                if current not in allowed.get(previous, set()):
                    fail(errors, f"invalid state transition: {previous} -> {current}")
            if states and data.get("review_state") not in {states[-1], "handoff_allowed"}:
                fail(errors, "manifest review_state disagrees with state_history terminal state")
            for entry in history:
                if not isinstance(entry, dict) or any(not entry.get(field) for field in ("state", "actor", "timestamp", "input_revision", "evidence_ref")):
                    fail(errors, "each state_history entry needs state, actor, timestamp, input_revision and evidence_ref")
        round_no = data.get("review_round")
        max_rounds = data.get("max_review_rounds", 3)
        rounds = data.get("review_rounds")
        if not isinstance(round_no, int) or round_no < 0 or (round_no == 0 and data.get("review_state") != "draft"):
            fail(errors, "review_round must be a positive integer")
        if not isinstance(max_rounds, int) or max_rounds < 1 or max_rounds > 3:
            fail(errors, "max_review_rounds must be an integer from 1 to 3")
        if isinstance(round_no, int) and isinstance(max_rounds, int) and round_no > max_rounds:
            fail(errors, "review_round exceeds max_review_rounds")
        if not isinstance(rounds, list) or not rounds:
            fail(errors, "review_rounds must contain at least one round record")
        else:
            valid_round_numbers = [record.get("round", 0) for record in rounds if isinstance(record, dict) and isinstance(record.get("round"), int)]
            if isinstance(round_no, int) and valid_round_numbers and round_no != max(valid_round_numbers):
                fail(errors, "review_round must equal the latest review_rounds entry")
            for record in rounds:
                if not isinstance(record, dict) or any(not record.get(field) for field in ("round", "review_run_id", "input_revision", "trigger")):
                    fail(errors, "each review_rounds record needs round, review_run_id, input_revision and trigger")
    if profile in {"design", "implementation", "promotion"}:
        for gate in ("authority", "user_decisions", "l1", "mapping", "l2"):
            if gates.get(gate) not in PASS:
                fail(errors, f"gate not passed: {gate}")
    if profile != "orientation":
        next_task = data.get("next_task")
        if not isinstance(next_task, dict) or not next_task.get("id") or not next_task.get("owner"):
            fail(errors, "next_task must include id and owner")
        for field in ("advancement_trigger", "stop_rule"):
            if not isinstance(data.get(field), str) or not data.get(field).strip():
                fail(errors, f"{field} is required")
        evidence = data.get("promotion_evidence")
        if not isinstance(evidence, list) or not evidence or any(not isinstance(item, str) or not item.strip() for item in evidence):
            fail(errors, "promotion_evidence must be a non-empty list")
    if data.get("status") == "ready" and errors:
        fail(errors, "status ready is incompatible with failed gates")
    if data.get("status") == "ready" and data.get("review_state") in {"blocked", "review_requested", "review_received", "consumption_pending"}:
        fail(errors, "status ready is incompatible with unresolved review_state")
    if errors:
        print("Package completeness: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Package completeness: OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Package completeness: FAIL\n- checker error: {exc}", file=sys.stderr)
        raise SystemExit(1)
