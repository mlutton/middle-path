# Middle Path

A software factory. Models supply the judgment, scripts supply the
instructions, and every change leaves a record.

Middle Path is the gravel walk down the spine of Kenyon College; every
building opens onto it. This repository is the same idea for software
delivery: one path that every piece of work crosses, with gates along it
and a record of who walked it.

## What it is

An orchestration layer for building software with AI coding agents under
platform-engineering discipline. It is being extracted from a private
workspace where it has run since September 2026, building a real product in
public ([agent-brain](https://github.com/mlutton/agent-brain)) and publishing
numbers about itself while it did.

The thesis:

- **Judgment lives in named roles.** An Owner writes work requests and merges.
  A Foreman runs the floor. A Tech Lead per lane designs and slices. Engineers
  build; Testers verify, some of them without the acceptance criteria.
- **Everything else is a script a model calls once.** In the design,
  release, close, publish and admit are scripts; today some are and some are
  still done by hand. A script boundary is a transaction boundary; a script
  either finishes every step and records them or records where it stopped so
  a rerun resumes there.
- **State is a record, never memory.** In the design, every transition is an
  event written by the process that observed it, and work orders, rounds, who
  holds what, and what each round was shown are kept in the record, so any
  role can be relaunched from the record alone. Today part of that record is
  still kept by hand.
- **Two doors.** In the design, nothing enters execution without a work
  order behind it, and nothing leaves without passing the one script that
  holds public credentials; every artifact carries an audience. Today the
  Owner posts publicly by hand.

## What you can do with this repository today

This repository holds documentation and one walking skeleton. The skeleton, in
[components/middle-path](components/middle-path/), is a small slice that takes a
story (the skeleton's input for one change) to a merge decision through every
layer, with GitHub and the agents
faked. It shows the shape of the path and where it refuses to go forward, not
how any model behaves. To run it, use `components/middle-path/run-suite` from
the top of a clone, or `./run-suite` inside that folder (Python 3.11 or later
and pytest). Beyond that, you can read
the design and check it against the evidence:

- Read the [vision](docs/vision.md) for what the factory is for and which
  principles hold today and which are still design.
- Read the decisions, listed below, and the [glossary](docs/glossary.md), which
  marks the mechanisms that are "design; not yet built".
- Read how the factory works day to day: the [roles](docs/roles.md), the
  [lifecycle](docs/lifecycle.md) of a piece of work, the
  [flows](docs/flows.md), [how verification works](docs/verification.md) and the
  [methods](docs/methods.md).
- Read the case study (below), where the same ideas are tried on real work and
  the numbers are published.

## The decisions

The decisions are recorded as ADRs and are the first thing worth reading:

- [0001, the factory's objects and roles](docs/adr/0001-the-factorys-objects-and-roles.md)
- [0002, audience and the two doors](docs/adr/0002-audience-and-the-two-doors.md)
- [0003, state transitions as events](docs/adr/0003-state-transitions-are-events-emitted-by-the-process-that-observed-them.md)
- [0004, launching and notifying as seams](docs/adr/0004-launching-and-notifying-are-seams-and-runtime-state-is-a-record.md)
- [0005, review depth](docs/adr/0005-review-depth-is-chosen-by-what-the-subject-can-damage.md)
- [0006, work records](docs/adr/0006-work-records-are-plain-data-in-snapshots-with-one-writer-per-part.md)
- [0007, components and their published interfaces](docs/adr/0007-a-component-is-a-folder-with-its-own-tests-and-a-published-interface.md)
- [0008, seams that narrow what a test reaches](docs/adr/0008-a-seam-narrows-what-the-code-under-test-can-reach.md)
- [0009, the round cap as a sensor for weak design](docs/adr/0009-the-round-cap-is-a-sensor-for-weak-design.md)

More decisions will be added as they are ruled on.

## The case study

The factory is described in a Substack series, "Agent-first delivery", which
starts with [the introduction](https://mlutton.substack.com/p/one-person-a-team-of-agents-and-295).
Parts 2 to 5 each take one claim the factory depends on and show what it took
to earn it, on real work:

- [Part 2, what a local model is actually for](https://mlutton.substack.com/p/what-a-local-model-is-actually-for)
- [Part 3, if the test is hard to write, the shape is wrong](https://mlutton.substack.com/p/if-the-test-is-hard-to-write-the)
- [Part 4, green tests don't mean it works](https://mlutton.substack.com/p/green-tests-dont-mean-it-works)
- [Part 5, run the new thing beside the old one](https://mlutton.substack.com/p/run-the-new-thing-beside-the-old)

## What is not here yet

Release R1.2 introduced typed review verdicts and a pure readiness decision.
R1.3 is planned to make that decision authoritative, backed by tests for every
listed class of input.

- **Most of the code.** The skeleton is the first slice. The rest of the working
  code lives in a private workspace today and will arrive here one slice at a
  time, each with its own tests.
- **A packaged way to run it.** There is no installer and no supported version;
  the skeleton runs from a clone.
- **The record's storage and format.** The record is described, and today it is
  files kept in a private repository, partly by hand.
- **The scripts in the design.** Release, close, publish and admit are not all
  scripts yet, and the one script that holds public credentials is still
  design. Today the Owner posts publicly by hand.
- **Protection from untrusted input.** The factory assumes that work orders
  arrive already made safe. No such gate is part of it today.
- **The rest of the design.** The glossary marks the objects and mechanisms that
  are decided but not yet built, among them the work order itself (tickets stand
  in for it), the audience field, most events, status views computed from events
  and the recording of refusals.
- **Anyone but one operator.** This is a single-operator factory. It says what
  one operator has exercised, not what it would do at scale, and nothing here
  has been independently audited.

Security reports and what holds today are in [SECURITY.md](SECURITY.md). Changes
to this repository are in [CHANGELOG.md](CHANGELOG.md).

## Name

<img src="docs/middle-path.jpg" alt="Middle Path at dusk, painted" width="400">

Middle Path runs the length of Kenyon's campus. Old Kenyon, which burned in 1949
and was rebuilt the next year, stands at one end, and Bexley Hall at the other.
In between are the academic, residential and administrative buildings. Middle
Path is what connects everything on the hill in Gambier, Ohio, where the author
grew up.
