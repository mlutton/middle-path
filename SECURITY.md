# Security

Middle Path is a single-operator factory. This repository holds documentation
and one walking skeleton in `components/middle-path/`, in which GitHub and the
agents are faked. The release tags are not supported versions. This page says what holds
today, what does not hold yet, and how to report a problem. It is not an audit,
and it does not claim the factory is secure.

## What holds today

- **The Owner is the publication point.** One person pushes, opens pull
  requests and merges on this repository. By rule, agents prepare drafts and
  do not post to it. [ADR 0001](docs/adr/0001-the-factorys-objects-and-roles.md)
  lists the Owner's decisions, and [ADR 0002](docs/adr/0002-audience-and-the-two-doors.md)
  describes the two doors that work passes through.
- **This tag crossed from the private workspace through a checked
  procedure.** The procedure is followed by the Owner and the factory, and
  parts of it are run by hand. The files that will be published get a
  publication scan, a pre-push check, a prose check and a read by a second
  reader against a written checklist, and then the Owner's own read. By the
  procedure, a check that was not run blocks the crossing. A scan also runs
  daily against this repository from the private workspace, without anyone
  starting it.
- **A claim needs evidence.** Work is accepted on checkable evidence.
  Every change is reviewed by a model other than its author; security-boundary
  and other high-risk changes need two vendors; a review never passes for lack
  of capacity: the work waits. See [how verification works](docs/verification.md).

## What does not hold yet

- **Review does not prove correctness.** Two vendors lower the chance of a
  shared blind spot and do not remove it. A structural check shows only that
  evidence exists; whether the claim is true is a separate question.
- **The review tiers and round budgets are process.** They decide how much
  attention a change gets. They are not a proof that a change is safe.
- **Nothing has been independently audited.**
- **Controls that are decided but not built** are marked "design; not yet
  built" in the [glossary](docs/glossary.md). Do not rely on them.
- **One point of control.** The Owner can delete records and rewrite history.
  The record is kept in git, which preserves history, but not every file in it is
  append-only yet.
- **The publishing door is still manual.** The one script that holds public
  credentials is design. Today the Owner posts publicly by hand, and nothing
  automatically refuses a private value on its way out beyond the checks above.
- **Untrusted input.** The factory assumes that work orders reaching it were
  made safe by something else. No such gate is part of it today.
- **There is no supported version.** The skeleton is a demonstration of a path
  with faked services. Nothing in this repository is released for use.

## Scope and reporting

This page covers this repository: its documentation and the skeleton. The private workspace
the factory runs in is not published, and the agent-brain product has its own
repository.

Report a security problem through this repository's Security tab: choose
"Report a vulnerability". The report stays private between you and the
maintainer unless an advisory is published. Please do not open a public issue for a security
problem. Anything
that is not a security problem can be a public issue.
