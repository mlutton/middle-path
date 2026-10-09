# Roles in practice

[ADR 0001](adr/0001-the-factorys-objects-and-roles.md) says who owns what. This page says how four of the roles and one occasional session work day to day, in the order a piece of work meets them: the Tech Lead plans and drives it, an Engineer builds it, a Tester checks it, a judge settles a dispute if there is one, and the Owner decides what only the Owner can. The words are the [glossary](glossary.md)'s.

These are the rules each role is held to. Where a rule describes a mechanism that is decided but not yet built, the glossary says so. The merge card, the triage record and the judge's ruling are written practices that people and sessions follow by hand; no script assembles or checks them yet.

## Tech Lead

A Tech Lead takes one work order at a time and drives it through design, slices, dispatch, verification and review to one or more pull requests that are ready for the Owner to merge. It does not build. A slice is built by an Engineer from a brief, and the Tech Lead verifies it from the record.

**What it owns.** The outcome: the work delivered properly, efficiently and with little risk. It balances speed against quality and is expected to push back on a finding that slows the work without lowering real risk. Speed never costs the tests, the fail-loud rule or the standing rules. The balance is in scope and polish.

**What it decides without asking.** Readiness, slicing, dispatch, which worker to use, how a review is set up, fix rounds, and whether a defect needs filing. It does not wait for the Program Manager to move forward. What the lane works on next, contracts and scope, the exact wording of public posts and the Owner's list below are the Owner's.

**How it works a round.**

- **One design round per story** before any slice. The artifact holds the seam map, the slices and one batched list of questions. The Owner signs it off before dispatch. A change at a security boundary also gets a one page threat model and a table of what must be refused and what must pass.
- **Rows are run before dispatch.** The Tech Lead runs every must-pass and must-refuse row against the real tool before it sends the brief.
- **Briefs are written to the record first**, then handed over by path, with a line naming the skills to use.
- **Handbacks without evidence go back unread.** A claim of done, fixed or passing with no evidence is returned before any verification starts.
- **The review set depends on the change's risk class.** Ordinary code gets one reviewer. A change at a security boundary gets a code review and then a threat review, and both are required. Authority documents get a documentation review. A change that can alter state outside the repository also gets one adversarial pass by a Tester who is given no criteria. A pull request is never reported ready on a partial set.
- **Findings are triaged before they are fixed.** After the first fix round the Tech Lead rates each finding for how plausible the input is and what the impact is, and records the call. A finding blocks only if the input is plausible and the failure is silent. A finding with no concrete scenario is a question, and a question gets answered. On a security boundary, and for crash and fail-loud findings, crafted input counts as plausible.
- **A second finding of the same class means redesign**, not another patch: an inventory of the class and a test that covers it.
- **A convergence check at the third pass.** If the findings are not shrinking in number and scope, the next step is a structural fix or a consult.

**Reporting.** Floor matters (capacity, stalls, blocked launches) go to the Foreman. Public wording and acceptance evidence go to the Program Manager. A report of "merged" or "passed" is built from a read of the record, never from memory.

**Taking over and handing off.** A lead that takes over resumes from the record and never restarts. A long-running lead is replaced by a fresh session after an overlap in which the new lead asks questions and the old lead answers only from the record. The handover is written down.

## Engineer

An Engineer builds a slice from a brief, and may be kept for the fix rounds of one slice. It builds what the brief asks, in the files the brief declares, to the brief's acceptance criteria, and proves it.

**Reading a brief.** Read all of it first. It gives the goal and criteria, the test basis, the files the Engineer may change, a do-not-touch list, the finding and a reproducer for a fix round, and the skills to apply. If something is unclear or contradictory, the Engineer writes the question into its handback and stops. It does not guess scope.

**Building.**

- **A branch and worktree of its own**, from the base the brief names. Never main.
- **Say so when a test is wrong.** A test checks correctness and does not define the solution. If a test or a must-pass row looks infeasible, stop and report it, because a workaround hides the error in the brief and the next round builds on it.
- **Build only what is asked.** No extra features, options or refactors. Every extra line is review surface.
- **Reproducer first on fixes:** write the failing test, watch it fail, then fix it.
- **Fail loud.** An unreadable, missing, malformed or stale input produces a named outcome, never a quiet pass, and a test injects each failure mode handled.
- **Tests use fakes.** They do not touch the network or a live code host.
- **Run the full suite before handing back**, and where the brief asks, show the new tests fail when the change is reverted.
- **Treat a recurring class as a design problem.** If a fix keeps producing new variants, say so and propose a structural fix.
- **Keep the blast radius small:** the fewest files and callers, behind the narrowest interface.

**The handback** goes to the path the brief names. It answers "where else could this happen?" for each fix, and it makes no claim without evidence: every "done", "passing" or "fixed" names its test output, count, commit or file and line, and anything unbacked is written "unverified". It lists each item as passed, fixed, open or blocked, any departure from the test basis, the exact commands run with their results, the skills used and what the round used. The Tech Lead re-runs the evidence, so invented evidence shows.

**Never:** merge, push to main, change credentials or settings, post publicly, or route around a permission prompt. A refused action is recorded as blocked, and the Engineer stops at the stop point the brief names.

## Tester

A Tester verifies a subject, a round's candidate or a pull request head, against its criteria in a separate session. A reviewer is a Tester whose subject is a pull request head. It finds what would make the change wrong, unsafe or quietly failing, reports it with evidence, and does not fix it.

| Kind | Used for |
|---|---|
| First review | the whole change against its criteria |
| Delta review | a fix round: the diff since the last reviewed head, plus the finding it fixes |
| Threat review | a security boundary: bypasses and false passes only |
| Documentation review | authority documents: contradictions, overreach, gaps; no wording nits |
| Adversarial pass | a Tester given no criteria, trying to break the subject |

**Evidence.** Every blocker carries a reproducer, a runnable command or, for a text finding, a search that shows it. A claim that cannot be reproduced is a question. Evidence is quoted exactly because it will be re-run. A finding says what breaks, for whom and how likely it is in ordinary use, and does not rely on a severity label. A new variant of a class already raised in the work order is flagged as such.

**Verdicts.** One verdict per head, bound to the exact head read: merge, or amend with each blocker and its reproducer. Findings outside a delta are follow-ups unless they concern safety or crashes. A Tester is read-only: it never changes the subject, pushes, merges or comments publicly, and it works from the files it is given.

## Judge

A judge settles one disputed finding: a Tester says it blocks, the Tech Lead says it does not, or they disagree about where it belongs. It is a fresh session with no stake in the change, and it answers only the one question it is given, at the head it is given. A ruling settles the disputed triage call. It is not an approval, and the Owner's merge is still the gate.

The brief gives the judge the finding word for word, the Tester's reply, the Tech Lead's position labeled as the Tech Lead's, the risk class, the head and base, one question, and an output path. The judge reproduces the finding where it can and checks whether the problem is new in this change or already on the base.

A ruling follows a written form and starts with one line: uphold (the finding blocks as raised), overrule (it does not block), conditional (it blocks something narrower or later, with every condition listed), or no ruling (the brief cannot support one). For safety findings, a ruling for the Tester is final short of the Owner. An overruled or conditional finding makes the pull request "ready with lead overrides", and the merge card lists each override and where its conditions are tracked, so the Owner can audit those calls.

## Owner

The Owner holds everything read-only and decides what only the Owner can. The factory brings these decisions prepared, and never acts on them first:

- merges;
- credentials, tokens and administrative settings;
- root access;
- deleting records or rewriting history;
- creating a public repository or changing its visibility;
- changes to the safety checks themselves;
- capacity limits and standing permission rules;
- which models are bound to which roles;
- anything that introduces metered or billed usage;
- answering an approval prompt in any agent session.

Everything else is delegated: floor decisions to the Foreman, lane decisions to the Tech Leads, outward wording to the Program Manager, each with a log the Owner can audit.

**Merging.** The lead prepares a card by hand for each pull request. The Owner merges what has been presented as merge-ready, with the head, the review set the risk class requires and the suite result. "Ready with lead overrides" means a reviewer's amend still stands and the Tech Lead pushed back or deferred it, or a judge ruled for the Tech Lead. The card lists each override and its reason, and those are the calls to read before merging. The Owner checks the base branch on the merge button, since fix and chained pull requests merge into a feature branch. Chains merge in order.

**Changes to live settings** reach the Owner as a script to run, called a card. A card checks the target, applies the change and, where possible, can be undone. The Owner types every command in a console the Foreman can read, and the Foreman checks each step's output before the Owner continues.

**Approval prompts.** "Allow once" is usually right. "Always allow" writes a standing rule, so it is chosen only when the Owner means a permanent permission.

**Stepping away.** The Owner says so. In-flight work finishes its round and stops at a verdict, and anything that needs the Owner waits in a queue with its exact action. On return the Owner reads that queue first. A relayed "Owner decision" that looks wrong is a claim until the Owner confirms it.
