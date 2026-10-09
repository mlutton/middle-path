# Launching and notifying are seams, and runtime state is a record

**Status**: decided in September 2026, after two stalls in one day. Builds on [ADR 0001](0001-the-factorys-objects-and-roles.md) and on [ADR 0003, state transitions](0003-state-transitions-are-events-emitted-by-the-process-that-observed-them.md). This ADR records decisions. The delivery states and the assignment record are not yet built, and the release gate is only partly built: a start check on usage limits runs today, and the other interlocks are intended. [The glossary](../glossary.md) marks items that are design.

## Context

The factory's roles reached each other three ways, and the ways behave differently in a manner nothing at the call site expressed:

| Path | Delivery | Durable |
|---|---|---|
| A prompt typed into a terminal pane | immediate | no |
| A cross-session message | may be held for the recipient's user to approve | no |
| A comment on the tracker | immediate | yes, but read only when someone looks |

The difference cost long stalls. A sign-off was relayed by cross-session message, the message was held unapproved, and the work sat for hours with the instruction readable on the record the whole time. Separately, a round finished, wrote its handback and closed its Engineer's invocation, and its Tech Lead waited because nothing said the round had returned. Both moved within minutes of a prompt through a pane.

Neither was a session behaving badly. Both were a caller choosing a transport without being able to see what that transport promises. Launching has the same shape one step earlier: a session was launched in a way that produced nothing to notify.

Pids, pane identifiers and "which session is responsible for this" also lived in a model's memory or in an inherited environment variable. A background session inherited another pane's identifier and would have addressed the wrong session. The Owner delegated sign-off in words, and a session could not prove it held that authority, because no record said who held what.

## Decision

**Name two seams, and let them meet at one thing: the address of a launched session.**

**The launcher** starts a role and returns an addressable handle. Every launch yields something that can later be addressed. A headless subprocess and a terminal pane are both first class, and neither is the default.

The rule for choosing between them is provisional and stated as such. Mapping it to role names, with Engineers headless and Tech Leads in panes, describes today's usage and would make every future role a special case. The discriminator that explains the current cases is whether the role must be addressable while it runs, or only reports when it exits. A role that reports at exit is a headless subprocess. A role that is nudged, ruled at or watched while it runs needs a pane. The factory records which rule it applied whenever a launcher is added, so the mapping can be re-derived from evidence.

**The notifier** delivers a message to an address and names four things the old paths differ on:

- **address**: a handle bound to one session instance, not a role name and not a pane identifier;
- **delivery**: one of three states, below;
- **durability**: the record is permanent and a pane prompt is not;
- **direction**: notify-only, or expecting a reply. A reply is the only acknowledgement.

| Delivery state | What it establishes |
|---|---|
| **submitted** | the bytes were written to the transport |
| **started** | the recipient began a turn caused by this message |
| **acknowledged** | the recipient did something the sender can check |

A successful write establishes only *submitted*. Treating it as *started* is what cost the stall. *Started* needs evidence tied to this message, which is harder than it looks, because a recipient already at work can complete a prior turn and satisfy a naive wait. Where an implementation cannot tie activity to the message, it reports *unconfirmed* and never *started*. *Acknowledged* is not required, since most messages are one-way by intent.

**An address is a session handle, and a role is how you ask for one.** Two sessions of the same role can run at once, and a restart makes a new session in the same role, so a role cannot be an address. Resolution belongs to the registry. Lookup is scoped to the work order, ambiguity is refused and never guessed, and a restart invalidates the handle, which then fails loudly. Delivering to the wrong session is worse than delivering to none.

**The tracker is not a notifier.** A comment is *submitted* the moment it posts and reaches *started* only if someone happens to read it. A durable channel with no delivery is a log.

## Runtime state is a record

Runtime state is to be a typed record with one writer per kind, read by every waiter, notifier and stall check, and never held in memory: `session`, `residency`, `process`, `round` and `assignment`.

**Assignment** records who holds each level right now: the Program Manager, Foreman and Tech Lead for a work order, the Engineer or Tester for a round, and the Owner or a delegate for a request. Each holder has an identity and an address that carries its transport kind, granted by whom and since when. A change of holder is a decision event on the work order, which is also how a shift handover is recorded and how a session proves it holds authority.

Notification then has two layers. `route` walks the tree from a round to its work order to its holders, so no caller names a recipient. `send` delivers to an address using the transport that address names and reports whether the message was delivered, held, recorded or unreachable. A change in how a holder is reached is a record update.

| Event at round end | Routed to |
|---|---|
| Verdict: merge or amend | the Tech Lead |
| Blocked with a stated need, or waiting on the Owner | the Foreman |
| Ended without handback, terminated or stalled | the Tech Lead, and the Foreman if the lane is now idle |
| Work order done and published | the Owner, as request state |

**One release gate** is to run when work moves from ready to released and at every dispatch. Each interlock is an observable fact, for example that no earlier round is unended and that the declared files are not claimed by another open round. The claim is written at dispatch and cleared at close, as in lockout and tagout. Capacity is checked in the same call. Prioritization inside a lane stays with the Tech Lead and across lanes with the Foreman. Admission to the floor is code.

## Considered and rejected

- **Addresses in briefs and environment variables.** The failure this answers.
- **Direct calls to the pane tool at each call site.** It gives the factory a dependency it cannot describe in a sentence, spread across scripts that have no other reason to know what a pane is. The dependency is confined to one module per seam.
- **The record as the notification channel.** It is durable, and *nobody looking* is the property that failed.
- **No abstraction, because one pane tool is what exists today.** Other transports are known to be wanted, and a dependency taken at every call site is paid for again at extraction.
- **One seam instead of two.** Messages go to things this process did not launch, and things are launched that are never messaged, such as a headless Engineer whose wrapper waits on it.
- **A scheduler role.** Sequencing inside a lane is the Tech Lead's judgment, and a role shaped like a person for a one-person floor invents work.

## Consequences

- Delivery becomes a property a caller can read.
- Detecting a stall needs no channel into the watched session, but reporting it does. A stall found and reported nowhere is a log.
- The release gate is intended as one slice, replacing separate checks for residency, preflight and open rounds.
- The factory gains a dependency on one pane tool for interactive roles, bounded to one module per seam.
