# Positioning and delivery horizon

- User: backend teams building on the scheduling service; the problem is that
  every new job type edits the scheduler core because job state has no owner.
- First deployment boundary: one process; the boundary is a module boundary,
  not a service split.
- Non-goals: multi-tenant isolation, horizontal scaling, plugin system.

## Delivery horizon

- Delivers: owned write boundary for job state, parity fixtures, migration
  plan for the four call sites.
- Defers: read-model extraction, retry-policy ownership, cross-service
  identity.
- Advancement trigger: write-boundary parity tests pass on legacy and target
  paths.
- Stop rule: stop and preserve the current path if the write boundary cannot
  be frozen without breaking the scheduling authority.
