# Rearchitecture Development Workflow

An evidence-driven agent skill for planning, reviewing and incrementally
delivering software architecture redesigns — without turning the first design
package into a whole-system rewrite.

## What it does

The skill runs one seven-step loop — baseline, frame, L1 target,
map/contract, slice, independent review, handoff — at three sizes:
`orientation` (a bounded entrypoint), `design` (a reviewable design package),
and `implementation` (one vertical slice with fixtures and rollback). A
single checker script derives gate state from what actually exists: every
review finding must be consumed into a ledger with an owner, a consumer
artifact and evidence before handoff.

It is not intended for ordinary feature work, a single bug fix or a code-only
refactor.

## Install

Personal ZCode installation:

```bash
git clone <this-repo> ~/.agents/skills/rearchitecture-development-workflow
```

Project installation (versioned with the repository):

```bash
git submodule add <this-repo> .agents/skills/rearchitecture-development-workflow
```

Codex installation is the same layout under `~/.codex/skills/`. Restart or
reload skill discovery after installing.

## Use

Ask for an architecture redesign in natural language, for example:

```text
Use rearchitecture-development-workflow to inspect this repository and prepare
the smallest design-only increment. Do not change runtime code.
```

```text
继续上一次架构重构。先恢复已有增量和未关闭的评审项，再判断是否可以开始下一步。
```

The skill right-sizes its output: a small design-only request does not
require L3 contracts, fixtures or migration evidence.

## Validate

```bash
python3 scripts/validate_package.py
```

Checks package structure, frontmatter, links, hygiene, and runs the package
checker against `fixtures/example-package/` as a self-test.

## Layout

```text
SKILL.md                       The loop, sizes, manifest, hard gates
references/contracts.md        L1/L2/L3 rules and interface checklist
references/review.md           Review protocol, adversarial/steelman questions, ledger format
references/user-decision-gates.md  Material user decisions and recording
references/delivery.md         Delivery horizon, migration evidence, promotion
references/doc-gates.md        Complexity budget and over-design gates
references/optional-concerns.md    Plugins, isolation, version coexistence
scripts/init_package.py        Create a package manifest
scripts/check_package.py       Derive and enforce gate state
fixtures/example-package/      Healthy design package (checker self-test)
```

## License

Released under the [MIT License](LICENSE).
