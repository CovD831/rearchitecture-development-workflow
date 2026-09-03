#!/usr/bin/env python3
"""Check a rearchitecture package: manifest, artifacts, and finding consumption.

Gate state is derived here, never declared: the package passes only when the
required artifacts exist and every review finding is consumed with evidence.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SIZES = {
    "orientation": ("scope",),
    "design": ("scope", "positioning", "l1", "mapping", "l2", "adr", "handoff", "review_report", "review_ledger"),
    "implementation": ("scope", "positioning", "l1", "mapping", "l2", "adr", "handoff", "l3", "fixtures", "acceptance", "rollback", "review_report", "review_ledger"),
}
REVIEW_STATUSES = {"pending", "consumed", "blocked"}
SEVERITIES = {"blocking", "non-blocking"}
DECISIONS = {"accepted", "rejected", "deferred", "exception"}


def repo_root(package: Path) -> Path | None:
    for parent in (package, *package.parents):
        if (parent / ".git").exists():
            return parent
    return None


def existing_path(package: Path, raw: str) -> Path | None:
    candidate = Path(raw)
    if candidate.is_absolute():
        return None
    roots = [package]
    root = repo_root(package)
    if root is not None:
        roots.append(root)
    for base in roots:
        resolved = (base / candidate).resolve()
        if resolved == base.resolve() or base.resolve() in resolved.parents:
            if resolved.is_file():
                return resolved
    return None


def contained(package: Path, raw: str) -> Path | None:
    candidate = Path(raw)
    if candidate.is_absolute():
        return None
    resolved = (package / candidate).resolve()
    if resolved != package.resolve() and package.resolve() not in resolved.parents:
        return None
    return resolved


def check(package: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = package / ".rearchitecture-package.json"
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path}"]
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid manifest: {exc}"]

    size = data.get("size")
    if size not in SIZES:
        errors.append("size must be orientation, design or implementation")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", str(data.get("package_id", ""))):
        errors.append("package_id is missing or invalid")
    if not str(data.get("baseline_revision", "")).strip():
        errors.append("baseline_revision is required")

    documents = data.get("documents")
    if not isinstance(documents, dict):
        errors.append("documents must be an object")
        documents = {}
    report: dict = {}
    ledger: list = []
    for key in SIZES.get(size, ()):
        values = documents.get(key)
        values = values if isinstance(values, list) else [values]
        if any(not isinstance(item, str) or not item.strip() for item in values):
            errors.append(f"missing document mapping: {key}")
            continue
        for item in values:
            target = contained(package, item)
            if target is None:
                errors.append(f"document escapes package directory: {item}")
            elif not target.is_file():
                errors.append(f"missing document: {item}")
            elif target.suffix == ".md":
                text = target.read_text(encoding="utf-8")
                for link in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
                    link = link.split("#", 1)[0].strip()
                    if link and "://" not in link and not (target.parent / link).resolve().exists():
                        errors.append(f"broken link in {item}: {link}")
            elif target.suffix == ".json" and key == "review_report":
                try:
                    report = json.loads(target.read_text(encoding="utf-8"))
                    if not isinstance(report, dict):
                        errors.append(f"review report must be an object: {item}")
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"invalid review report {item}: {exc}")
            elif target.suffix == ".json" and key == "review_ledger":
                try:
                    ledger = json.loads(target.read_text(encoding="utf-8"))
                    if not isinstance(ledger, list):
                        errors.append(f"review ledger must be an array: {item}")
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"invalid review ledger {item}: {exc}")

    review = data.get("review")
    if not isinstance(review, dict) or review.get("status") not in REVIEW_STATUSES:
        errors.append("review.status must be pending, consumed or blocked")
    elif size != "orientation" and review.get("status") in {"consumed", "blocked"}:
        errors.extend(check_review(package, report, ledger, consumed=review.get("status") == "consumed"))

    next_task = data.get("next_task")
    if not isinstance(next_task, dict) or not next_task.get("id") or not next_task.get("owner"):
        errors.append("next_task must include id and owner")
    if size != "orientation":
        for field in ("advancement_trigger", "stop_rule"):
            if not str(data.get(field, "")).strip():
                errors.append(f"{field} is required")
    return errors


def check_review(package: Path, report: dict, ledger: list, consumed: bool) -> list[str]:
    errors: list[str] = []
    findings = report.get("findings")
    if not isinstance(findings, list) or not findings:
        return ["review report has no findings"]
    if not isinstance(report.get("steelman"), dict) or not report["steelman"].get("decision_refs"):
        errors.append("review report steelman lacks decision_refs")

    report_ids: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict) or not finding.get("id"):
            errors.append("review finding without stable id")
            continue
        finding_id = str(finding["id"])
        if finding_id in report_ids:
            errors.append(f"duplicate finding id: {finding_id}")
        report_ids.add(finding_id)
        if finding.get("severity") not in SEVERITIES:
            errors.append(f"invalid severity: {finding_id}")
        if not str(finding.get("statement", "")).strip():
            errors.append(f"finding statement missing: {finding_id}")

    ledger_by_id: dict[str, dict] = {}
    for entry in ledger:
        if not isinstance(entry, dict) or not entry.get("finding_id"):
            errors.append("ledger entry without finding_id")
            continue
        finding_id = str(entry["finding_id"])
        if finding_id in ledger_by_id:
            errors.append(f"duplicate ledger entry: {finding_id}")
        ledger_by_id[finding_id] = entry

    if report_ids != set(ledger_by_id):
        errors.append(
            "report and ledger finding IDs differ: "
            f"report-only={sorted(report_ids - set(ledger_by_id))} "
            f"ledger-only={sorted(set(ledger_by_id) - report_ids)}"
        )

    for finding_id, entry in ledger_by_id.items():
        if entry.get("severity") not in SEVERITIES:
            errors.append(f"invalid severity in ledger: {finding_id}")
        if entry.get("decision") not in DECISIONS:
            errors.append(f"invalid decision: {finding_id}")
        if not str(entry.get("owner", "")).strip():
            errors.append(f"ledger entry lacks owner: {finding_id}")
        consumer = entry.get("consumer")
        if not isinstance(consumer, dict) or not consumer.get("path"):
            errors.append(f"ledger entry lacks consumer path: {finding_id}")
        else:
            target = contained(package, str(consumer["path"]))
            if target is None or not target.is_file():
                errors.append(f"consumer path does not exist: {finding_id}")
            elif not str(consumer.get("anchor", "")).lower() in target.read_text(encoding="utf-8").lower():
                errors.append(f"consumer anchor not found in {consumer['path']}: {finding_id}")
        if entry.get("decision") == "exception" and not str(entry.get("approver", "")).strip():
            errors.append(f"exception lacks approver: {finding_id}")
        evidence = str(entry.get("evidence", "")).strip()
        if evidence:
            raw = evidence.split("::", 1)[0].split("#", 1)[0]
            if existing_path(package, raw) is None:
                errors.append(f"evidence path does not exist: {finding_id}")
        if entry.get("status") not in {"open", "closed"}:
            errors.append(f"invalid status: {finding_id}")
        blocking = entry.get("severity") == "blocking"
        if blocking and consumed:
            if entry.get("status") != "closed":
                errors.append(f"blocking finding left open: {finding_id}")
            if entry.get("decision") == "accepted" and not evidence:
                errors.append(f"accepted blocking finding lacks evidence: {finding_id}")
    return errors


def main() -> int:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = check(package)
    if errors:
        print("Package check: FAIL", file=sys.stderr)
        for error in dict.fromkeys(errors):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Package check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
