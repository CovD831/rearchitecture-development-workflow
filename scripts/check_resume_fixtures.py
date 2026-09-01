#!/usr/bin/env python3
"""Validate the reusable resume fixtures used for skill regression checks."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "references" / "fixtures" / "resume"


def read_tree(name: str) -> str:
    fixture = ROOT / name
    files = sorted(path for path in fixture.rglob("*") if path.is_file())
    if not files:
        raise AssertionError(f"fixture {name!r} is empty")
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def main() -> int:
    healthy = read_tree("healthy")
    assert "docs/README.md" in "\n".join(
        str(path.relative_to(ROOT / "healthy"))
        for path in (ROOT / "healthy").rglob("*")
        if path.is_file()
    )
    assert "Status: promoted" in healthy
    assert "Advancement trigger:" in healthy
    assert "Promotion evidence:" in healthy
    assert "non-blocking | defer" in healthy
    assert "Increment 2" in healthy
    print("healthy: resume next increment; carry deferred EXP-2/open L2")

    blocked = read_tree("blocked")
    assert "Status: pending" in blocked
    assert "blocking | defer" in blocked
    assert "Do not start Increment 2" in blocked
    print("blocked: stop and report unmet prior gate")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"resume fixture check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
