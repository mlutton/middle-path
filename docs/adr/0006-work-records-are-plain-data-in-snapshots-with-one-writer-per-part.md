# Work records are plain data, kept as snapshots, with one writer per part

**Status**: decided in October 2026. Builds on [ADR 0001](0001-the-factorys-objects-and-roles.md) and [ADR 0003, state transitions](0003-state-transitions-are-events-emitted-by-the-process-that-observed-them.md). This ADR records decisions. The store is built as a component with its own tests, and the factory's other parts are being moved onto it. Until they are, some records are still kept by hand, as [the glossary](../glossary.md) marks.

## Context

The [operator record](../glossary.md) is where the factory keeps what happened. An early picture of it was a pile of events from which every question is answered by replaying them. Two problems showed up when a store was designed on that picture.

The first was behavior. Each rule about work, such as when a round may start or how many redos are allowed, wanted to live next to the data it reads. A store that carries business rules gets one reason to change for every rule it carries, and every part of the factory that uses it depends on all of them.

The second was the question the record exists to answer. The Owner put it this way: the record is the auditable account of what was built, its current state, how it got there, why it is the way it is, and the evidence that it is correct. A pile of events answers the last three well and the first one only by replay. A reader who wants the current state should be able to read it.

## Decision

**A work record is plain data. All behavior lives in the parts of the factory that own the rules.**

The store keeps only storage mechanics: typed shapes, an atomic append, an append that fails if someone else saved since the writer read, read, list, and recovery from a half-written line. It has no rules about work.

**Each save appends a complete snapshot.** A work order is one file. Every line is the whole state of the order after a change, with who wrote it, why, and the evidence behind it. The latest line is the current state, and the earlier lines are its history, never edited. This keeps the rule in [ADR 0003](0003-state-transitions-are-events-emitted-by-the-process-that-observed-them.md) that history is appended and a correction is a new entry that points at the one it corrects. What changes is that a reader gets the state without replaying anything.

**A snapshot is made of parts, and each part has one writer.** A table names every part of a record and the one component allowed to change it. A save names only the parts that change, and every other part carries forward. A change to a part by anyone but its owner is refused, and so is a part the table does not know. The writer's rules stay with the writer: it reads the latest snapshot, decides in a pure function, and saves with the version check, retrying if someone else saved first.

**Access is through a published interface only.** No part of the factory reads the files directly. The interface never hands out the store itself, because a handle that can save is a way around the writer table. Views for status boards and for the checks that raise alerts are computed from the data and write nothing. A later change of storage then stays inside the component. Whether to give each kind of reader its own narrower handle is still open.

**Plain files first.** Records are line-based files, one work order per file, with backlog items in the same store. A database is deferred until the scan cost or a need for transactions shows up. Snapshots are not compacted. The size at which that gets revisited is a number to be set from real files.

**Text in a record is data.** The why and the evidence in a snapshot are shown quoted and never treated as instructions by whatever reads them, and they have a bounded length.

**The tracker is where requests start, and the record is the truth after that.** Once a work order exists, its record is the source of truth. The two are linked once, with a closing note on the request, and are not synchronized in both directions.

## Considered and rejected

- **A store with business rules in it.** One component then knows every rule, and a rule change touches everything that reads.
- **State as a fold over events, never stored.** It was the first design, and it makes the current state a computation every reader must repeat. Snapshots keep the history and the answer.
- **A database now.** It answers questions nobody has asked yet. Files fit the shape of the work, and the interface keeps the choice reversible.
- **Components reading each other's files.** It makes every file format a promise to every reader. The interface makes the promise one place.

## Consequences

- A reader sees the current state, the history and the reasons from one file.
- Adding a kind of record is adding parts and naming their writers, which is a reviewed change in one table.
- The store stays small, and each rule is tested where it lives.
- Snapshots repeat unchanged parts, so files grow faster than an event log would. That cost is accepted until the data says otherwise.
- A bug in a writer's decision shows up as a wrong snapshot with the writer named, which should make the owner of the fix obvious.
