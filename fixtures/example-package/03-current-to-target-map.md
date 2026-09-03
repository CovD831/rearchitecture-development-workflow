# Current-to-target map

| Current hotspot | Action | Current owner | Target owner | Removal gate |
|---|---|---|---|---|
| `scheduler/core.py` direct job-row writes (4 call sites) | split | scheduler core | Job Store | all four call sites route through the store command |
| `scheduler/admission.py` admission decisions | retain | scheduler | Scheduler (unchanged) | n/a |
| `worker/poll.py` status rewrites | adapt | worker poller | Job Store command + receipt | poller writes removed |
| `scripts/backfill_job_rows.py` | deprecate | ops script | Job Store bulk command | backfill rerun succeeds through the store |
