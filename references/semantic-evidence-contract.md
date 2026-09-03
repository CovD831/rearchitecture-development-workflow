# Semantic evidence contract

Structural references are not evidence. A consumer or evidence reference must
be a typed object, not an arbitrary plan phrase.

```json
{
  "kind": "path",
  "ref": "tests/test_parity.py::test_legacy_target_parity",
  "exists": true
}
```

Allowed kinds are:

- `path`: a repository/package file, optionally with `::symbol` or `#anchor`;
- `command`: a reproducible command plus a checked result artifact;
- `record`: a durable decision, approval or external result record.

The checker resolves `path` references against the repository root and requires
the file to exist. `command` and `record` references must include a result or
record path that exists. A phrase such as `S1 L3 contract`, `future test` or
`inventory script and checked-in baseline` is invalid evidence.

For every review round, the union of report finding IDs and ledger finding IDs
must match exactly. A later-round finding cannot disappear from the ledger, and
a ledger entry cannot exist without a corresponding report finding.
