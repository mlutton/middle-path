# Middle Path

A software factory. Models supply the judgment, scripts supply the
instructions, and the record shows every row.

Middle Path is the gravel walk down the spine of Kenyon College; every
building opens onto it. This repository is the same idea for software
delivery: one path that every piece of work crosses, with gates along it
and a record of who walked it.

## What it is

An orchestration layer for building software with AI coding agents under
platform-engineering discipline. It is being extracted from a private
workspace where it has run since September 2026, building a real product in
public ([agent-brain](https://github.com/mlutton/agent-brain)) and measuring
itself while it did.

The thesis, earned rather than claimed:

- **Judgment lives in named roles.** An Owner writes work requests and merges.
  A Program Manager translates them and owns everything that leaves. A
  Foreman runs the floor. A Tech Lead per lane designs and slices. Engineers
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

## Where it stands

The decisions are recorded as ADRs and are the first thing worth reading:
[the factory's objects and
roles](docs/adr/0001-the-factorys-objects-and-roles.md), [audience and the
two doors](docs/adr/0002-audience-and-the-two-doors.md), [state
transitions as events](docs/adr/0003-state-transitions-are-events-emitted-by-the-process-that-observed-them.md),
[launching and notifying as
seams](docs/adr/0004-launching-and-notifying-are-seams-and-runtime-state-is-a-record.md),
[review depth](docs/adr/0005-review-depth-is-chosen-by-what-the-subject-can-damage.md),
[work records](docs/adr/0006-work-records-are-plain-data-in-snapshots-with-one-writer-per-part.md),
[components and their published
interfaces](docs/adr/0007-a-component-is-a-folder-with-its-own-tests-and-a-published-interface.md),
[seams that narrow what a test reaches](docs/adr/0008-a-seam-narrows-what-the-code-under-test-can-reach.md)
and [the round cap as a sensor for weak
design](docs/adr/0009-the-round-cap-is-a-sensor-for-weak-design.md), with the
[methods](docs/methods.md), the [roles](docs/roles.md) and [how verification
works](docs/verification.md) alongside. Further decisions arrive the same
way, by extraction once ruled on. The kit itself, about 13,000 lines of
scripts and 22,000 lines of tests, follows in slices, each landing with
the failing test that motivated it.

This is a single-operator factory today. It says what one operator has
exercised, not what it would do at scale.

## Name

<img src="docs/middle-path.jpg" alt="Middle Path at dusk, painted" width="400">

Old Kenyon burned in 1949 and was rebuilt the next year from the original
drawings. Middle Path is the walk that runs past it. Both are on the hill in
Gambier, Ohio, where the author grew up.
