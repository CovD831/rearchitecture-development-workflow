#!/usr/bin/env python3
"""Validate the shareable rearchitecture workflow Skill package."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/adversarial-review.md",
    "references/deliverable-matrix.md",
    "references/user-decision-gates.md",
    "scripts/check_resume_fixtures.py",
    "VERSION",
)
OPERATIONAL_FILES = (
    ROOT / "SKILL.md",
    ROOT / "agents" / "openai.yaml",
    *sorted((ROOT / "references").glob("*.md")),
    ROOT / "scripts" / "check_resume_fixtures.py",
)
FORBIDDEN_PORTABILITY_MARKERS = (
    "/Users/",
    "MAPLE",
    "codesoul",
    "xianyu",
    ".ai-team",
    "MVP-A",
    "MVP-B",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")


def validate_frontmatter() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError as exc:
        raise AssertionError("SKILL.md frontmatter is not closed") from exc
    if not re.search(r"^name:\s+rearchitecture-development-workflow\s*$", frontmatter, re.M):
        fail("frontmatter name is missing or inconsistent")
    description = re.search(r"^description:\s+(.+)$", frontmatter, re.M)
    if not description or len(description.group(1).strip()) < 40:
        fail("frontmatter description is missing or too vague")
    if not body.strip():
        fail("SKILL.md body is empty")


def validate_metadata() -> None:
    text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    for key in ("display_name:", "short_description:", "default_prompt:"):
        if key not in text:
            fail(f"agents/openai.yaml is missing {key}")


def validate_version() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"VERSION is not semantic: {version!r}")


def validate_markdown_links() -> None:
    missing: list[str] = []
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (markdown.parent / target).resolve().exists():
                missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
    if missing:
        fail("missing relative Markdown links:\n" + "\n".join(missing))


def validate_text_hygiene() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                fail(f"trailing whitespace: {path.relative_to(ROOT)}:{line_number}")


def validate_portability() -> None:
    for path in OPERATIONAL_FILES:
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_PORTABILITY_MARKERS:
            if marker.lower() in text.lower():
                fail(f"project-specific marker {marker!r} in {path.relative_to(ROOT)}")


def validate_python() -> None:
    for script in sorted((ROOT / "scripts").glob("*.py")):
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_resume_fixtures.py")],
        check=True,
    )


def main() -> int:
    validate_required_files()
    validate_frontmatter()
    validate_metadata()
    validate_version()
    validate_markdown_links()
    validate_text_hygiene()
    validate_portability()
    validate_python()
    print("Skill package validation: OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print(f"Skill package validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
