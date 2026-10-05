# Vision

Middle Path is a software factory. Its job is to deliver meaningful chunks of
software that meet four bars:

- **Product.** It does what the work request asked, judged the way the person
  who asked would judge it.
- **Engineering.** It is built to the repository's standards and reviewed,
  normally by at least one model from a vendor other than the author's.
- **Operational.** It runs where it lands, can be recovered, and does not break
  what is already live.
- **Testing.** Its behavior is pinned by tests, and the evidence that it passes
  can be rechecked by someone who was not there.

These are what the factory is built to deliver, not a claim that every
delivery meets all four today.

This page is the big picture: what the factory is for, the principles it is
built on, and what comes next. The decisions behind it are the
[ADRs](adr/); this page links to them rather than repeating them.

## Principles

These are the principles the factory is being built to. Each one says whether it
holds today or is part of the design.

- **Deliver the work order, with evidence.** The unit of delivery is the work
  order: the artifact, plus evidence that it matches the request. A "done" with
  no evidence behind it is a claim, and claims are checked. That rule holds
  today. Tickets still stand in for work orders until the design lands
  ([ADR 0001](adr/0001-the-factorys-objects-and-roles.md)).
- **Judgment in a few named roles; everything else is a script.** The roles make
  the judgment calls. The design makes release, close, publish and admit scripts
  that a model calls once, and a script either finishes every step and records
  it or records where it stopped ([ADR 0001](adr/0001-the-factorys-objects-and-roles.md),
  [ADR 0002](adr/0002-audience-and-the-two-doors.md)). Today some of these are
  scripts and some are still done by hand.
- **The record, never memory.** Every change of state is meant to be an event
  written by the process that observed it. In the design, events are appended,
  never edited, and a correction is a new event that points at what it corrects.
  Boards and status pages are meant to be views computed from the events; today
  some are still kept by hand, and replacing them is part of the work.
- **Refusals will be recorded too.** When a check refuses something, that
  refusal becomes an event. A run of refusals followed by a pass on the same
  work is something a person should look at, and the record will make it
  visible.
- **Two doors.** In the design, nothing enters execution without a work order
  behind it, and nothing leaves except through the one script that holds public
  credentials ([ADR 0002](adr/0002-audience-and-the-two-doors.md)). Every
  artifact will carry an audience. Today a person posts publicly by hand.
- **Everything a step needs comes in with the work.** A step works from what its
  work order and brief give it. If something is missing, it stops and asks
  instead of guessing. In the design, the question and the answer are recorded
  on the work order.

## The operator record

The operator record (the published ADRs call it the internal record) is where
the factory keeps what happened: its work, the steps taken on it, who held it,
what each step was given, what it returned, and how it ended. It is private to
the installation that runs the factory. Parts of it are still kept as files and
notes by hand; the design makes all of it events.

- **It is a record in storage, not a database of current state.** Today it is
  files in a private git repository. The design gives it a versioned format
  and puts the way it is stored behind one interface, so the storage can change
  without the factory noticing.
- **It is meant to be append-only.** In the design, the current state of a work
  order is computed from its events. That keeps the evidence intact (each step
  is judged on what it was actually given), lets a role restart from the record
  alone, and means a writer cannot quietly change history. Today the record is
  files in a git repository, so history is kept, but not every file is
  append-only.
- **It is meant to be the evidence.** A finished work order should point at
  checkable facts: a commit, a test, a link, and how to recheck each one.
- **Git and a private remote are optional, and they help.** The record does not
  have to live in git; today it does. Keeping it in a git repository gives it history (every
  change kept and dated), a backup when the remote sits on another machine, and
  review (a change to the record can be read like a change to code). If you add
  a remote, keep it private: the record holds the factory's working detail.

## What we assume

The factory assumes that the work orders reaching it carry entry data that
something else has already made safe. No such gate is part of the factory today.
Mitigations for untrusted input, such as text from the open web, are being
prototyped outside the factory; the current focus is building the factory
itself. This is a stated assumption, not a solved guarantee.

## Where it stands

This is a single-operator factory today. The first two decisions, [ADR 0001](adr/0001-the-factorys-objects-and-roles.md)
and [ADR 0002](adr/0002-audience-and-the-two-doors.md), are published, and more
will follow. The code arrives in pieces, each with a clear contract and tests.

## Coming next

**Setting up the operator record.** A first script that creates a new record
(the layout and the format version) or checks an existing one before the
factory uses it, refusing with a named reason if the existing record's format is
one the factory cannot read. If the record has a git remote that looks public,
the script warns, and the factory will not push the record to it.

Each update to this page names the next piece.
