## 重构目标:最小闭环版 rearchitecture-development-workflow(0.31.0)

在 `架构重构 skill 2` 工作区(已复制的 0.30.0 副本)上原位重构。先把 0.30.0 原样 commit 留基线,再叠加新版本,历史可回溯。

### 核心设计:一个循环、一个拨盘、一个台账

**循环(唯一工作流,7 步,每步一段话)**:
基线与权威 → 定位与增量范围(交付边界)→ L1 目标架构 → 现状→目标映射 + 相关 L2 → 最小垂直切片(实施时加 L3)→ 独立对抗评审+钢人 → 消费每条 finding → 交接与下一增量。

**档位(一个拨盘,取代 profiles×4 + layers×5 + phases×9 三套本体)**:
- `orientation`:跑到第 2 步,产出入口摘要 + 下一任务
- `design`:跑到第 6 步,产出完整设计包(终点是 implementation-candidate 建议,不是实施授权)
- `implementation`:design + L3/fixtures/验收/回滚;promotion 并入其中作为 authority 合并记录,不再单独立档
- Layer 0-3 与 Level L1/L2/L3 撞名问题:workflow 层不再叫 Layer,循环步骤无编号,只保留 L1/L2/L3 一套架构分类法

**最小 manifest(~8 字段,gates 全部删除——门禁状态由 checker 从"文件存在+台账消费完"机械推导,不再让模型自报,根治 0.30"改散文假装 pass"的问题)**:
```json
{
  "package_id": "R-001",
  "size": "orientation | design | implementation",
  "baseline_revision": "<rev>",
  "documents": {"scope": "00-scope.md", "l1": "02-l1.md", "...": "..."},
  "review": {"report": "review-report.json", "ledger": "review-ledger.json", "status": "pending | consumed | blocked"},
  "next_task": {"id": "…", "owner": "…"},
  "advancement_trigger": "…",
  "stop_rule": "…"
}
```

**评审协议(散文规则,取代 6 态状态机 + 回执 + host hook + provenance)**:
主会话派一个独立 sub-agent(新 context)、冻结输入(路径+revision+评审问题)、评审者只读不改包不设门禁;一轮 = 对抗+钢人同时做;报告 JSON 落盘,台账 JSON 每条 finding 必须有 id/severity/decision/consumer(文档+锚点)/owner/evidence(存在的路径或命令+产物);至多一次闭环复审(仅当阻塞 finding 已修复且输入 revision 变化),更多需用户批准;阻塞 finding 未 resolved(带证据)或未 exception(带批准人)不得交接——此规则全文只在 review.md 陈述一次(顺带修掉 close/open 笔误)。

### 文件形态(18 refs → 6,13 scripts → 3)

```
SKILL.md                    ~150 行:循环 7 步 + 档位表 + 硬门禁 + 路由表 + manifest 示例
references/
  contracts.md              L1/L2/L3 + 12 字段接口清单   ← architecture-contracts.md
  review.md                 对抗/钢人问题清单 + 报告/台账格式 + 消费规则 ← adversarial-review + review-agent-protocol(砍机制)
  user-decision-gates.md    保留,微调(决策记录进增量记录)
  delivery.md               档位细则 + 增量记录 + 迁移/晋升证据 ← deliverable-matrix + migration-and-promotion
  doc-gates.md              复杂度预算 + 过设 gate + 「新增机制五问」 ← document-and-complexity-gates + complexity-audit
  optional-concerns.md      原样保留
scripts/
  init_package.py           ~40 行,生成最小 manifest
  check_package.py          ~180 行,单一校验器(规则见下)
  validate_package.py       精简:必需文件 + 链接 + hygiene + 对 fixture 跑 check_package
fixtures/example-package/   一个带 manifest+report+ledger 的健康样例,作 checker 自测
VERSION=0.31.0、CHANGELOG.md(重启,记录裁剪决策)、README(一页,补 ZCode ~/.agents/skills/ 安装路径)、agents/openai.yaml、LICENSE
```

**整体删除**(9 个 reference + 11 个脚本):workflow-state-machine、review-loop、layered-workflow、package-completeness、semantic-evidence-contract、evidence-registry、runtime-dispatch-provenance、host-dispatch-log、hooks.json.example;以及全部 validate_* / *_hook / receipt 脚本。

**check_package.py 规则(~10 条,全机械可判)**:manifest 合法且 size ∈ 三档;documents 文件存在、不逃逸包目录、md 链接可解析;按档位校验必产文档(orientation=scope;design=+positioning/l1/mapping/l2/adr/review;implementation=+l3/fixtures/acceptance/rollback);review.status=consumed 时 report 与 ledger 的 finding ID 集合完全一致,每条有 decision/consumer/owner/evidence 且 evidence 指向存在的文件;blocking finding 必须 resolved 带证据或 exception 带批准人;next_task/advancement_trigger/stop_rule 非空。任何一条不满足输出逐条 FAIL。

### 三个根因的对应

| 历史 failure | 0.30 的补丁 | 0.31 的最小对策 |
|---|---|---|
| 模型不守流程 | 执行契约 + 25 字段 manifest + 6 态状态机 | init 脚本生成 manifest + checker 交接强制;循环压到 7 步/150 行,更可跟随 |
| 评审不被消费 | rounds + review loop + provenance | 台账是唯一强制 artifact,checker 机械验证每条 finding 被消费 |
| 越来越臃肿 | 再分层(profiles/layers) | 每个机制过「它守护闭环哪一步」一问,答不上即删;一个档位拨盘 |

### 实施步骤

1. `git add -A && git commit` 固化 0.30.0 基线
2. 重写 SKILL.md + 6 个 reference
3. 写 init_package.py、check_package.py,精简 validate_package.py
4. 建 fixtures/example-package;删除废弃文件
5. VERSION → 0.31.0,重启 CHANGELOG.md,重写 README(补 ZCode 安装路径)
6. 跑全部校验至绿;grep 验证无重复规则正身(委派规则、L3 禁令、阻塞门禁各只出现一次)、6 处 P0 矛盾不复存在
7. 按 skill-creator 的评估循环,用 2-3 个真实 prompt(design-only 请求 /「你定吧」委派 / 续作增量)做冷启动测试,跑偏再迭代

**验收线**:SKILL.md ≤160 行、references ≤6、scripts ≤3 且总量 ≤400 行;全部校验通过;每条规则单一正身。