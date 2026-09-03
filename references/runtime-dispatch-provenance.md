# Runtime dispatch provenance

Package-local JSON is self-attested and cannot prove that an independent
reviewer was actually dispatched. A resolved review therefore requires an
out-of-package dispatch receipt produced by the runtime/orchestrator.

Recommended location:

```text
<repository>/.rearchitecture/dispatch-log/<review_run_id>.json
```

The receipt must be written outside the package directory and contain:

```json
{
  "request_id": "R-001-review-01",
  "package_id": "R-001",
  "source_thread_id": "main-thread",
  "reviewer_thread_id": "independent-thread",
  "reviewer_id": "/root/independent_arch_review",
  "runtime_agent_id": "runtime-agent-uuid",
  "input_revision": "<revision>",
  "report_ref": "docs/rearchitecture/R001/review-report.json",
  "dispatch_status": "completed",
  "started_at": "<timestamp>",
  "completed_at": "<timestamp>",
  "producer": "codex-runtime"
}
```

The checker verifies location, schema and cross-references. It cannot prove
the producer's identity or that the runtime did not forge its own log; that is
an explicit trust boundary owned by the host runtime. Without an external
receipt, a non-orientation package may remain `review_received` or `blocked`,
but may not become `review_resolved` or `handoff_allowed`.
