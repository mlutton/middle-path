# Review depth is chosen by what the subject can damage, and an adversarial arm is not given the acceptance criteria

**Status**: decided in September 2026, after three defects reached a pull request. Builds on [ADR 0001](0001-the-factorys-objects-and-roles.md). The adversarial arm is a working practice followed by hand. No script selects it or checks that it ran.

## Context

A command in a product the factory was building passed alignment with two reviewers, an independent verification round that found and fixed a real defect, and a fix round. At the Owner's review, an adversarial pass found three more defects in an hour, each confirmed by running it:

- one failing step abandoned every other step and lost the whole report, after a change record had already been written;
- a symlinked target was hashed from outside the intended directory and committed as true;
- a temporary-file guard checked one path and then deleted another, destroying a file the command did not own.

The verification round was neither lazy nor late. It ran the product end to end and found a real defect. It missed these three because it was asked a different question. A Tester given the brief's acceptance criteria asks whether the work does what the criteria say. The adversarial pass was given the subject and no criteria, and asked what else the work does. All three came from inputs the criteria never mentioned, so nothing checked them.

The factory had already recorded the same finding at other levels: a brief whose criteria asked whether refusals write nothing and never asked whether a measurement the tool cannot make is reported as a number, and a finding that stated a remedy instead of the property it violated. Criteria under-ask, so the failure cannot be fixed by writing better criteria. A longer checklist has the same blind spot, because the person writing the criteria and the person missing the case are the same person.

## Decision

**Review depth is chosen by what the subject can damage, and the choice is made before dispatch from a property anyone can check.**

**A round whose subject changes state outside the repository gets an adversarial arm in its verification round.** The test is decidable. A change that archives a file the launch script already writes does not qualify. A command that deletes files, rewrites a user's documents and makes commits in their workspace does.

**The adversarial arm is not given the acceptance criteria.** It receives the subject, the seam it runs at, and the classes of hostile input worth trying. If it reads the criteria it inherits their blind spots, which is the failure being addressed, and an arm given the checklist is a second Tester. This is the one rule here that must not be softened for convenience.

**It reports and does not gate.** Its findings go to the Owner's review like any other, and the usual round budgets decide what a round costs. It is a second question asked of the same work, not a second approval.

## Considered and rejected

- **Better acceptance criteria.** This was the proposed fix each of the three times the same gap was diagnosed.
- **An adversarial arm on every round.** A round that edits a docstring or adds a test has nothing for it to find, and running one everywhere teaches everyone to skim the result.
- **Waiting for the Owner's review.** It works, and it works at the worst moment: after the round is closed, its retrospective is written and its pull request is open.
- **A checklist of hostile inputs in the brief.** That is criteria in a different hat, and it tells the arm what to look for.

## Consequences

- A class of defect becomes findable before a pull request. All three defects above were containment defects, meaning the command touched something outside what it was pointed at. A nameable class is also a candidate for a reusable harness. Where a harness can express the class, it outranks the arm, because code ranks above judgment. The arm earns its cost on what a harness cannot express.
- Verification cost rises for rounds that change state outside the repository.
- The selection rule will be wrong somewhere. It keys on damage, and damage is not always outside the repository: a change that corrupts the record damages the instrument every other decision is read from. The factory records which rule it applied, and why, whenever an arm is or is not run, so the rule can be re-derived from cases.
- Findings are meant to be recorded with a disposition (rework, use as is, defer or scrap), attached to the work order, and a round is not to close with a finding that has none. That part is design.
