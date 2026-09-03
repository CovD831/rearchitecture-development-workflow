# Evidence registry

Evidence is a produced, revision-bound artifact, not a future filename or a
plan sentence. Each implementation or promotion package should maintain an
evidence registry alongside its review ledger.

```json
[
  {
    "evidence_id": "EV-AR-001-001",
    "kind": "test_result",
    "command": "pytest tests/test_parity.py::test_legacy_target_parity",
    "input_revision": "<revision>",
    "exit_status": 0,
    "result_artifact": "evidence/EV-AR-001-001.json",
    "scope": "AR-001"
  }
]
```

Allowed `kind` values are `test_result`, `benchmark_result`, `inventory`,
`decision_record` and `runtime_trace`. A registry entry is valid only when its
result artifact exists, its input revision matches the package revision being
reviewed, and its command/result is complete enough to reproduce or inspect.
Plans, TODOs and names of files that do not exist are not evidence.
