---
name: ai-development-governance
description: Establish and operate repository-centered governance for long-lived software projects, including resumable task state, change control, architectural decisions, checkpoints, and Git traceability. Use for requests such as “AI开发项目构架建立”, “AI开发项目架构建立”, “建立AI开发项目治理框架”, “初始化长期开发项目”, or “接管/继续长期维护项目”, and when resuming, checkpointing, closing, or auditing governed work. Do not use for disposable experiments or one-off edits in repositories that have not adopted the framework.
---

# AI Development Governance

Treat the repository as the durable system of record. Conversation context is disposable working memory. Preserve engineering semantics—goals, constraints, decisions, state, verification, rejected approaches, and next actions—not a transcript of agent activity.

## Determine the mode

- **INIT:** The user asks to adopt the framework. Read [references/lifecycle.md](references/lifecycle.md), inspect the repository, then run `scripts/init_project.py`. Never overwrite existing governance files without explicit authorization; merge project-specific facts manually when files already exist.
- **RESUME:** A governed repository already exists or a new thread/agent is taking over. Read `AGENTS.md`, `.ai/PROJECT.md`, `.ai/STATE.md`, the active task stack, relevant ADRs, and Git state. Read [references/lifecycle.md](references/lifecycle.md) and [references/task-model.md](references/task-model.md). Reconcile records with repository evidence before editing, then give a concise takeover report.
- **WORK:** Before a meaningful change, apply Goal Guard and classify it as EPIC, TASK, SUBTASK, PATCH, or INTERRUPT. Read [references/task-model.md](references/task-model.md) and [references/change-policy.md](references/change-policy.md). Perform an Impact Review when its triggers apply.
- **CHECKPOINT:** After a meaningful recoverable stage or before interruption, compaction, or handoff, read [references/checkpoint-policy.md](references/checkpoint-policy.md). Update the owning task and then the lightweight state pointer; record verification evidence.
- **CLOSE:** Verify every Definition of Done item, reconcile Git and task references, and update task status before removing it from the active stack. Read the checkpoint policy and [references/adr-policy.md](references/adr-policy.md).

## Non-negotiable invariants

1. Evidence precedence is: current code and Git; current state and active task records; accepted project documents and ADRs; conversation history.
2. A local request does not replace the parent objective. Represent related work as a SUBTASK or PATCH and unrelated temporary work as an INTERRUPT. Restore the suspended frame after it closes.
3. Every meaningful code change has one owning task. PATCH work may live as a checkpoint inside its parent unless it needs independent review or traceability.
4. Do not mark work done because one symptom is fixed. Close only when the task Definition of Done and required verification are complete.
5. Do not silently change architecture, public contracts, persistent data, compatibility commitments, security boundaries, or major dependencies. Use an ADR when [references/adr-policy.md](references/adr-policy.md) requires one.
6. Keep `.ai/STATE.md` short. It is a current pointer, not a history log. Put durable history in task records, decisions in ADRs, and stable facts in `.ai/PROJECT.md`.
7. Never auto-commit, rewrite history, publish, or overwrite an existing governance file merely because this skill is active.

## Bound the context

Use a three-tier working set:

- **Hot:** STATE and the active task stack. Read on every RESUME and keep bounded.
- **Warm:** PROJECT, task-relevant accepted ADRs, relevant diff, and task-linked commits. Read as needed.
- **Cold:** completed tasks, unrelated ADRs, and old Git history. Do not load unless linked by active work or needed to resolve a conflict.

Do not scan all tasks or decisions on routine RESUME. Before a new window or agent takeover, make a handoff checkpoint in the active task and STATE; do not create a duplicate handoff log.

## Mechanical checks

```text
python scripts/validate_state.py <project-root>
python scripts/check_traceability.py <project-root>
```

Run both at CHECKPOINT and CLOSE when Git is available. Their default checks are limited to hot state and the configured Git range. Use `--full` only for an explicit cold-history audit. A nonzero exit code is a failed governance check, not permission to repair unrelated files. Explain discrepancies and make only scoped corrections.

## Project memory contract

INIT creates:

```text
AGENTS.md
.ai/
  PROJECT.md
  STATE.md
  CHANGE_POLICY.md
  TRACEABILITY_BASELINE
  tasks/
  decisions/
```

Use `templates/` only for project instances. Do not store project-specific state inside this skill.
