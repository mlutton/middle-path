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
- **Everything else is a script a model calls once.** Release, close,
  publish, admit. A script boundary is a transaction boundary; a script
  either finishes every step and records them or records where it stopped so
  a rerun resumes there.
- **State is a record, never memory.** Every transition is an event written
  by the process that observed it. Work orders, rounds, who holds what, and
  what each round was shown are on disk. Any role can be relaunched from the
  record alone.
- **Two doors.** Nothing enters execution without a work order behind it;
  nothing leaves without passing the one script that holds public
  credentials. Every artifact carries an audience.

## Where it stands

The decisions are recorded as ADRs and are the first thing worth reading.
They arrive here through extraction from the private workspace once ruled on;
until then the proposed set is in review there. The kit itself, about 13,000
lines of scripts and 22,000 lines of tests, follows in slices, each landing
with the failing test that motivated it.

This is a single-operator factory today. It says what one operator has
exercised, not what it would do at scale.

## Name

Old Kenyon burned in 1949 and was rebuilt the next year from the original
drawings. Middle Path is the walk that runs past it. Both are on the hill in
Gambier, Ohio, where the author grew up.
