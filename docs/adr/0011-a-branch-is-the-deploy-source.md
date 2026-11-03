# A branch is the deploy source

**Status**: decided in October 2026.

## Decision

A branch is the deploy source. Each pull request (PR) is a deployable unit. Rollback returns to the branch's previous version.

## Context

Pinned releases and install cards currently govern deployments. A branch can record deployed code and its previous version. Migration remains separate work.

## Rules

1. `live` is the branch recording what is deployed. Each move takes it, in order, to one PR's merge commit on `main`.
2. Merging a PR does not deploy it. Moving the branch is a deliberate, separate step for the Owner or a named, Owner-approved route; agents cannot move it. The first route is the Owner moving `live` by hand.
3. Deployed code runs from a read-only checkout pinned to a deployment-branch commit, never a working checkout. Verify that it is clean, at the expected commit, and passes the unit's own check.
4. Rollback moves the branch to its previous commit. To remove an older PR while keeping later PRs, revert it on `main` and deploy forward.
5. A PR needing a configuration or state change names that change and its own undo. Moving the branch back does not undo state.
6. Files outside the repository's deploy path, including root-owned hooks and managed settings, remain explicit Owner steps named in the PR. Agents' worker tools and guard and hook code use the same `live` branch; guard and hook code needs a separate Owner step.
7. A running session keeps the commit on which it launched. It moves to a new commit only by relaunch.

## Consequences

- Rollback is linear: going back one version undoes the latest PR.
- A deploy is a merge commit. It may combine PRs that were not tested together, so that commit needs a green suite before the deployment branch moves.
- Guard and hook code becomes live through a git move. That move must be protected and watched by the integrity watch.
- Existing pinned release folders and install cards keep working. Migration is separate follow-up work; acceptance of this decision changes nothing in operation.

## Rejected options

- Per-unit registry: unnecessary complexity.
- Staging directories: unnecessary deployment locations.
- One unit per repository, file, or card: the wrong boundary for a PR.
