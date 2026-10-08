# How work is verified

[ADR 0001](adr/0001-the-factorys-objects-and-roles.md) names the roles, [lifecycle](lifecycle.md) shows where verification sits in a piece of work, and [ADR 0005](adr/0005-review-depth-is-chosen-by-what-the-subject-can-damage.md) explains how deep a review goes. This page collects the rules verification follows. They are the rules the factory holds itself to, and most are practices followed by hand. The [glossary](glossary.md) marks what is design and not yet built.

## No evidence, no claim

A step is crossed only when the file behind it exists. An Engineer's handback names evidence for every "done", "passing" or "fixed": test output, a count, a commit, or a file and line. A claim with no evidence is written "unverified". The Tech Lead re-runs the evidence, so an invented result shows. A handback that claims without evidence goes back before any verification starts.

## Who verifies

A Tester verifies in a separate session from the Engineer's, and reports one verdict per head: merge or amend. The verdict is bound to the exact head it read, so a later change needs a new verdict.

Review is normally by one reviewer from each of two vendors, so a blind spot in one family of models is less likely to pass both. When that is not possible, the review runs on one vendor and the record says so. A change at a security boundary gets a threat review as well, which looks for bypasses and false passes only. A change that can alter state outside the repository gets an adversarial arm, which is given no criteria (ADR 0005). Authority documents get a documentation review. A pull request is never reported ready on a partial set of verdicts, and a finding never passes for lack of reviewer capacity: with no headroom, it stays open.

## Tests

Tests use fakes and do not reach the network or a live code host. The project's full suite runs on the candidate before a verdict is applied, because a verdict should rest on the whole suite and not a chosen part of it. A fix starts with a failing test that reproduces the finding. An unreadable, missing, malformed or stale input produces a named outcome and never a quiet pass, and a test injects each failure mode the code handles.

## Reviewed changes to live settings

A change to the machine or to settings reaches the Owner as a script to run, called a card, after review. A card checks the target, applies the change and, where possible, can be undone. The Owner runs it in a console where the Foreman can read each step's output.

## Guards, by purpose

The factory uses a few guards, and this page describes them by what they are for and not how they work: a scan before anything is published, a check on commands that agents try to run, a start check on usage limits, and a check that fails loudly when its input is missing or stale. A guard earns its place from a failure, and the factory prefers moving a capability out of reach to adding one more rule that judges every action.

## Risk triage

Every finding gets four questions: can we undo it, how big can it get, who pays and do they have recourse, and would a named monitor catch it. A finding blocks a merge only if it is irreversible or unbounded. A bounded finding that a named monitor would catch becomes a follow-up with that monitor. A theoretical one is recorded as a known limit with a follow-up. A monitor is named only where its coverage has been shown.

Code-quality findings (weak tests, unclear code) are always fixed, whatever their risk.

A blocking finding names a concrete failure: what breaks, for whom, and under what input. A finding without one is a question, and a question gets answered before the pull request is reported ready.

From the third review pass on a change at a security boundary, a finding blocks only if it is a correctness or safety failure with a scenario from ordinary use, and it has been reproduced. The exception is a finding that defeats the boundary's own purpose, such as a private value in the output of a redaction change, an action that gets past a check to do what it should refuse, or a leaked secret. Those still block, crafted input included, and only a fresh Tester, a judge or the Owner can downgrade one.

## What verification does not do

Review does not prove correctness. A structural check cannot prove that a claim is true, only that evidence for it exists. These rules lower the chance that a defect passes. They do not remove it.
