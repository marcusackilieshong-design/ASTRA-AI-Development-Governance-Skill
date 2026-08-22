# ASTTRA AI Development Governance

[English](#english) · [简体中文](#简体中文)

<a id="english"></a>

## English

A repository-centered AI development governance and continuity skill for long-lived software projects.

It helps Codex and other coding agents reconstruct project state after context compaction, interruptions, window changes, or agent handoffs—without turning project records into an ever-growing transcript.

> Conversation is disposable. Repository is persistent.

The canonical invocation name is `$ai-development-governance`.

### What problem does it solve?

Long-running collaboration with coding agents commonly fails in predictable ways:

- the agent loses the project objective or implementation position after context compaction;
- a small temporary request silently replaces the primary task;
- fixing one local symptom is mistaken for completing the whole task;
- a new window trusts an old conversation summary without checking code and Git;
- architectural decisions, compatibility constraints, and rejected approaches are not traceable;
- state files grow into verbose AI diaries and consume the context they were meant to preserve;
- Git commits and task records cannot be traced in both directions;
- governance depends entirely on model discipline instead of mechanical validation.

The goal is not to make a model remember every conversation. The goal is to let any new agent recover the correct working state from repository evidence.

### Core principles

#### Repository as the system of record

When sources disagree, use this evidence order:

1. current code and Git;
2. `.ai/STATE.md` and active task records;
3. accepted project documentation and ADRs;
4. conversation history.

Project knowledge lives in each project repository. The skill defines how to record, recover, and validate that knowledge; it never stores project-specific state inside the skill itself.

#### Bounded context

Project recovery uses a three-tier working set:

| Tier | Contents | Reading rule |
|---|---|---|
| Hot | `STATE.md` and the active Task Stack | Read on every RESUME and keep strictly bounded |
| Warm | `PROJECT.md`, relevant ADRs, relevant diffs, and task-linked commits | Read only when required by active work |
| Cold | Completed tasks, unrelated ADRs, and old Git history | Do not load by default; read only when referenced or resolving a conflict |

`STATE.md` is limited to 120 lines and 12 KiB. Routine validation checks only hot state and the configured Git range. Cold history is scanned only when `--full` is requested explicitly.

#### Local changes do not replace the primary task

The Task Stack supports:

- `EPIC`: a sustained outcome spanning multiple tasks;
- `TASK`: an independently deliverable change with its own Definition of Done;
- `SUBTASK`: a recoverable step required by the current task;
- `PATCH`: a small, low-risk correction within the current objective;
- `INTERRUPT`: unrelated temporary work that suspends but does not replace active work.

The primary lineage is `EPIC → TASK → SUBTASK`. PATCH and INTERRUPT are temporary frames. When they close, the suspended primary task must be restored.

#### Goal Guard and Definition of Done

Before a meaningful change, the agent must establish:

1. which task owns the change;
2. which parent objective it advances;
3. whether it is a continuation, child, patch, interruption, or objective replacement;
4. which constraints or accepted ADRs it may affect;
5. which observable result and verification will prove completion.

A task cannot close merely because one symptom disappeared. Every required Definition of Done item and its verification evidence must be complete before the task becomes `DONE`.

### Lifecycle

| Mode | Purpose | Primary output |
|---|---|---|
| INIT | Adopt governance in a new or existing project | `AGENTS.md`, `.ai/`, initial task, and current state |
| RESUME | Recover after a new window, new agent, pause, or context compaction | A Git-reconciled takeover report |
| WORK | Perform normal development | Goal-anchored, scope-classified implementation |
| CHECKPOINT | Capture a logical stage, pause, blocker, or handoff | A recoverable task checkpoint and compact STATE |
| CLOSE | Finish a task | Closed DoD, verification, ADR, and Git traceability loop |

### Generated project structure

```text
PROJECT/
├─ AGENTS.md
└─ .ai/
   ├─ PROJECT.md
   ├─ STATE.md
   ├─ CHANGE_POLICY.md
   ├─ TRACEABILITY_BASELINE
   ├─ tasks/
   │  └─ TASK-001.md
   └─ decisions/
```

Responsibilities:

- `AGENTS.md`: stable rules every agent must follow in the repository;
- `PROJECT.md`: purpose, architecture, commands, critical constraints, and sensitive areas;
- `STATE.md`: current stack, focus, latest checkpoint, and next action—not historical narration;
- `tasks/`: objective, scope, DoD, checkpoints, Impact Review, verification, and Git references;
- `decisions/`: consequential architectural decisions;
- `CHANGE_POLICY.md`: change levels, Impact Review triggers, and authorization boundaries;
- `TRACEABILITY_BASELINE`: Git commit at which governance became active.

### Installation

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
git clone https://github.com/marcusackilieshong-design/ASTTRA-AI-Development-Governance.git "$HOME\.agents\skills\ai-development-governance"
```

#### macOS / Linux

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/marcusackilieshong-design/ASTTRA-AI-Development-Governance.git "$HOME/.agents/skills/ai-development-governance"
```

Codex normally detects the skill automatically. Restart Codex if it does not appear.

### Invocation

#### Explicit invocation

```text
$ai-development-governance
```

#### Natural-language invocation

Examples include:

```text
Initialize AI development governance for this long-lived project.
```

```text
Resume this governed project from repository state and verify it against Git before editing.
```

Chinese natural-language triggers are also included in the skill description; see the Chinese section below.

### Common workflows

#### 1. Initialize a project

Tell Codex from the target project directory:

```text
Use $ai-development-governance in INIT mode for the current project.
Inspect the repository, Git state, build/test configuration, and existing documentation first.
Do not overwrite existing governance files.
```

You can also run the initializer directly:

```text
python <skill-directory>/scripts/init_project.py <project-root> \
  --project-name "My Project" \
  --purpose "The durable project objective" \
  --task-id TASK-001
```

The initializer refuses to overwrite existing files by default. Use `--force` only after explicitly accepting the overwrite risk.

#### 2. Continue normal development

```text
Use $ai-development-governance to continue the active task.
Apply Goal Guard, identify the owning task and Definition of Done, then begin the scoped change.
```

Small related changes become PATCH or SUBTASK work. Unrelated temporary work becomes an INTERRUPT. None of them silently replaces the primary objective.

#### 3. Create a checkpoint

```text
Use $ai-development-governance in CHECKPOINT mode.
Reconcile code and Git, update the active task and STATE, record verification,
and leave one executable Next Action.
```

A checkpoint is a recoverable engineering boundary. It does not require a Git commit and must not become a log of file reads, ordinary commands, or chat history.

#### 4. Handoff between old and new windows

Send this in the old window:

```text
Use the AI Development Governance skill in CHECKPOINT mode to prepare a new-window handoff.
Reconcile code, Git, the active Task Stack, and verification evidence.
Update the active task and `.ai/STATE.md`, leave one executable Next Action,
run the mechanical checks, then stop before starting the next implementation stage.
```

Open a new window against the same project working directory and send:

```text
Use the AI Development Governance skill in RESUME mode to take over this project.
Do not assume access to the old conversation and do not edit code yet.
Read AGENTS, STATE, the active tasks, and relevant ADRs; reconcile them with Git,
the relevant diff, and verification evidence; then provide a takeover report and wait.
```

The takeover report should include the current objective, Task Stack, completed and unfinished work, critical constraints, Git/working-tree state, verification, exact next action, and any conflict between records and repository evidence.

After reviewing it, reply:

```text
Confirmed. Continue the active task and execute the recorded Next Action.
```

> The new window must see the old window's real working tree. An independent Git worktree normally cannot see uncommitted changes from another worktree. Use the same checkout, or create a traceable checkpoint commit first when the user explicitly authorizes it.

#### 5. Close a task

```text
Use $ai-development-governance in CLOSE mode.
Verify every Definition of Done item, reconcile ADRs and bidirectional Git traceability,
and close the task only after validation passes.
```

### Change levels and ADRs

Changes are classified as:

- `L0`: read-only analysis; no task-state mutation;
- `L1`: local, reversible PATCH with no contract change;
- `L2`: multi-file or internal behavior change represented by a SUBTASK or TASK;
- `L3`: architecture, public API, persistent data, security boundary, dependency strategy, or compatibility commitment change.

Impact Review—and normally an ADR—is triggered when a change:

- modifies a public API, CLI, format, schema, database, or protocol;
- changes architectural boundaries, critical dependencies, deployment, or recovery behavior;
- affects security, privacy, performance budgets, or backward compatibility;
- conflicts with an accepted ADR or stable constraint;
- requires migration or is difficult to roll back.

### Mechanical validation

#### State and local references

```text
python <skill-directory>/scripts/validate_state.py <project-root>
```

This checks:

- required project-memory files;
- STATE structure, valid statuses, and context size;
- whether Active Task is the top stack frame;
- whether Task Stack references exist and types match;
- whether STATE and active-task statuses agree;
- whether a DONE task still has unchecked DoD items;
- whether ADR references resolve.

#### Bidirectional Git and Task traceability

```text
python <skill-directory>/scripts/check_traceability.py <project-root>
```

This checks:

- whether product commits after the governance baseline contain a Task ID;
- whether Task IDs referenced by commits exist;
- whether task records link back to their commits;
- whether task-record commit references exist and name the owning task;
- whether product working-tree changes have a valid Active Task.

Recommended commit subject:

```text
TASK-042: implement unload lifecycle
```

Routine checks scan only hot state and post-baseline commits. For an explicit cold-history audit, use:

```text
python <skill-directory>/scripts/validate_state.py <project-root> --full
python <skill-directory>/scripts/check_traceability.py <project-root> --full
```

### Skill repository layout

```text
ASTTRA-AI-Development-Governance/
├─ SKILL.md
├─ README.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ lifecycle.md
│  ├─ task-model.md
│  ├─ change-policy.md
│  ├─ checkpoint-policy.md
│  └─ adr-policy.md
├─ templates/
│  ├─ AGENTS.template.md
│  ├─ PROJECT.template.md
│  ├─ STATE.template.md
│  ├─ TASK.template.md
│  └─ ADR.template.md
└─ scripts/
   ├─ init_project.py
   ├─ validate_state.py
   └─ check_traceability.py
```

### Behavioral boundaries

Activating this skill does not authorize an agent to:

- commit or push automatically;
- overwrite existing governance files;
- rewrite Git history;
- publish, deploy, or perform destructive cleanup;
- broaden a local fix into an unrequested refactor.

Those actions still require normal user authorization.

### Current version

Version 0.1 focuses on the smallest complete continuity loop: project memory, Task Stack, Goal Guard, Checkpoints, ADRs, Impact Review, Git traceability, and mechanical validation.

Feedback from real long-running projects is welcome through GitHub Issues.

---

<a id="简体中文"></a>

## 简体中文

面向长期维护软件项目的、以仓库为中心的 AI 开发治理与连续性 Skill。

它帮助 Codex 及其他 coding agent 在聊天上下文压缩、任务中断、新窗口切换或新 agent 接管后，仍能从仓库中可靠地重建项目状态，同时避免为了记录而制造不断膨胀的上下文。

> Conversation is disposable. Repository is persistent.

Skill 的正式调用名是：`$ai-development-governance`。

### 它解决什么问题

长期与 coding agent 协作时，常见风险包括：

- 聊天上下文压缩或丢失后，agent 忘记项目目标和施工位置；
- 临时小修改替换了主任务，完成后没有回到原目标；
- 修复一个局部症状就把整个任务标记为完成；
- 新窗口只依赖旧对话摘要，没有核对实际代码和 Git；
- 架构决策、兼容性约束和失败方案没有留下可追溯记录；
- 状态文件逐渐变成巨大的 AI 日记，反过来消耗上下文；
- Git 提交与任务记录彼此无法追溯；
- 工作机制只依赖模型“自觉”，缺少机械校验。

本 Skill 的目标不是让模型记住所有聊天，而是让任何新 agent 都能从仓库事实恢复到正确的工作位置。

### 核心原则

#### Repository as System of Record

发生冲突时，证据优先级为：

1. 当前代码与 Git；
2. `.ai/STATE.md` 与活跃任务记录；
3. 已接受的项目文档与 ADR；
4. 历史聊天上下文。

项目知识保存在项目仓库中，Skill 只定义如何记录、恢复和校验，不保存任何具体项目的状态。

#### 有边界的上下文

恢复项目时使用三层工作集：

| 层级 | 内容 | 读取规则 |
|---|---|---|
| Hot | `STATE.md` 与活跃 Task Stack | 每次 RESUME 必读，严格保持短小 |
| Warm | `PROJECT.md`、相关 ADR、相关 diff 与任务提交 | 根据当前任务按需读取 |
| Cold | 已完成任务、无关 ADR、旧 Git 历史 | 默认不加载，只在引用或冲突调查时读取 |

`STATE.md` 被限制在 120 行、12 KiB 以内。常规校验只扫描热状态和配置的 Git 范围；只有显式使用 `--full` 才检查冷历史。

#### 局部修改不替换主任务

Task Stack 支持：

- `EPIC`：跨多个任务的长期目标；
- `TASK`：可独立交付、具有 Definition of Done 的任务；
- `SUBTASK`：当前任务的一个可恢复步骤；
- `PATCH`：当前目标内的小型低风险修正；
- `INTERRUPT`：与当前目标无关的临时插入工作。

主链是 `EPIC → TASK → SUBTASK`。PATCH 和 INTERRUPT 是临时栈帧，完成后必须恢复被挂起的主任务。

#### Goal Guard 与 Definition of Done

进行有意义的修改前，agent 必须确认：

1. 哪个任务拥有这次变更；
2. 它推进哪个父目标；
3. 它是继续、子任务、补丁、中断还是目标替换；
4. 它可能影响哪些约束或 ADR；
5. 什么可观察结果和验证能够证明完成。

任务不能因为某个局部症状消失就关闭。所有必需的 Definition of Done 条目和验证证据完成后，才能标记为 `DONE`。

### 工作生命周期

| 模式 | 用途 | 主要输出 |
|---|---|---|
| INIT | 首次建立项目治理框架 | `AGENTS.md`、`.ai/`、初始任务与状态 |
| RESUME | 新窗口、新 agent、上下文压缩后接管 | 经 Git 核对的接管报告 |
| WORK | 日常开发 | 受 Goal Guard 和变更分级约束的实现 |
| CHECKPOINT | 逻辑阶段、暂停、阻塞或交接 | 可恢复的任务检查点和短 STATE |
| CLOSE | 任务收尾 | DoD、验证、ADR 与 Git 追溯闭环 |

### 初始化后生成的项目结构

```text
PROJECT/
├─ AGENTS.md
└─ .ai/
   ├─ PROJECT.md
   ├─ STATE.md
   ├─ CHANGE_POLICY.md
   ├─ TRACEABILITY_BASELINE
   ├─ tasks/
   │  └─ TASK-001.md
   └─ decisions/
```

文件职责：

- `AGENTS.md`：进入仓库后 agent 必须遵守的稳定规则；
- `PROJECT.md`：项目目的、架构、命令、关键约束和敏感区域；
- `STATE.md`：当前任务栈、焦点、最近检查点和下一步，不保存历史流水；
- `tasks/`：任务目标、范围、DoD、检查点、Impact Review、验证和 Git 引用；
- `decisions/`：重要架构决策记录；
- `CHANGE_POLICY.md`：变更分级、Impact Review 和授权边界；
- `TRACEABILITY_BASELINE`：启用治理时的 Git 基线。

### 安装

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
git clone https://github.com/marcusackilieshong-design/ASTTRA-AI-Development-Governance.git "$HOME\.agents\skills\ai-development-governance"
```

#### macOS / Linux

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/marcusackilieshong-design/ASTTRA-AI-Development-Governance.git "$HOME/.agents/skills/ai-development-governance"
```

Codex 通常会自动发现 Skill；如果没有出现，请重启 Codex。

### 如何调用

#### 显式调用

```text
$ai-development-governance
```

#### 中文自然语言触发

可以直接使用：

```text
AI开发项目构架建立：为当前项目初始化长期开发治理框架。
```

也支持类似表达：

- AI开发项目架构建立；
- 建立AI开发项目治理框架；
- 初始化长期开发项目；
- 接管或继续长期维护项目。

### 常用工作流

#### 1. 初始化一个新项目

在目标项目目录中告诉 Codex：

```text
使用 $ai-development-governance 以 INIT 模式初始化当前项目。
先检查仓库、Git、构建测试配置和已有文档；不要覆盖现有治理文件。
```

也可以直接运行初始化脚本：

```text
python <skill-directory>/scripts/init_project.py <project-root> \
  --project-name "My Project" \
  --purpose "项目的长期目标" \
  --task-id TASK-001
```

初始化脚本默认拒绝覆盖已有文件。`--force` 只能在明确确认覆盖风险后使用。

#### 2. 日常开发

```text
使用 $ai-development-governance 继续当前任务。
先应用 Goal Guard，确认变更所属任务和 Definition of Done，再开始修改。
```

临时小修改会作为 PATCH 或 SUBTASK；无关的临时工作会作为 INTERRUPT。它们不会静默替换主任务。

#### 3. 创建 Checkpoint

```text
使用 $ai-development-governance 进入 CHECKPOINT 模式。
核对代码和 Git，更新活跃任务与 STATE，记录验证结果和一个明确的 Next Action。
```

Checkpoint 表示可恢复的工程边界，不要求 Git commit，也不应该记录文件读取、普通命令或聊天流水。

#### 4. 新旧窗口交接

旧窗口发送：

```text
请使用“AI 开发项目治理”Skill，以 CHECKPOINT 模式为切换新窗口执行交接。
核对代码、Git、活跃 Task Stack 和验证结果；更新活跃 TASK 与 `.ai/STATE.md`，
留下一个可直接执行的 Next Action，运行机械校验，然后停止，不要继续下一阶段。
```

打开指向同一项目工作区的新窗口后发送：

```text
请使用“AI 开发项目治理”Skill，以 RESUME 模式接管这个长期维护项目。
不要假设拥有旧窗口的聊天记录，也不要立即修改代码。
读取 AGENTS、STATE、活跃任务与相关 ADR，核对 Git、diff 和验证证据，
然后先输出接管报告，等待我确认。
```

接管报告至少应包含：当前主目标、任务栈、已完成和未完成内容、关键约束、Git/工作区状态、验证结果、下一步动作以及记录与实际仓库之间的冲突。

确认后回复：

```text
确认，继续当前任务，执行记录中的 Next Action。
```

> 新窗口必须看到旧窗口的真实工作区。独立 Git worktree 通常看不到另一个 worktree 的未提交修改；这种情况下应使用同一工作目录，或在获得用户授权后先创建可追溯的 checkpoint commit。

#### 5. 关闭任务

```text
使用 $ai-development-governance 进入 CLOSE 模式。
逐项验证 Definition of Done，核对 ADR 和 Git 双向追溯，通过校验后再关闭任务。
```

### 变更分级与 ADR

变更分为：

- `L0`：只读分析，不修改任务状态；
- `L1`：局部、可逆、无契约变化的 PATCH；
- `L2`：跨文件或内部行为变化的 SUBTASK/TASK；
- `L3`：架构、公共 API、持久化数据、安全边界、依赖策略或兼容性承诺变化。

以下情况会触发 Impact Review，并通常需要 ADR：

- 修改公共 API、CLI、文件格式、schema、数据库或协议；
- 改变架构边界、关键依赖、部署或恢复行为；
- 影响安全、隐私、性能预算或向后兼容性；
- 与已接受 ADR 或稳定约束冲突；
- 需要迁移或难以回滚。

### 机械校验

#### 状态与引用

```text
python <skill-directory>/scripts/validate_state.py <project-root>
```

检查包括：

- 必需项目记忆文件是否存在；
- STATE 结构、状态值和上下文大小；
- Active Task 是否为栈顶任务；
- Task Stack 引用是否存在、类型是否匹配；
- STATE 与活跃任务状态是否一致；
- DONE 任务是否仍有未完成 DoD；
- ADR 引用是否有效。

#### Git 与 Task 双向追溯

```text
python <skill-directory>/scripts/check_traceability.py <project-root>
```

检查包括：

- 治理基线后的产品提交是否包含 Task ID；
- commit 中的 Task ID 是否存在；
- 任务记录是否反向引用对应 commit；
- 任务记录中的 commit 是否存在并引用所属 Task；
- 存在产品工作区修改时是否有有效 Active Task。

建议提交标题包含任务 ID，例如：

```text
TASK-042: implement unload lifecycle
```

日常校验默认只扫描热状态和治理基线后的提交。只有进行冷历史审计时才使用：

```text
python <skill-directory>/scripts/validate_state.py <project-root> --full
python <skill-directory>/scripts/check_traceability.py <project-root> --full
```

### Skill 目录

```text
ASTTRA-AI-Development-Governance/
├─ SKILL.md
├─ README.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ lifecycle.md
│  ├─ task-model.md
│  ├─ change-policy.md
│  ├─ checkpoint-policy.md
│  └─ adr-policy.md
├─ templates/
│  ├─ AGENTS.template.md
│  ├─ PROJECT.template.md
│  ├─ STATE.template.md
│  ├─ TASK.template.md
│  └─ ADR.template.md
└─ scripts/
   ├─ init_project.py
   ├─ validate_state.py
   └─ check_traceability.py
```

### 行为边界

启用本 Skill 不代表授权 agent：

- 自动提交或推送代码；
- 覆盖已有治理文件；
- 重写 Git 历史；
- 发布、部署或执行破坏性清理；
- 为局部修复进行未经请求的广泛重构。

这些操作仍然需要正常的用户授权。

### 当前版本

当前为 v0.1，重点是建立最小但完整的项目连续性闭环：项目记忆、Task Stack、Goal Guard、Checkpoint、ADR、Impact Review、Git 追溯与机械校验。

欢迎通过 GitHub Issues 提交实际长期项目中的使用反馈。
