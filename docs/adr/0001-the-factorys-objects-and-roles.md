# The factory's objects are the work request, the work order and the round; its roles are Owner, Program Manager, Foreman, Tech Lead, Engineer and Tester

**Status**: decided in the 22–23 September 2026 architecture round; the factory diagram, seam map and component inventory are the working artifacts (not yet published).

**Amended 2026-09-23 after a role audit.**

See [the thesis this supports](../../README.md) and [ADR 0002, audience and the two doors](0002-audience-and-the-two-doors.md) for the publish rules that build on these roles.

## Context

The layer had parcels, rounds, tickets and shadow tickets, and three roles
with judgment — Driver, Executor, Verifier — plus the Owner. Three weeks of
running it showed the objects and roles were not the ones the work has:

- **Nothing sits above a round but a ticket number.** A ticket is a tracker
  artifact typed by hand; the record has no object that says what the
  factory took on, in its own terms, or what state that work is in. The
  board was repeatedly wrong, because the only place that state existed
  was prose.
- **Public need and factory backlog were one tracker.** Shadow
  tickets drifted from their public originals; the private tracker filled
  with receipts, findings and intake, not requests.
- **The Driver held two jobs.** It assembled packets and decided next rounds
  (judgment) and it dispatched, waited and closed (mechanics). Every
  mechanical failure of the week — stale checkouts, a stalled wake, hand-typed
  state — happened in the judgment role's shell.
- **The boundary role had two faces.** The session that translated a request
  into factory terms also posted to public trackers, and the private
  read-receipt marker reached a public repository.

The manufacturing vocabulary was reviewed term by term. Where a factory term
named a mechanism the layer lacked, it was adopted; where it named the same
thing under another word, the software word was kept.

## Decided

**Three objects.**

| Object | Where | What it is |
|---|---|---|
| **Work request** | The public tracker of the repository the work is for | What the Owner asks for, in public words; kind feature or defect. Created by the Owner directly or by a delegate through Publish (ADR 0002). One request may yield several work orders |
| **Work order** | The internal record | The request restated in factory terms and linked to it. One state machine: raw → refined → ready → released → in progress → done, with failed and abandoned as endings. Unreleased work orders are the backlog; released ones are execution. Nonconformance records, decision events, waiting-on and links to other work orders hang off it |
| **Round** | The internal record, attached to a released work order | One operation on the work order: design, build, verify or fix. Its record names the references exposed to it and its declared file set; its handback returns what was used and the evidence; it ends with an ending and a verdict. It is the only object an Engineer or Tester sees. A build round's candidate is verified by **one or more verify rounds**, one per Tester (for example one Tester per vendor and the criteria-blind arm). Each is bound to the build round and to the head it read, with its own ending and verdict. A fix round produces a new head, and verification repeats against that head. The build is accepted when the verifications the lane requires have passed at the same head. |

A **review pass** is the set of verify rounds at one head. The process docs count passes ("pass 3"), not "rounds", so that "round" always means this ADR's object.

State will derive upward and will never be typed: a request reads done
because its work orders are done, because their rounds have endings. Each
level will also record its **holder** — the session with identity and
address that is responsible for it right now — and a change of holder will
be a decision event.

**Six roles, and scripts where there was a seventh.**

| Role | Faces | Owns |
|---|---|---|
| **Owner** | Everything, read-only | Work requests; acceptance; contracts; lane allocation; amendment of prior rulings; merges (approve and merge in one sitting); credentials, tokens and admin settings; sudo and root; deleting records or rewriting history; creating a public repository or changing a repository's visibility; installing or changing the guard hook; and capacity limits (the Foreman operates within them). Other permission decisions are delegated to the Foreman. |
| **Program Manager** | The outside | Translation of a request into factory terms, with the Tech Lead for technical meaning; the audience of every artifact; the wording of everything that leaves; filing requests as the Owner's delegate; change control; acceptance evidence. Operates Admit and Publish. The contract-manufacturing "customer program manager"; in a product organization a Product Manager holds the seat |
| **Foreman** | The floor, across lanes | Capacity within the Owner's limits; assignment of holders; sequencing **across lanes**, and admission to the floor; the order of work inside a lane stays with the Tech Lead. Owns stalls and the one permission-wait queue: decides waits outside the Owner's list; routes waits on that list to the Owner, confirms each cleared from evidence, and never answers one for the Owner. Owns the quota gate and its override: the Foreman uses the override when the Owner says one is wanted, recording each use (actor, the Owner's call, the command and its result) in the internal record's approvals log. Makes dispositions that stay internal; never speaks to the outside |
| **Tech Lead**, one per lane | The lane | The design round; slicing; the path per slice (full or light); what a round needs to see |
| **Engineer** | A round | Builds a slice from a round record. May be kept for the fix rounds of one slice; each brief is still written to the record first, so a fresh Engineer can continue from it. Was Executor |
| **Tester** | A round or PR head | Verifies a subject (a round's candidate or a PR head) against its criteria in a separate session; each verification is a verify round bound to the head it read. A reviewer is a Tester whose subject is a PR head. The lead's own verification is the Tech Lead's acceptance check, not a Tester verdict. Was Verifier. The adversarial arm is a Tester given no acceptance criteria |
| **Driver** | Nothing | Scripts only: dispatch, wait, close. Its judgment moved to the Program Manager and the Tech Lead |

A consult is an advisory session started by a holder for one question; it holds nothing and decides nothing.

For a single operator, several roles are one person or one session wearing
different hats. The hat is recorded on every action through the audience
field and the assignment record, so the split costs nothing now and becomes
several people without a redesign.

## Considered options

- **Keep parcels and tickets as the objects.** Rejected: a parcel is one
  attempt at a ticket, and a ticket is a tracker artifact. Neither can hold
  the factory's own state or be the unit a customer asked for.
- **Two objects across the boundary, one intake item and one execution
  record.** Considered on 23 September and collapsed: a work order with a
  state machine covers both, and the backlog is a view, not a second object
  to keep in sync.
- **"Requirement" or "feature" for the tracker-side object.** Rejected: a
  defect is not a feature, and "requirement" carries formal weight. "Work
  request" pairs naturally with "work order".
- **"Coordinator", "Editor", "Supervisor" for the boundary role.**
  Rejected in turn: coordinator already names the kit's sessions and says
  nothing about what is decided; editor implied a publishing house;
  supervisor already names the process that watches a Driver.
- **One boundary role holding both doors.** Rejected: floor work and public
  posting are different jobs, and a contract manufacturer gives the customer
  relationship to a program manager and the floor to a foreman.

## Consequences

- The roles table, the lane cards and the packet templates
  are rewritten to these names by a slice; until then this ADR is the mapping.
- The internal record gains the work order and its state machine, the
  assignment record, decision events and waiting-on.
- The private tracker will narrow to internal conversation; receipts, shadows
  and the intake log will become renders of the record ([ADR 0002](0002-audience-and-the-two-doors.md)).
- A relaunch test is a first article for every role: kill the session
  holding a work order mid-flight and have a fresh one continue from the
  record alone.
