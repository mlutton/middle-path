# Tester runbook

A short checklist for a [Tester](roles.md#tester) in one verify round, in the order a round goes. It is not the rules: the [Tester rules](tester.md) and the [verification rules](verification.md) say what a Tester must do and report, and they cover more than this list.

## Before the round

1. Know the subject and the exact head to verify. Except in an adversarial review, which gets no criteria (see [tester.md](tester.md)), know the criteria.
2. Confirm you did not author the subject and that your session is separate from the Engineer's.
3. The kinds of review are first, delta, threat, documentation and adversarial (see [tester.md](tester.md)); the Tech Lead selects the review set. A first review of a subject is always a full review.
4. Work read-only. Do not change the subject, push, merge or comment publicly.

## During the round

1. Read the whole change and its context for a first review. For a delta review, read the change since the previous reviewed head, the earlier findings and the related code needed to judge their closure.
2. Except in an adversarial review, which gets no criteria (see [tester.md](tester.md)), check each criterion against evidence you can re-run. Check that unreadable, missing, malformed and stale inputs give named outcomes, and that tests inject the failures the code handles.
3. For every possible blocker, write a reproducer: a runnable command, or for a text finding a search that shows it. Quote the observed result exactly. If you cannot reproduce it, report it as a question.
4. State each finding as what breaks, for whom and under what input.
5. In a delta review, mark each earlier finding closed or open with evidence, and say what the fix could have broken and how you checked.
6. Keep unverified items apart from blockers, and never mark an unverified item closed.

## Closing the round

1. Write one [verdict](templates/verdict.md) for the exact head you read: `MERGE` when no blocker remains, `AMEND` when at least one does.
2. Put the `VERDICT:` line first and the `Reviewed by <name> at <full head sha>` line last.
3. If you are asked to revisit a disputed finding, answer with a reproducer or withdraw it.
4. A later head needs a new verdict.
