#!/usr/bin/env python3
"""Validate the bounded independent-review loop without implementation gates."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_manifest_structure import validate as validate_manifest


def _load(package: Path, raw: object, label: str, errors: list[str]) -> list[dict]:
    values = raw if isinstance(raw, list) else [raw]
    result: list[dict] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label} mapping must contain paths")
            continue
        path = (package / value).resolve()
        if package.resolve() not in path.parents or not path.is_file():
            errors.append(f"missing {label}: {value}")
            continue
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid {label} {value}: {exc}")
            continue
        if label == "review report" and isinstance(parsed, dict):
            result.append(parsed)
        elif label == "review ledger" and isinstance(parsed, list):
            result.extend(item for item in parsed if isinstance(item, dict))
        else:
            errors.append(f"{label} must have the expected JSON shape: {value}")
    return result


def validate(package: Path) -> list[str]:
    errors = validate_manifest(package)
    manifest = package / ".rearchitecture-package.json"
    if errors or not manifest.is_file():
        return errors
    data = json.loads(manifest.read_text(encoding="utf-8"))
    state = data.get("review_state", "not_started")
    if state in {"draft", "not_started", "decision_pending"}:
        return ["review loop has not been requested"]
    reviewer = data.get("reviewer")
    if not isinstance(reviewer, dict) or not reviewer.get("id") or reviewer.get("independent") is not True:
        errors.append("reviewer must be an independent object with id")
    documents = data.get("documents", {})
    reports = _load(package, documents.get("review_reports"), "review report", errors)
    ledger = _load(package, documents.get("review_ledger"), "review ledger", errors)
    if not reports:
        errors.append("review loop requires at least one report")
    report_ids: set[str] = set()
    report_rounds: set[int] = set()
    latest_round = 0
    for report in reports:
        round_no = report.get("round")
        if not isinstance(round_no, int) or round_no < 1 or round_no in report_rounds:
            errors.append("review reports need unique positive rounds")
        else:
            report_rounds.add(round_no)
            latest_round = max(latest_round, round_no)
        if report.get("package_id") != data.get("package_id"):
            errors.append("review report package_id mismatch")
        report_reviewer = report.get("reviewer")
        if not isinstance(report_reviewer, dict):
            errors.append("review report reviewer must be an object")
        elif reviewer.get("id") and report_reviewer.get("agent_id") != reviewer.get("id"):
            errors.append("review report reviewer mismatch")
        findings = report.get("findings")
        if not isinstance(findings, list):
            errors.append("review report findings must be an array")
            continue
        for finding in findings:
            if not isinstance(finding, dict) or not finding.get("id"):
                errors.append("review finding must have a stable id")
            else:
                finding_id = str(finding["id"])
                if finding_id in report_ids and finding.get("continues_id") != finding_id:
                    errors.append(f"duplicate finding id requires continues_id: {finding_id}")
                report_ids.add(finding_id)
    ledger_ids = {str(item.get("finding_id")) for item in ledger if item.get("finding_id")}
    if report_ids != ledger_ids:
        errors.append("review findings and ledger IDs differ")
    rounds = data.get("review_rounds")
    if isinstance(rounds, list) and rounds:
        manifest_rounds = {item.get("round") for item in rounds if isinstance(item, dict)}
        if manifest_rounds != report_rounds:
            errors.append("manifest review_rounds and report rounds differ")
    if latest_round > 2 and not data.get("review_loop_exception_ref"):
        errors.append("review loop beyond two cycles requires an explicit exception record")
    return errors


def main() -> int:
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate(package)
    if errors:
        print("Review loop: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Review loop: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
