# How a piece of work moves

This page follows one piece of work from request to merge. It uses the
names from [ADR 0001](adr/0001-the-factorys-objects-and-roles.md): the
Owner, the Tech Lead, the Engineer, the Tester, and the work request, work
order and round.

The rule that runs through all of it:

> A step is crossed only when the file behind it exists.

A "done" with no file behind it is a claim, not a fact. So is a verdict with
no file behind it. Testers and the Owner read artifacts, not conversation.
The record outlives the agent that produced it, and no agent is trusted
because of what it said earlier.

## What a piece of work goes through

| Step | What happens | The file it leaves |
| --- | --- | --- |
| 1. Ticket | One bounded piece of work is opened as a ticket. (ADR 0001 replaces the ticket with the work order: under ADRs 0001 and 0002 a work request on the public tracker will be admitted as one or more work orders. That admission is planned, not built.) | A ledger row, the line that tracks the work and its state |
| 2. Brief | The Tech Lead writes the brief with must-pass rows. A lint checks the rows first, because a row that cannot pass wastes an Engineer. | A linted brief |
| 3. Build | An Engineer works in an isolated worktree, on one piece. | A diff on a branch |
| 4. Handback | The Engineer returns evidence, not "done": the test runs, the diff, the commands it ran. | An evidence file |
| 5. Re-run | The Tech Lead re-runs the Engineer's claims. This is the lead's own check, not a Tester verdict. | A log of the re-run |
| 6. Cross-vendor review | Testers review the change, normally one from each vendor. Each writes a verdict, merge or amend, that names the exact commit it read. A Tester who focuses on security joins on sensitive changes. | A verdict on a commit |
| 7. Merge-ready gate | The change is reported merge-ready only if the pull request head is the commit that was reviewed (or that commit merged with main, with no conflict in reviewed code and the full test suite re-run on the result), the full test suite passed, and no blocker is open. | A merge-ready report |
| 8. Merge | The Owner merges. | The merge commit |
| 9. Install | A change to a live system ships as an Owner card: a staged script with a confirm step, an undo, and pins to the reviewed version. The card is itself reviewed. The Owner runs it. | An install log and the pins |
| 10. Record | The ledger row, a short retrospective, approvals and lab results are kept. | The private internal record |

An amend sends the work back into a fix round. A fix round produces a new
head, and the new head is reviewed again. A verdict on the old commit does
not carry over.

Two steps need the Owner's hands: the merge and the install. Every other step
can be checked after the agent that did it is gone.

## The three verification loops

Verification is not one thing. It is three loops with three different costs,
and the order is on purpose.

1. **The local loop is free.** It uses plain code and a local model on the
   Owner's own hardware, and it runs before any paid review. Its main check
   is deterministic: the brief lint, which catches must-pass rows that cannot
   pass. The local model is used only for narrow yes/no questions, and only
   as advice: for example, does a code comment say what the code does.
   Nothing here spends vendor quota.
2. **The cross-vendor loop is paid for in subscription quota, and it gates
   the merge.** It normally has one Tester per vendor, each giving a verdict
   on the exact commit. Its purpose is to catch what the author's own model
   misses: logic and safety defects, and regressions between fix rounds.
   With two vendors, a change is normally read by at least one model from a
   vendor other than the author's. That does not mean no model reviews its
   own vendor's work: one of the two Testers often shares the author's
   vendor. When quota is short, a review can run with a single vendor.
3. **The exploratory loop teaches and never gates.** These are lab runs
   that ask questions such as which jobs a local model can do, or whether a
   cheaper model can take a role. The pass or kill rule is written down
   before the first call, and outcomes are scored blind.
   The results inform later choices. They never decide a merge.

The free loop runs before the paid one. The exploratory loop is kept out of
the path to a merge.

## Human gates

In this flow, three things are done by the Owner alone. By rule, no agent
does them. ADR 0001 lists what the Owner holds more widely.

- **Merge.** Only the Owner merges. The cost is throughput. The benefit is
  one accountable decision per change.
- **Install on a live system.** Only the Owner runs the reviewed Owner card.
- **Public posting.** For now, agents draft issues, comments and reviews for
  public repositories, and the Owner posts them. That holds until the publish
  door in [ADR 0002](adr/0002-audience-and-the-two-doors.md) exists.

A review verdict, or a dismissal of a finding, is itself a claim to be
checked. It is not a fact until the file behind it says so.

## Known limits

The Owner is the throughput bottleneck, because every merge waits for one
person. Measuring cost and cycle time for each change is not built yet. This
is a single-operator process, and this page says what one operator has
exercised, not what it would do at scale.

## Where the terms come from

The roles and objects are defined in
[ADR 0001](adr/0001-the-factorys-objects-and-roles.md). The rule that every
artifact carries an audience, and that only two scripts cross the boundary,
is in [ADR 0002](adr/0002-audience-and-the-two-doors.md). The methods
that Engineers and Testers are expected to apply are listed in
[methods](methods.md).
