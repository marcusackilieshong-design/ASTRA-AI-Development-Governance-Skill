# Agent Instructions

This repository uses repository-centered AI development governance.

Before modifying the repository:

1. Read `.ai/STATE.md` and every task in its active stack.
2. Read `.ai/PROJECT.md`, `.ai/CHANGE_POLICY.md`, and only the ADRs relevant to active work.
3. Inspect Git branch, status, relevant diff, and task-linked commits.
4. Reconcile records with repository evidence. Code and Git outrank conversation context.
5. Apply Goal Guard and identify one owning task before meaningful changes.

During work:

- A local request does not replace the active objective. Use SUBTASK/PATCH for related work and INTERRUPT for unrelated temporary work, then restore the prior stack.
- Keep changes scoped. Do not perform adjacent refactors or silently change documented constraints.
- Trigger Impact Review and an ADR when `.ai/CHANGE_POLICY.md` requires them.
- After meaningful stages, update the owning task first and `.ai/STATE.md` second.
- Do not mark a task DONE until its Definition of Done and verification are complete.

Before pausing, context compaction, a new window, handoff, or closure:

- Reconcile task/state records with Git and verification evidence.
- Leave one exact Next Action and run the governance validators supplied by `ai-development-governance`.
- Keep STATE under 120 lines and 12 KiB. Do not load cold history on routine resume or store chat transcripts.

Project-specific commands and constraints are recorded in `.ai/PROJECT.md`.
