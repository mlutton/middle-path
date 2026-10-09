# Glossary

The words the README, the ADRs and the other pages use. Where a definition
describes a mechanism that is decided but not yet built, it says
"design; not yet built". Older names are listed at the end.

## Roles

**Owner**:
The one human accountable for the factory. Writes work requests, accepts work,
merges, and holds credentials, administrative settings and the power to delete
records or rewrite history.
_Avoid_: user, admin

**Program Manager**:
The role that faces the outside: translates a work request into factory terms,
and owns the audience of every artifact and the wording of everything that
leaves.
_Avoid_: product owner, editor

**Foreman**:
The role that runs the floor across lanes: capacity within the Owner's limits,
assigning holders, and sequencing across lanes.
_Avoid_: coordinator, supervisor

**Tech Lead**:
The role, one per lane, that owns the design round, the slicing and what a round
needs to see.
_Avoid_: architect, driver

**Engineer**:
The role that builds one slice in a build or fix round, from its brief.
_Avoid_: executor (retired), developer

**Tester**:
The role that verifies a subject, a round's candidate or a pull request head,
against its criteria in a separate session, and gives a verdict.
_Avoid_: verifier (retired), QA

**Driver**:
Scripts only: dispatch, wait and close. Its judgment moved to the Program
Manager and the Tech Lead.
_Avoid_: orchestrator

**Consult**:
An advisory session started by a holder for one question. It holds nothing and
decides nothing.
_Avoid_: reviewer

**Judge**:
A fresh session with no stake in the change that settles one disputed finding,
at the head it is given. Its ruling is uphold, overrule, conditional or no
ruling. A ruling settles the disputed triage call and is not an approval; the
Owner's merge is still the gate.
_Avoid_: reviewer, arbiter

**Holder**:
The session, with identity and address, that is responsible for a work order or
round right now. Recording each change of holder as an event is design; not yet
built.
_Avoid_: owner (a different role)

**Lane**:
A stream of work with one Tech Lead.
_Avoid_: team, track

## Work

**Work request**:
What the Owner asks for, in public words, on the public tracker of the
repository the work is for: a feature or a defect. One request may become
several work orders.
_Avoid_: ticket, requirement

**Work order**:
The request restated in factory terms, with one state machine: raw, refined,
ready, released, in progress, and then done, failed or abandoned (its final
states). Today a ticket stands in for it; the work order itself is design; not
yet built.
_Avoid_: ticket, task

**Round**:
One operation on a work order: design, build, verify or fix. A build and its
check are two rounds, and their parent is the work order.
_Avoid_: iteration, cycle

**Fix round**:
A round that changes the work after an amend. It produces a new head, which is
verified again; a verdict on the old head does not carry over.

**Review pass**:
The set of verify rounds at one head. Counting passes keeps "round" for the
operation itself.
_Avoid_: round (in the review sense)

**Brief**:
The Engineer's instructions for one round: the deliverable, the inputs, the
constraints and what counts as done, with the evidence expected for each
criterion. It is fixed when the round starts. The ADRs and the methods page
call the same instructions a packet.
_Avoid_: prompt

**Handback**:
What a build or fix round returns: what was used, what was produced, the
evidence, and the Engineer's claim.
_Avoid_: report

**Claim**:
The Engineer's own report on its round: complete or blocked. A complete claim
needs evidence for each criterion. On other pages "claim" also has its everyday
sense, any statement not yet backed by a file; this entry is the Engineer's
report.
_Avoid_: result, outcome, status

**Verdict**:
A Tester's judgment on one head, from a verify round: merge, or amend, which
sends the work to a fix round.
_Avoid_: result, outcome, approval

**Ending**:
How a round stopped: closed, terminated, ended-without-handback, or superseded.
Recorded by the script that ran the round, never by the Engineer. A work order
has its own final states: done, failed or abandoned.
_Avoid_: result, outcome, status

**Evidence**:
A checkable fact behind a claim: a commit, a test, a link, with how to recheck
it.

**Re-run**:
The Tech Lead's own repeat of the checks behind the Engineer's claims. It is not
a Tester's verdict.

**Merge-ready**:
Reported only when the pull request head is the commit that was reviewed, the
full test suite passed, and no blocker is open.

**Accepted**:
A work order the Owner has accepted. In the flows on these pages that is when
its verify rounds passed at one head and the Owner merged; a script that
observes the merge records it (design; not yet built).

**Owner card**:
How a change to a live system ships: a staged script with a confirm step, an
undo and pins to the reviewed version, itself reviewed, and run by the Owner.

## The record

**Operator record**:
Where the factory keeps what happened: its work, the steps taken on it, who held
it, what each step was given and returned, and how it ended. The ADRs call it
the internal record. It is private to the installation that runs the factory.
_Avoid_: memory, database

**Round record**:
What the operator record keeps about one round: its brief, its handback, its
events and its ending.

**Event**:
One row appended to the record by the process that observed the fact. Events are
never edited; a correction is a new event that points at the one it corrects.
Round events are appended today; the rest is design; not yet built.
_Avoid_: log line, update

**Projection**:
A view computed from events, such as a work order's state or a status page.
Never typed by hand (design; today some pages still are).
_Avoid_: status field

**Refusal**:
A check declining to let something through, recorded as an event so a run of
refusals followed by a pass can be seen (design; not yet built).

**Script boundary**:
A transaction boundary: a script either finishes every step and records them,
or records where it stopped so a rerun resumes there.
_Avoid_: function

**Relaunch test**:
Stop the session holding a work order partway and have a fresh one continue
from the record alone.
_Avoid_: failover

## The doors

**Audience**:
A field on every factory artifact with two values, internal and public, set when
the artifact is created and never inferred later (design; not yet built).
_Avoid_: visibility, classification

**Door**:
One of the two scripts through which anything crosses the factory's boundary:
Admit inward and Publish outward (design; not yet built). Today the Owner posts
publicly by hand.
_Avoid_: gateway, API

**Admit**:
The script that records a work request as one or more work orders, linked back,
with the audience set (design; not yet built).
_Avoid_: intake

**Publish**:
The only script that holds public credentials. It refuses an artifact whose
audience is not public, a head the record has not verified, and a body carrying
a private token (design; not yet built).
_Avoid_: release, post

**Receipt**:
What Publish returns for what it published (design; not yet built).
_Avoid_: confirmation

**Reconciler**:
A script, not a background service, that compares the record with the public
tracker at each close, acceptance and disposition and applies the difference
through Publish (design; not yet built).
_Avoid_: sync job

**Context request**:
A step's request for something its brief lacked. The answer comes back as an
addition to the work order. The intent is a channel to the Owner that is
separate from Publish; until it is built, how the request crosses the
factory's boundary is not yet decided (design; not yet built; today the step
stops and asks).

**Method**:
A document that is read and applied, not a tool to install or invoke.
[methods](methods.md) says which must be read before which decisions or edits.
_Avoid_: skill, plugin

## Older names

Older material uses these.

| Older | Current |
|---|---|
| Executor | Engineer |
| Verifier | Tester |
| Driver (as a judgment role) | Program Manager and Tech Lead; the Driver is scripts only |
| Parcel | Round (on a work order) |
| Ticket (as the factory's object) | Work request and work order |
