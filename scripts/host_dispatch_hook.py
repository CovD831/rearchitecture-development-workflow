#!/usr/bin/env python3
"""Record Codex SubagentStart/SubagentStop events in a user-level log."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def package_info(cwd: str) -> tuple[str | None, str | None]:
    path = Path(cwd).resolve()
    candidates: list[tuple[str, str]] = []
    for directory in (path, *path.parents):
        manifest = directory / ".rearchitecture-package.json"
        if manifest.is_file():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                rounds = data.get("review_rounds", [])
                latest = max((item for item in rounds if isinstance(item, dict)), key=lambda item: item.get("round", 0), default={})
                package_id, request_id = data.get("package_id"), latest.get("review_run_id")
                if package_id and request_id:
                    candidates.append((package_id, request_id))
            except (OSError, json.JSONDecodeError, ValueError):
                continue
    if not candidates:
        for manifest in path.rglob(".rearchitecture-package.json"):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                rounds = data.get("review_rounds", [])
                latest = max((item for item in rounds if isinstance(item, dict)), key=lambda item: item.get("round", 0), default={})
                if data.get("review_state") in {"review_requested", "review_received", "consumption_pending", "blocked"} and data.get("package_id") and latest.get("review_run_id"):
                    candidates.append((data["package_id"], latest["review_run_id"]))
            except (OSError, json.JSONDecodeError, ValueError):
                continue
    return candidates[0] if len(candidates) == 1 else (None, None)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    if event.get("hook_event_name") not in {"SubagentStart", "SubagentStop"}:
        return 0
    package_id, request_id = package_info(str(event.get("cwd", ".")))
    record = {"event": event.get("hook_event_name"), "timestamp": datetime.now(timezone.utc).isoformat(), "session_id": event.get("session_id"), "turn_id": event.get("turn_id"), "agent_id": event.get("agent_id"), "runtime_agent_id": event.get("agent_id"), "agent_type": event.get("agent_type"), "cwd": event.get("cwd"), "package_id": package_id, "request_id": request_id}
    log_dir = Path.home() / ".rearchitecture" / "dispatch-log"
    log_dir.mkdir(parents=True, exist_ok=True)
    with (log_dir / "host-events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
