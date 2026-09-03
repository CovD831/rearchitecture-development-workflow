# Complexity audit and rule ownership

Before adding a hard gate, record its `rule_id`, layer, canonical owner,
consumer, evidence, severity and removal condition.

A new hard gate is admitted only when all answers are explicit:

1. Which layer first needs it?
2. Which concrete consumer uses it?
3. What unsafe transition does it prevent?
4. Can the checker validate it without interpreting prose?
5. Does it duplicate an existing rule or owner?

Otherwise record it as a reviewer question or warning, not a new blocker.

Simplification rules:

- one concept has one canonical field name and owner;
- later-layer requirements never leak into earlier layers;
- structural checks, semantic review and host provenance remain separate;
- malformed input is reported as `FAIL`, never as an uncaught exception;
- every fix starts with a failing fixture;
- duplicate protections are merged into one rule and one error message.

The intended checker split is:

```text
manifest/schema -> package structure -> review consumption
                 -> implementation evidence -> optional provenance
```

Until that split exists, the monolithic checker is a compatibility tool, not
proof that every layer is independently modeled.

The compatibility migration starts with two explicit entrypoints:

- `--phase manifest` for schema and basic structure;
- `--phase design-core` for the minimum Layer 1 loop.
- `--phase review-loop` for the bounded independent-review loop.
- `--phase implementation-evidence` for the selected implementation slice.
- `--phase provenance` only for an explicit external-dispatch proof claim.

New manifests opt into the layered aggregator with
`validation_mode: "layered"`. Existing manifests are not silently migrated;
this avoids changing the meaning of already-published packages.

Later phases should be added as separate validators before the strict default
checker is retired.
