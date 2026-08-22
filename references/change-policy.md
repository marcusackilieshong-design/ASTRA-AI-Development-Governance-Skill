# Change Policy

## Principles

- Make the smallest change that satisfies the owning task and its Definition of Done.
- Do not refactor adjacent code, change public behavior, or broaden scope without a task-level reason.
- Preserve user changes and existing local modifications. Do not assume an unclean working tree belongs to the current agent.
- Repository questions do not mutate state unless they change the active objective or create work.
- Never redefine the project goal, discard a suspended task, or overwrite an accepted decision silently.

## Change levels

| Level | Typical scope | Required governance |
|---|---|---|
| L0 | Read-only analysis or explanation | No task-state mutation |
| L1 | PATCH; local, reversible, no contract change | Owning task and proportional verification |
| L2 | SUBTASK/TASK; multiple files or internal behavior | Task record, Definition of Done, checkpoint evidence |
| L3 | Architecture, public API, persistent data, security boundary, dependency strategy, or compatibility commitment | TASK, Impact Review, ADR, migration/rollback consideration |

File count is a signal, not a decision by itself. A one-line public API break may be L3; a mechanical internal rename may be L2.

## Impact Review triggers

Perform an Impact Review when any apply:

- more than three core modules or multiple architectural layers change;
- a public API, CLI, format, schema, database, protocol, or compatibility promise changes;
- dependencies, build/deploy behavior, security/privacy boundaries, performance budgets, or recovery behavior change;
- implementation contradicts an accepted ADR or stable constraint;
- rollback is difficult or migration is required.

Record applicable impacts in the owning TASK: architecture, API/UX, data/migration, backward compatibility, security/privacy, performance, dependencies/operations, tests, documentation, rollback, and parent objective. Write `N/A` with a short reason where irrelevant.

## Authorization boundaries

The framework does not authorize committing, pushing, publishing, deployment, destructive cleanup, history rewriting, or overwriting existing governance records. Obtain the authorization those actions normally require.
