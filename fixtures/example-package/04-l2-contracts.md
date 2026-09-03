# L2 contracts

## Job Store write boundary

- Responsibility: sole writer of durable job records; exposes one command
  (`submit`, `transition`), one immutable query view, and one receipt form.
- Non-responsibility: ordering, admission policy, execution.
- Current components: `scheduler/core.py` write sites move behind the store;
  `worker/poll.py` rewrites become store transitions.
- Provided services: `store.submit(cmd) -> receipt`, `store.transition(cmd) ->
  receipt`, `store.view(job_id) -> immutable view`.
- Required services: durable record storage (existing table, unchanged
  schema).
- Writable authority: job rows only; the store never writes schedule or
  worker tables.
- Allowed calls: Scheduler and Runtime may call commands and views; nothing
  else touches job rows.
- Lifecycle and failure: store reports and contains write failures; unknown
  external outcomes are reconciled by receipt replay, never blind retry.
- Compatibility: legacy direct writes remain executable behind a fixture
  until the removal gate in the map passes.

Claims: established — sole-writer rule and command forms; conditional —
receipt replay semantics; open — none in this increment.

## Scheduler/Store interaction

Commands and receipts only; the Scheduler never reads job rows except through
the immutable view.
