# ASTTRA AI Development Governance

面向长期维护软件项目的、以仓库为中心的 AI 开发治理与连续性 Skill。

它帮助 Codex 及其他 coding agent 在聊天上下文压缩、任务中断、新窗口切换或新 agent 接管后，仍能从仓库中可靠地重建项目状态，同时避免为了记录而制造不断膨胀的上下文。

> Conversation is disposable. Repository is persistent.

Skill 的正式调用名是：`$ai-development-governance`。

## 它解决什么问题

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

## 核心原则

### Repository as System of Record

发生冲突时，证据优先级为：

1. 当前代码与 Git；
2. `.ai/STATE.md` 与活跃任务记录；
3. 已接受的项目文档与 ADR；
4. 历史聊天上下文。

项目知识保存在项目仓库中，Skill 只定义如何记录、恢复和校验，不保存任何具体项目的状态。

### 有边界的上下文

恢复项目时使用三层工作集：

| 层级 | 内容 | 读取规则 |
|---|---|---|
| Hot | `STATE.md` 与活跃 Task Stack | 每次 RESUME 必读，严格保持短小 |
| Warm | `PROJECT.md`、相关 ADR、相关 diff 与任务提交 | 根据当前任务按需读取 |
| Cold | 已完成任务、无关 ADR、旧 Git 历史 | 默认不加载，只在引用或冲突调查时读取 |

`STATE.md` 被限制在 120 行、12 KiB 以内。常规校验只扫描热状态和配置的 Git 范围；只有显式使用 `--full` 才检查冷历史。

### 局部修改不替换主任务

Task Stack 支持：

- `EPIC`：跨多个任务的长期目标；
- `TASK`：可独立交付、具有 Definition of Done 的任务；
- `SUBTASK`：当前任务的一个可恢复步骤；
- `PATCH`：当前目标内的小型低风险修正；
- `INTERRUPT`：与当前目标无关的临时插入工作。

主链是 `EPIC → TASK → SUBTASK`。PATCH 和 INTERRUPT 是临时栈帧，完成后必须恢复被挂起的主任务。

### Goal Guard 与 Definition of Done

进行有意义的修改前，agent 必须确认：

1. 哪个任务拥有这次变更；
2. 它推进哪个父目标；
3. 它是继续、子任务、补丁、中断还是目标替换；
4. 它可能影响哪些约束或 ADR；
5. 什么可观察结果和验证能够证明完成。

任务不能因为某个局部症状消失就关闭。所有必需的 Definition of Done 条目和验证证据完成后，才能标记为 `DONE`。

## 工作生命周期

| 模式 | 用途 | 主要输出 |
|---|---|---|
| INIT | 首次建立项目治理框架 | `AGENTS.md`、`.ai/`、初始任务与状态 |
| RESUME | 新窗口、新 agent、上下文压缩后接管 | 经 Git 核对的接管报告 |
| WORK | 日常开发 | 受 Goal Guard 和变更分级约束的实现 |
| CHECKPOINT | 逻辑阶段、暂停、阻塞或交接 | 可恢复的任务检查点和短 STATE |
| CLOSE | 任务收尾 | DoD、验证、ADR 与 Git 追溯闭环 |

## 初始化后生成的项目结构

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

## 安装

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
git clone https://github.com/marcusackilieshong-design/ASTTRA-AI-Development-Governance.git "$HOME\.agents\skills\ai-development-governance"
```

### macOS / Linux

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/marcusackilieshong-design/ASTTRA-AI-Development-Governance.git "$HOME/.agents/skills/ai-development-governance"
```

Codex 通常会自动发现 Skill；如果没有出现，请重启 Codex。

## 如何调用

### 显式调用

```text
$ai-development-governance
```

### 中文自然语言触发

可以直接使用：

```text
AI开发项目构架建立：为当前项目初始化长期开发治理框架。
```

也支持类似表达：

- AI开发项目架构建立；
- 建立AI开发项目治理框架；
- 初始化长期开发项目；
- 接管或继续长期维护项目。

## 常用工作流

### 1. 初始化一个新项目

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

### 2. 日常开发

```text
使用 $ai-development-governance 继续当前任务。
先应用 Goal Guard，确认变更所属任务和 Definition of Done，再开始修改。
```

临时小修改会作为 PATCH 或 SUBTASK；无关的临时工作会作为 INTERRUPT。它们不会静默替换主任务。

### 3. 创建 Checkpoint

```text
使用 $ai-development-governance 进入 CHECKPOINT 模式。
核对代码和 Git，更新活跃任务与 STATE，记录验证结果和一个明确的 Next Action。
```

Checkpoint 表示可恢复的工程边界，不要求 Git commit，也不应该记录文件读取、普通命令或聊天流水。

### 4. 新旧窗口交接

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

### 5. 关闭任务

```text
使用 $ai-development-governance 进入 CLOSE 模式。
逐项验证 Definition of Done，核对 ADR 和 Git 双向追溯，通过校验后再关闭任务。
```

## 变更分级与 ADR

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

## 机械校验

### 状态与引用

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

### Git 与 Task 双向追溯

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

## Skill 目录

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

## 行为边界

启用本 Skill 不代表授权 agent：

- 自动提交或推送代码；
- 覆盖已有治理文件；
- 重写 Git 历史；
- 发布、部署或执行破坏性清理；
- 为局部修复进行未经请求的广泛重构。

这些操作仍然需要正常的用户授权。

## 当前版本

当前为 v0.1，重点是建立最小但完整的项目连续性闭环：项目记忆、Task Stack、Goal Guard、Checkpoint、ADR、Impact Review、Git 追溯与机械校验。

欢迎通过 GitHub Issues 提交实际长期项目中的使用反馈。
