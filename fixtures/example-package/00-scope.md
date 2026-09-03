# Scope and authority

- Baseline revision: `a1b2c3d` (documented working tree of the scheduling service).
- In scope: job submission, scheduling authority, run lifecycle.
- Out of scope: billing, user management, dashboard.
- Authority: `docs/README.md` is the architecture authority; no earlier
  rearchitecture program exists in the repository.
- Implemented today: single-process scheduler writing job state directly from
  four call sites. Target intent marked throughout this package as **target**.
