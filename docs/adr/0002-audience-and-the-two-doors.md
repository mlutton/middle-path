# Every artifact carries an audience, and Admit and Publish are the only doors between the factory and the world

**Status**: decided in the 22–23 September 2026 architecture round.

See [the thesis this supports](../../README.md) and [ADR 0001, the factory's objects and roles](0001-the-factorys-objects-and-roles.md) for the roles named below.

## Context

Whether something was safe to post publicly has been decided at the moment
of posting, by a model, from memory. That decision was sometimes wrong: a
private read-receipt marker reached a public repository, because the rule
said *always echo it* and never said *where*. Nothing bound a public merge to
a verified head, so a merge could carry a different candidate than the one
that passed verification.

The same session that argued a design internally then wrote the public
specification amendment in the same voice, so the line between "what we are
discussing" and "what the repository is now held to" was drawn by tone.

Inbound, a work request is translated into factory terms in issue comments,
and nothing records that a piece of execution traces to a request the Owner
actually wrote.

## Decided

**Audience will be a field on every factory artifact**, with two values:
`internal` and `public`. It will be set by the Program Manager when the
artifact is created and will never be inferred later. Seam maps, round
records, packets, findings before disposition, retros and the intake log
are internal. Specification amendments, ADRs of a public repository, pull
request bodies, ticket state, nonconformance results at disposition and
acceptance reports are public. Promotion will be a Publish event that
creates the public artifact as a new object; the internal one stays
internal.

**Two scripts will be the only doors.**

- `admit(work_request) → work order`: will record the request as a work
  order in factory terms, linked back, audience set, state raw. Nothing
  will enter execution without a work order behind it.
- `publish(kind, subject) → receipt`, for kinds `pr`, `tracker_state`,
  `post`, `request`: will be the only holder of public credentials. It
  will refuse an artifact whose audience is not public, a head the record
  has not verified, and a body carrying a private token. It is meant to be
  a credential boundary in code, not a rule a model remembers: **no
  factory process is to hold a public credential**, and the release gate
  will check that before a round starts.

**Work requests will be written only by the Owner directly or by a
delegate through Publish.** A Program Manager filing a defect found
mid-feature is the delegate case; the new request will then be admitted
back as a work order linked to the one that found it.

**A reconciler, not a daemon, will project state outward.** At every
close, accept and disposition, a script will diff the record against the
public tracker and apply the difference through Publish. It will be
idempotent and will reuse the tracker reader; an event trigger can replace
the schedule later without changing what is published.

**What leaves the factory**, and nothing else: work request state as state;
the pull request with its evidence, from a verified head, citing the
request; the outcome at completion; inspection results on a public product
at disposition, curated; the outcome of a ruling on a public contract;
acceptance reports.

## Considered options

- **A scan at posting time.** A gate for handbacks already exists and did
  not stop the leaks, because the posting paths did not run it. A gate that
  every path must remember to call is the failure mode.
- **A rule in the entry file.** Tried for the token. The rule is right, and
  it is still a rule a model remembers.
- **Three or more audience levels now.** Deferred: a company will need a
  "customer, not public" level; the field is a level, not a boolean, and a
  third value is a data change when it is needed.

## Consequences

- The factory will run without public credentials. `publish` will hold them
  under its own identity, separate from every factory session, so the public
  and private roles never share credentials; the release gate will refuse a
  round whose process holds one.
- Every work request will close with a public completion record: what the
  request asked for, what the work order committed to when it was admitted,
  what was delivered, and the evidence that it is done (the merged change
  from a verified head, and the checks it passed), plus anything left undone
  or changed along the way.
- The private tracker will stop being the orchestration surface. It will
  narrow to internal conversation; the kit's own work requests will move to
  the factory repository's public tracker at extraction; receipts, shadows
  and the intake thread will become renders of the record.
- Findings on a public product will be nonconformance records on the work
  order, published at disposition in curated form, not tickets filed at
  discovery.
- The two-tracker model will be rewritten: the public tracker will
  hold requests and outcomes; the internal record will hold the factory's work;
  the private tracker will hold conversation.
