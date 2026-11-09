# The verdict format

A verdict is a reviewer's judgment on one change, at one commit. It is the
evidence the readiness decision reads. This page describes the typed verdict that
the walking skeleton's merge layer has had since the v0.1.2-merge-gate tag, and
what the v0.1.3-extra-roles tag added to it: provenance on the verdict and
optional extra roles in the readiness decision.
[How work is verified](verification.md) says who reviews and why; this page
says what a verdict contains and how the readiness decision reads it.

## What a verdict carries

A verdict is a frozen value with six fields. The first four are required; the
last two have defaults.

| Field | What it holds |
| --- | --- |
| `decision` | One of `MERGE`, `AMEND`, `FIX_FIRST` or `BLOCK`. |
| `head` | The commit the verdict was given at: exactly 40 lowercase hexadecimal characters. |
| `reviewer` | Who gave the verdict: a name that is not empty after trimming whitespace. |
| `role` | The slot the reviewer fills for this change: `primary` or `second`. |
| `provenance` | `direct` (the default) or `carried`. |
| `carried_from` | The commit a carried verdict is carried from. `None` by default. |

A value that does not fit is refused when the verdict is built. An uppercase or
shortened commit is refused, and so is a blank reviewer or a role that is not
one of the two.

A direct verdict has no `carried_from`. A carried verdict is valid only when its
role is `second`, its decision is `MERGE`, `carried_from` is itself a full
lowercase commit, and `carried_from` differs from `head`. Anything else is
refused when the verdict is built. The package can describe a carried verdict;
the review rule is still one verdict per head.

## The rule and the readiness decision

A rule names the roles a change needs, as a non-empty tuple of roles. The
readiness decision takes the verdicts, the commit the change points at now, and
the rule, and returns either ready or not ready with one or more reasons from
a closed list. It also takes an optional set of extra roles, described below.

| Reason | When it appears |
| --- | --- |
| `extra-roles-invalid` | The extra roles are marked invalid. |
| `no-verdict-at-head` | There are no verdicts at all. |
| `stale-only` | There are verdicts, but none at the current commit. |
| `duplicate-reviewer` | The same reviewer, compared without regard to case, appears twice at the current commit. |
| `non-merge-at-head` | Some verdict at the current commit is not `MERGE`. |
| `missing-role:primary`, `missing-role:second` | A required role slot is not filled by a `MERGE` verdict at the current commit. A rule that requires a role twice needs two distinct reviewers in it. |

The checks run in that order and stop at the first that applies, except that
both missing-role reasons can appear together. A change is ready only when
extra roles are not invalid, every verdict at the current commit is `MERGE`, no
reviewer appears twice, and every required role is filled. The readiness
decision only returns a result; it merges nothing.

## Extra roles

Extra roles are an optional input to the readiness decision, written as a state
(`resolved` or `invalid`), a tuple of roles, and an optional rule version.
Without them the decision behaves as before.

- **`invalid` refuses everything.** If the extra roles are invalid, the
  decision returns `extra-roles-invalid`, whatever the verdicts say. Invalid extra
  roles cannot carry roles.
- **`resolved` can only raise the requirement.** The roles needed are the
  rule's roles together with the extra roles, taking the larger count for each
  role. An extra role never lowers what the rule requires, and it does not add
  to a count the rule already asks for. The roles in one set of extra roles
  are unique.

## The rules

- **A verdict counts only for the commit it names.** A verdict at an older
  commit does not count, and an objection at an older commit does not block.
- **A valid verdict alone does not make a change ready; the readiness decision
  also checks that every role the rule requires is filled.**
- **Approvals fill a role; one reviewer cannot fill two.** The caller says which
  role a reviewer holds; the core has no built-in list of reviewers.
- **Anything malformed is refused, not guessed.** Building a verdict with a
  bad value raises an error, and so does calling the readiness decision with a
  bad commit, rule, verdict collection or extra roles. These are errors, not
  readiness reasons.

`components/middle-path/merge/tests/test_readiness.py` tests the verdict and the
readiness decision, including extra roles. The verdict type itself is defined in `components/middle-path/ports/`.

## What this page does not cover

What the merge gate outside this repository does with
verdicts is not described here. See [what's next](whats-next.md).
