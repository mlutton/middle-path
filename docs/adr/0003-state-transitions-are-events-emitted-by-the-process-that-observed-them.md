# State transitions are events emitted by the process that observed them, and rows are projections

**Status**: decided in September 2026, after measuring the record. Builds on [ADR 0001, the factory's objects and roles](0001-the-factorys-objects-and-roles.md). Of what follows, the four round endings are recorded today. Everything else is the design the factory holds itself to and is built toward, and [the glossary](../glossary.md) marks each such item "design; not yet built".

## Context

The operator record held a large share of rounds with no row. Most were rounds that a later round had replaced, and in nearly all of those the successor closed, so the outcome was recorded under the successor. The ledger was not losing work. It was losing the fact that an attempt happened at all, and what the attempt cost.

The cause was not carelessness. The factory had no transition for a round that ends without a handback. Closing a round requires a handback, correctly, because a handback is the Engineer's claim and a round without one makes none. So a replaced attempt had no way to end. Closing had become something done to unblock the next dispatch, and a round with nothing after it was never closed.

Two other failures shared the root:

- **Facts were flattened into prose and scraped back out.** A handback check script refused an accurate handback because its verdicts were not at the start of a line, then refused another that honestly reported an authorized substitution, which could be satisfied only by inventing a verdict. A brief check refused ordinary briefs because a branch name appeared in English rather than as a field. Each fact was structured when it happened and had to be rebuilt later.
- **Honesty was upheld by character, not by construction.** In two days three sessions each declined a false but passing record that was available to them. All three were right, and none was forced to be.

## Decision

**Every state transition in the record is an event emitted by the process that observed the fact, at the moment it observed it. A row is a projection of that event log, not something authored at close.**

Three rules follow, and they are the whole decision:

1. **One writer per transition, and it is a script.** An agent may cause a transition and never records one. The launch script is meant to emit the exit classification because it saw the exit. A continuation names its antecedent, and the antecedent's ending follows from that. An agent asserting that a round ended cleanly is the thing being removed.
2. **A transition reads an observable fact, or it is not built.** If a rule cannot name the fact it reads, it will one day be satisfiable only by fabrication. Prose is not an observable fact.
3. **A round cannot be dispatched while its predecessor on the same work order has no ending.** It is tied to the specific predecessor and does not count work in progress. It needs no threshold, and fabrication cannot satisfy it, because the endings it accepts include *terminated with a reason* and *superseded*, which are honest endings.

A round can end four ways:

| Ending | Written from |
|---|---|
| closed | a handback exists |
| ended-without-handback | the wrapper's exit classification |
| superseded | an unended attempt is abandoned in favor of a successor |
| terminated | the word of the role that decided it, plus a required reason |

Waiting on a ruling is a recorded, non-terminal state a round sits in, never an ending, and the round is later closed, terminated or superseded like any other. A work order ends separately, from an observed merge by the Owner or a delegate the Owner named for that work order.

The boundary this draws is between mechanism and judgment. Code decides what happened, because that is observable: a round ended, a merge occurred, tokens were spent. Judgment decides what to build and whether it is right. Sign-off, rulings on scope, and whether to merge stay with the Owner, and this decision does not change that.

## Transactions

This section is design. Closing a round is built; the other transactions are the way the factory holds itself to work, and no script yet ties a failed attempt to a retry decision. The round is the unit of a transaction, and the work order is a projection over its rounds with no state of its own. That removes the drift where a request says in progress while its rounds say otherwise.

A retry is one transaction. "Make sure round N has an ending" and "append round N+1, linked to it" are a single decision, and splitting them into separate scripts is what let the records drift. So the transaction is named for the intent: `retry` has no code path that performs half of it. A ledger exposes `withdraw()` instead of `setBalance()` for the same reason. A name that carries the intent makes the incoherent state impossible to express.

| Transaction | Predecessor's ending | Authorized by |
|---|---|---|
| `retry` or `fix` | ensured; *superseded* only if it had none | a finding from a Tester or a Tech Lead |
| `terminate` | *terminated*, reason required | the deciding role's word and a reason |
| `close` | *closed* | a handback exists and the gates pass |
| `accept` | work order level | an observed merge |

`close` and `accept` are different scripts because they are different authorities. A round ends on the Tester's rules and a work order ends on the Owner's. Conflating them is how a work order gets marked done because its last round passed. `accept` records that an acceptance happened. It never grants merge authority to whoever runs it.

Where a predecessor already has an ending, the transaction validates it and writes no new one. A round that closed cleanly and is then followed by a fix round stays closed, with the successor linked to it.

## When code cannot decide

Some defects are not derivable from any fact the system holds: a brief whose deliverable forbids what its constraints require, an acceptance criterion that accepts the very value the request exists to forbid, a finding that states a remedy instead of the property it violates. No pattern match decides these, and attempts to build one produced false refusals and a gate that could be passed only by fabrication.

This tier is design. Where code cannot derive the fact, a small model is to check the brief's variable parts at the seam, before it is handed to another role. This ranks strictly below code. Four constraints keep it from becoming the thing it replaces:

1. **Named questions, not broad review.** It asks whether two sections contradict each other, or whether a criterion can be met without doing the work. It does not ask whether the brief looks right.
2. **Variable parts only.** The template is code's problem and is checked once.
3. **It reports and never edits.**
4. **It says what it could not check.** A silent pass must not be mistaken for a clean one.

Below that sits the last resort: the role receiving an artifact checks what it needs before starting work, and **the check is counted as an event**. An uncounted early check is a permanent tax in the costume of diligence. When two independent occurrences, in different work orders and different sessions, show the same check, it is promoted out of this tier, into code where the fact is derivable or into the seam check where it is not. This tier is where a check goes that has not yet earned automation, and the count is what earns it.

## Considered and rejected

**A cap on work in progress.** The number of open items was dominated by retries of the same work, so the cap would have sat far above real concurrency. It also never fires on a final round, which is the pattern that went unclosed. The precondition in rule 3 is the part of the idea that survives the data.

**Better instructions.** Prose telling an agent to close its rounds is what produced the unaccounted rounds across three conscientious sessions.

**A fallback read path** that lets `close` read a handback from an archive. Two input paths could disagree about what a round handed back, inside the tool whose job is to be the record.

## Consequences

- Recomputing a row is meant to become replay of the log, instead of a command with defects of its own.
- Legacy rounds are to be migrated from the artifacts that survive. What no artifact covers is to be recorded as `unknown` and never inferred. Replay never promotes `unknown` into a decided ending, and `terminated` always needs a human's word and a reason.
- A round that produced nothing is meant to get a row, with the tokens and time it spent. Work order cost stops being understated by however many retries it took.
- The design intends endings to be total: a heartbeat and a budget per round would write *terminated* with a reason when neither a handback nor a deciding role's ending arrives. That part is design.
- The glossary qualifies one earlier principle. Artifacts are the truth where an artifact exists. Where none does, the emitting process's observation is the record.
