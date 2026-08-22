# Lifecycle

The lifecycle is a state-reconstruction protocol, not a ceremony. Skip no evidence needed to recover safely, but do not generate records for trivial conversation.

## INIT

Entry: the user adopts the framework for a new or existing repository.

1. Inspect repository layout, Git status, build/test configuration, documentation, and existing agent instructions.
2. Identify stable purpose, architecture, commands, constraints, sensitive areas, and the initial objective. Mark unknown facts as `UNKNOWN`; do not invent them.
3. Run `init_project.py`. If target files already exist, stop and merge deliberately rather than forcing an overwrite.
4. Replace remaining template markers and tailor `AGENTS.md` and `.ai/PROJECT.md` to the actual repository.
5. Run `validate_state.py`. If Git exists, run `check_traceability.py`.

Exit: the initial task exists, STATE points to it, Next Action is executable, and validation passes.

## RESUME

Entry: a new window/thread/agent starts, context was compacted, the user says continue, or work resumes after interruption.

Read the hot working set first:

1. Applicable `AGENTS.md` files.
2. `.ai/STATE.md`.
3. Every task named in the active stack.

Then read only the warm evidence relevant to that work:

4. `.ai/PROJECT.md` and `.ai/CHANGE_POLICY.md`.
5. Accepted ADRs referenced by active tasks.
6. Git branch, status, relevant diff, and recent task-linked commits.
7. Code and verification evidence named by the current checkpoint.

Do not preload completed tasks, unrelated ADRs, or broad history. Reconcile conflicts by evidence precedence and report material mismatches. Before editing, give a concise takeover report: current objective, completed and unfinished work, constraints, Git/working-tree state, verification, exact next action, and any record/evidence conflict.

Exit: current objective, unfinished work, constraints, working-tree state, verification status, and next action are known.

Suggested handoff prompts:

```text
Old window: Use $ai-development-governance in CHECKPOINT mode. Create a handoff checkpoint, reconcile it with Git, and stop before the next implementation step.

New window: Use $ai-development-governance in RESUME mode. Reconstruct the active state from the repository, verify it against Git, and give me a takeover report before editing.
```

## WORK

Entry: state has been reconstructed and an owning task is known.

1. Apply Goal Guard: name the owning task, parent objective, intended outcome, and constraints at risk.
2. Classify the change using the task model.
3. Push a task frame only when needed. A question that requires no repository change does not change the stack.
4. Run Impact Review when triggered; create or update an ADR when required.
5. Implement the minimum scoped change and verify proportionally.

Exit: reach a checkpoint, blocker, interruption, or completed Definition of Done.

## CHECKPOINT

Entry: a meaningful stage is complete, work will pause, uncertainty/blockage changes, or handoff/compaction is likely.

Update the task first, then STATE. Record outcomes and evidence rather than chronological narration. Run mechanical checks. A checkpoint need not be a Git commit.

For a deliberate new-window handoff, the old agent must leave: an accurate active stack, a one-paragraph last-checkpoint outcome, verification results, current Git state in the task checkpoint, and one executable Next Action. The new agent uses RESUME; no separate `HANDOFF.md` is needed.

Exit: another agent can identify what was achieved, what remains, what evidence exists, and the next action.

## CLOSE

Entry: implementation appears complete.

1. Verify every Definition of Done item and required Impact Review action.
2. Confirm required ADRs exist and their status matches reality.
3. Reconcile task-to-commit and commit-to-task references.
4. Record final verification and change the task to `DONE`.
5. Pop PATCH/INTERRUPT/SUBTASK frames and restore the suspended parent. If no work remains, set STATE to `IDLE` and Active Task to `NONE`.
6. Run both validators.

Exit: records match repository reality and the next state is explicit.
