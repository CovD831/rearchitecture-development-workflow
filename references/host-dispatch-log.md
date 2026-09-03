# Host dispatch log

The package receipt is only a projection. The trust-bearing dispatch event must
be produced by the host runtime or an external dispatcher and stored outside
the package, preferably in an append-only user-level log.

Recommended event shape:

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
  "producer": "host-runtime"
}
```

The host hook/dispatcher owns creation of this event. The main session may read
it but must not be able to satisfy a resolved review by creating a replacement
event inside the package. The checker verifies the event's schema and joins it
to the package request/report; authenticity of the host log remains a runtime
trust boundary.

Codex command hooks receive one JSON object on stdin. Configure
`references/hooks.json.example` in a trusted user or repository hook layer to
run `scripts/host_dispatch_hook.py` for `SubagentStart` and `SubagentStop`.
The script writes append-only JSONL under the user's `.rearchitecture` data
directory, outside the package and repository.

After a reviewer report is received, run
`scripts/finalize_dispatch_receipt.py <package-dir> <report-file>`. It joins the
host start/stop pair to the logical reviewer report and writes the external
receipt under the repository's `.rearchitecture/dispatch-log/` directory.
Without a matching host pair, it fails and the package remains blocked.

When the host reports a repository-root `cwd`, the hook searches for active
package manifests below that directory. It associates a package only when
exactly one active package is discoverable; ambiguous or missing context stays
`null` and must remain blocked by the checker. Host `agent_id` values are
runtime identities and must be recorded separately from the human-readable
reviewer id used in the package.
