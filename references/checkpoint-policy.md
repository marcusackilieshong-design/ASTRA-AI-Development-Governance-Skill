# Checkpoint Policy

A checkpoint captures a recoverable engineering boundary. It is not a diary entry and does not require a Git commit.

## Trigger a checkpoint when

- a logical implementation stage and its verification complete;
- the next step changes subsystem, risk, or approach;
- work becomes blocked or an assumption is invalidated;
- an INTERRUPT is pushed or popped;
- context compaction, a new window/thread, agent handoff, or pause is likely;
- a task enters `VERIFYING`, `DONE`, or `CANCELLED`.

Avoid checkpoints for individual file reads, routine commands, or narration without durable state change.

## Required checkpoint content

In the owning task append a concise entry containing outcome, key affected components, verification and result, durable decisions/rejected approaches/new risks, exact next action or blocker, and commit/PR reference when one exists. Then update STATE with only the active stack, status, current focus, last checkpoint summary, next action, blockers, and latest verification.

## Context budget

- STATE is hot state: keep it under 120 lines and 12 KiB.
- Keep only recovery-critical facts in the active task. Condense superseded implementation notes at major milestones into an outcome summary.
- At CLOSE, retain final outcome, important checkpoints, rejected approaches that prevent repeated mistakes, verification, ADR links, and Git links; remove routine narration.
- Completed tasks and unrelated decisions are cold history. Do not read them during routine RESUME.
- If task history becomes unwieldy, archive completed task files under `.ai/tasks/archive/<year>/`; preserve IDs and links. Validators search recursively.

## Handoff

Before a handoff, reconcile STATE and the active task with Git status and diff. Record the handoff as a normal checkpoint. The receiving agent performs RESUME and verifies it against repository evidence. Do not maintain a parallel handoff document.

At CLOSE, check every Definition of Done item, record final Git references, and run both validators. If verification cannot run, keep the task in `VERIFYING` or `BLOCKED` and record why.
