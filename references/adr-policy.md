# ADR Policy

ADRs record consequential decisions and rationale. They are not design diaries and are not required for ordinary implementation choices.

## Create or supersede an ADR when

- system boundaries, architecture, or a cross-cutting pattern changes;
- a public contract, persistent schema, protocol, or compatibility commitment changes;
- a major dependency/platform is adopted, replaced, or removed;
- a security, privacy, reliability, deployment, or irreversible migration decision is made;
- an accepted ADR must be contradicted;
- viable approaches have materially different long-term tradeoffs.

Do not create an ADR for local refactoring, formatting, straightforward bug fixes, or choices already governed by an accepted decision.

## Lifecycle

Statuses are `PROPOSED`, `ACCEPTED`, `REJECTED`, `SUPERSEDED`, and `DEPRECATED`.

- A PROPOSED ADR may guide exploration but is not an accepted constraint.
- Record the approving authority or project rule before marking ACCEPTED.
- Never edit an accepted ADR to hide history. Create a new ADR and set supersession links.
- Link every ADR to at least one task and every affected task back to the ADR.

## Required content

Context, decision drivers, considered options, decision, consequences, compatibility/migration/rollback effects, related tasks, and supersession links. Keep rejected options concise but sufficient to avoid repeating settled exploration.
