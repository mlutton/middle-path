# The round cap is a sensor for weak design

**Status**: the cap was set in early October 2026 and given its purpose in the same month. Builds on [ADR 0005, review depth](0005-review-depth-is-chosen-by-what-the-subject-can-damage.md). This ADR records decisions. The cap and the re-review rule are practices, and no script judges whether a run of findings belongs to one family. [The glossary](../glossary.md) marks items that are design.

## Context

A change can fail review again and again. Each round finds something real, the Engineer fixes it, and the next round finds something else. Reviewers are right every time, so nothing in a single round says the process has gone wrong.

Two rules were already in place. A re-review checks only what changed since the last verdict, and new findings outside that change are parked unless they cannot be undone or have no bound on how bad they can get. And rounds are capped by risk tier, which is how reversible a change is and how large its worst case can get, at two, three or four rounds. At the cap, the work stops for a decision by the Owner, and the Tech Lead writes down the one assumption every failed fix had in common.

The question this ADR answers is what the cap is for.

## Decision

**The cap is a sensor for weak design.** It does not stop anyone from fixing a real finding; it flags a change that keeps failing review. When rounds keep finding new edge cases of the same family, the change is being patched where it should be redesigned, a pattern that is called whack-a-mole. Reaching the cap is the signal to step back and redesign instead of patching.

**At the cap, the response is a design change, and the next step must make the change smaller or simpler.** Two moves have worked: reduce what the change has to promise, so the cases that kept appearing stop being cases, or cut the change down to a narrow core and write its tests first.

**The assumption every failed fix shared is written down.** In one case, each fix had assumed that a new rule for a permission could be judged as simply looser or stricter than the old one. The real question was what each rule decides in every mode. An illustration, not the actual rule: say the old rule denied writes in every mode, and a fix rewrote it to deny writes and reads in the default mode. It looks stricter, since it blocks something new. But it no longer denies writes in the other modes, so those writes are now allowed. "Looser or stricter" has no single answer there, and "what does each rule decide in each mode" does. Naming the shared assumption is how a redesign finds its question.

**The cap earns its place only if it works.** It works if hitting it leads to a design change that ends the loop: the next review comes back clean, or the change gets smaller. If the factory hits the cap and keeps patching, or a redesign does not stop the findings, the cap is rethought.

## Evidence so far

Of sixteen recent changes, fifteen have a known round count. Fourteen took two review rounds or fewer, and one took five.

In one week, three changes hit the cap:

- A tool that picks which tests a change runs was given a simpler requirement. It stopped trying to detect who uses a changed interface and treats any interface change as needing the full suite. It passed review one round later, after an unrelated fix.
- A refactor that had failed three reviews was cut down to a narrow core, with tests that pin the current behavior written first, and passed its first review after that.
- The third went to the Owner for a design decision, because each redesign closed one family of findings and the next review found another. After the Owner's decision it took two more reviews, the first of which found only two test assertions that had been loosened, and it merged.

Three cases are not a sample.

## Considered and rejected

- **No cap, with rounds continuing until review is clean.** One change took five rounds, and every round found something real. A rule that only ever asks for one more round does not ask whether the design is the problem.

## Consequences

- A change that keeps failing review is treated as information about the design, and the shared assumption is looked for before another patch.
- The Owner's decision at the cap is a design decision, not an approval of the fix.
- The cap can be wrong. If it is reached often and redesign does not help, it goes.
- The practice relies on the Tech Lead noticing that rounds belong to one family. That judgment is not yet automated.
