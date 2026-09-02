# Rearchitecture Development Workflow

An evidence-driven Codex Skill for planning, reviewing and incrementally
delivering software architecture redesigns without turning the first design
package into a whole-system rewrite.

> Status: **0.9.2 public beta**. Ready for personal and team evaluation. The
> workflow has passed static validation, resume regressions, independent
> cold-start review and a real-repository design-package pilot. See
> [EVALUATION.md](EVALUATION.md) for the evidence and remaining limitations.

## What it does

The Skill helps an agent:

- recover the current architecture and existing program state before proposing
  a target;
- separate current authority, target intent, experiments and implementation
  claims;
- define an explicit Level-1 architecture, evidence-bounded Level-2 contracts
  and task-local Level-3 contracts;
- choose the smallest real migration slice and state what the first increment
  does not deliver;
- ask the user only at material decision gates and continue when the user
  explicitly delegates a reversible choice;
- maintain one canonical owner for each document claim;
- run adversarial review and bidirectional steelman, then consume every finding;
- resume later increments from repository records instead of chat memory;
- resist duplicate authorities, speculative abstractions and premature
  implementation.

It is not intended for ordinary feature work, a single bug fix or a code-only
refactor.

## Install

### Personal Codex installation

```bash
git clone https://github.com/CovD831/rearchitecture-development-workflow.git \
  ~/.codex/skills/rearchitecture-development-workflow
```

Restart or reload Codex skill discovery after installation. To update:

```bash
git -C ~/.codex/skills/rearchitecture-development-workflow pull --ff-only
```

### Team/repository installation

For a repository that discovers project skills from `.agents/skills/`, keep the
Skill versioned with the project:

```bash
git submodule add \
  https://github.com/CovD831/rearchitecture-development-workflow.git \
  .agents/skills/rearchitecture-development-workflow
```

If your agent host uses another project-level Skill directory, place this
repository at the supported equivalent path. Do not copy project-specific
architecture rules into this shared Skill; keep them in the consuming
repository's own instructions.

## Use

Invoke it explicitly with `$rearchitecture-development-workflow`, or ask for an
architecture redesign in natural language, for example:

```text
Use $rearchitecture-development-workflow to inspect this repository and prepare
the smallest design-only rearchitecture increment. Do not change runtime code.
```

```text
继续上一次架构重构。先恢复已有增量、未关闭的评审项和下一推进门禁，再判断是否可以开始下一步。
```

```text
我想重新设计这个系统的架构。先确认当前权威、目标问题、L1 边界和第一个真实切片；不确定的 L2 决策保留为实验问题。
```

The Skill deliberately right-sizes its output. A small design-only request does
not require every workflow phase or a complete Level-3 package.

## Suggested beta tests

1. **Thin-document repository:** ask for a design-only architecture proposal and
   observe whether the agent asks one material, bundled decision question.
2. **Delegated choice:** answer `你定吧` and verify that the agent records a
   reversible assumption instead of stopping or repeatedly asking.
3. **Resume:** in a fresh session, ask to continue a prior increment and verify
   that repository records and advancement evidence are checked first.
4. **Blocked resume:** leave an unmet blocking gate and verify that the agent
   reports it instead of silently beginning the next increment.
5. **Scope resistance:** request an architecture package without authorizing
   implementation and verify that no runtime code, push or PR is created.
6. **On-demand L2 detail:** ask for one L2 boundary contract and verify that the
   agent loads and applies the 12-field interface checklist without expanding
   the package to unrelated modules.

Use the feedback template in [CONTRIBUTING.md](CONTRIBUTING.md) when reporting a
test result.

## Validate

The repository uses only Python standard-library validation:

```bash
python3 scripts/validate_package.py
```

This checks package structure, metadata, reference links, portability markers,
trailing whitespace and the healthy/blocked resume fixtures. It does not replace
behavioral testing with an independent agent on a real repository.

## Repository layout

```text
SKILL.md                                  Core workflow and module router
agents/openai.yaml                       Codex UI metadata
references/deliverable-matrix.md         Artifact and increment routing
references/user-decision-gates.md        Material user decisions
references/architecture-contracts.md     L1/L2/L3 and interface contracts
references/document-and-complexity-gates.md Document and over-design controls
references/adversarial-review.md         Independent review and steelman
references/migration-and-promotion.md    Migration, experiments and promotion
references/optional-concerns.md          Plugins, isolation and version concerns
references/fixtures/                     Resume regression fixtures
scripts/check_resume_fixtures.py         Resume regression check
scripts/validate_package.py              Package validation entrypoint
```

## 中文说明

这是一个用于“架构重构开发包”的通用 Codex Skill。它强调现状证据、职责和
权威边界、渐进式迁移、L1/L2/L3 分层、文档治理、用户决策门禁、对抗性审查
以及跨会话续作。第一版只需要交付当前增量能够证明的内容，不要求一次设计或
实现完整目标系统。

## License

Released under the [MIT License](LICENSE).
