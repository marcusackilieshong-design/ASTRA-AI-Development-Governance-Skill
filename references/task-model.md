# Task Model

## Types

| Type | Purpose | Record rule |
|---|---|---|
| EPIC | Multi-task outcome or sustained direction | Separate task record |
| TASK | Independently deliverable change with its own Definition of Done | Separate task record |
| SUBTASK | Bounded step required by a parent TASK | Separate record when it spans checkpoints, agents, or commits; otherwise a parent checklist |
| PATCH | Small, low-risk correction inside an existing objective | Parent checkpoint by default; separate record only when independent traceability is useful |
| INTERRUPT | Unrelated temporary work that suspends but does not replace active work | Separate record if it changes the repository; pop after completion |

`ARCHITECTURAL CHANGE` is not a task type. It is a change characteristic that normally requires a TASK plus an ADR.

## Stack rules

The main lineage is `EPIC → TASK → SUBTASK`. At most one frame of each main-line type is active. PATCH and INTERRUPT are temporary top frames and identify their parent or suspended frame.

- Never replace an active task silently.
- A related small request becomes a PATCH or SUBTASK under the active TASK.
- An unrelated repository request becomes an INTERRUPT. Preserve and restore the prior stack.
- A question or analysis-only request does not alter the stack.
- Creating a new TASK that changes priority requires explicit user direction or a documented project rule.
- Parent completion requires required child work to be done, cancelled with a reason, or explicitly moved out of scope.

## Statuses

`PLANNED`, `IN_PROGRESS`, `BLOCKED`, `VERIFYING`, `DONE`, `CANCELLED`.

- Use `BLOCKED` with a concrete blocker and next unblocking action.
- Use `VERIFYING` when implementation exists but Definition of Done evidence is incomplete.
- `DONE` requires every required Definition of Done box checked and final verification recorded.
- `CANCELLED` requires a reason and does not imply success.

## Goal Guard

Before a meaningful code or governance change, answer from repository evidence:

1. Which task owns this change?
2. Which parent objective does it advance?
3. Is it a continuation, child, patch, interruption, or replacement?
4. Which constraints or accepted ADRs might it affect?
5. What observable result and verification will prove success?

If ownership or goal compatibility cannot be established safely, stop before implementation and ask for direction.

## Definition of Done

Write outcome-based, checkable conditions before substantial implementation. Include behavior, tests, compatibility/migration, documentation, and governance records only when relevant. Do not use vague items such as “works.” A task cannot close with unchecked required items.
