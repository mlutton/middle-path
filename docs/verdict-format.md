# The verdict format

A verdict is a reviewer's judgment on one change, at one commit. It is the
evidence the readiness decision reads. This page describes the typed verdict that
the walking skeleton's merge layer has had since the v0.1.2-merge-gate tag.
[How work is verified](verification.md) says who reviews and why; this page
says what a verdict contains and how the readiness decision reads it.

## What a verdict carries

A verdict is a frozen value with four fields. All four are required.

| Field | What it holds |
| --- | --- |
| `decision` | One of `MERGE`, `AMEND`, `FIX_FIRST` or `BLOCK`. |
| `head` | The commit the verdict was given at: exactly 40 lowercase hexadecimal characters. |
| `reviewer` | Who gave the verdict: a name that is not empty after trimming whitespace. |
| `role` | The slot the reviewer fills for this change: `primary` or `second`. |

A value that does not fit is refused when the verdict is built. An uppercase or
shortened commit is refused, and so is a blank reviewer or a role that is not
one of the two.

## The rule and the readiness decision

A rule names the roles a change needs, as a non-empty tuple of roles. The
readiness decision takes the verdicts, the commit the change points at now, and
the rule, and returns either ready or not ready with one or more reasons from
a closed list:

| Reason | When it appears |
| --- | --- |
| `no-verdict-at-head` | There are no verdicts at all. |
| `stale-only` | There are verdicts, but none at the current commit. |
| `duplicate-reviewer` | The same reviewer, compared without regard to case, appears twice at the current commit. |
| `non-merge-at-head` | Some verdict at the current commit is not `MERGE`. |
| `missing-role:primary`, `missing-role:second` | A required role slot is not filled by a `MERGE` verdict at the current commit. A rule that requires a role twice needs two distinct reviewers in it. |

The checks run in that order and stop at the first that applies, except that
both missing-role reasons can appear together. A change is ready only when
every verdict at the current commit is `MERGE`, no reviewer appears twice, and
every required role is filled. A ready change is not merged automatically; the
Owner merges.

## The rules

- **A verdict counts only for the commit it names.** A verdict at an older
  commit does not count, and an objection at an older commit does not block.
- **A valid verdict alone does not make a change ready; the readiness decision
  also checks that every role the rule requires is filled.**
- **Approvals fill a role; one reviewer cannot fill two.** The caller says which
  role a reviewer holds; the core has no built-in list of reviewers.
- **Anything malformed is refused, not guessed.** Building a verdict with a
  bad value raises an error, and so does calling the readiness decision with a
  bad commit, rule or verdict collection. These are errors, not readiness reasons.

The tests that pin this behaviour are in
`components/middle-path/merge/tests/test_readiness.py`. The verdict type itself
is defined in `components/middle-path/ports/`.

## What this page does not cover

The verdict in the skeleton's earlier end-to-end slice is a simpler value and
the older merge result is now called a merge decision. What the merge gate
outside this repository does with verdicts is not described here. See
[what's next](whats-next.md).
