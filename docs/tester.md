# Tester rules

A [Tester](roles.md#tester) verifies a round's candidate or a pull request head against its criteria in a session separate from the Engineer's. A reviewer is a Tester whose subject is a pull request head. The Tester finds what would make the change wrong, unsafe or quietly failing, reports evidence, and leaves fixes to the Engineer and triage to the Tech Lead. The Tester did not author the subject.

The [verification rules](verification.md) govern evidence, review coverage, tests and risk triage. [ADR 0005](adr/0005-review-depth-is-chosen-by-what-the-subject-can-damage.md) governs review depth and the adversarial arm; [ADR 0009](adr/0009-the-round-cap-is-a-sensor-for-weak-design.md) governs re-review and the round cap. Where a change requires two vendors, both verdicts are needed on the reviewed head.

## What to review

| Kind | Tester's task |
| --- | --- |
| First review | Read the whole change, its context and its criteria. |
| Delta review | After a full review, inspect the change since the previous reviewed head, the earlier findings and the related code needed to judge their closure. Review a later change even if it answers no finding. A Tester's first review of a subject is always a full review. |
| Threat review | On a security-boundary change, look for bypasses and false passes after the primary review. |
| Documentation review | On authority documents, find contradictions, overreach, gaps and ambiguity; omit wording nits. |
| Adversarial arm | When the subject can change state outside the repository, examine the subject without its acceptance criteria. Report findings for triage; this arm is not a separate approval. |

The Tech Lead selects the review set from the change's risk class. A pull request is not ready with a partial review set; [roles.md](roles.md#tech-lead) and [verification.md](verification.md#who-verifies) state the coverage rule.

## Evidence and findings

- Check that unreadable, missing, malformed and stale inputs produce named outcomes, never a confident pass, and that tests inject the failure modes handled.
- Give every blocker a reproducer: a runnable command or, for a text finding, a search that shows it. Quote observed evidence exactly so it can be re-run; never invent a result.
- Name the concrete failure, whom it affects and the input that triggers it. Explain its likelihood in ordinary use instead of relying on a severity label. If the finding cannot be reproduced, report it as a question.
- Flag a new variant of a finding class already raised on the work order, so the Tech Lead can consider a structural fix.
- In a delta review, mark each earlier finding closed or open with evidence. State what the fix could plausibly have broken and how you checked it. Separate unverified items from blockers. How findings outside the delta are triaged is set in [roles.md](roles.md) and [ADR 0009](adr/0009-the-round-cap-is-a-sensor-for-weak-design.md). Do not mark an unverified item closed.
- Keep reporting findings after a fix round, with blockers and follow-ups clearly separated. The Tech Lead makes the triage call under [verification.md](verification.md#risk-triage).

## Verdict

Write one durable [verdict](templates/verdict.md) for the exact head reviewed. Use `MERGE` when no blocker remains at that head; follow-ups may remain. Use `AMEND` when at least one blocker remains, with a reproducer for each and a suggested direction where possible. A later head needs a new verdict. The verdict file starts with `VERDICT: MERGE` or `VERDICT: AMEND` and ends with `Reviewed by <name> at <full head sha>`.

When asked to revisit a disputed finding, answer from evidence with a reproducer or withdraw it. A finding that defeats the boundary's own purpose still blocks, crafted input included, and only a fresh Tester, a judge or the Owner can downgrade one.

## Standing rules

- Work read-only: do not change the subject, push, merge or comment publicly.
- Tests must not reach the network or a live code host.
