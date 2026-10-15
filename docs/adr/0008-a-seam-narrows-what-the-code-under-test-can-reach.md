# A seam narrows what the code under test can reach

**Status**: decided in October 2026, from an Owner ruling made while the factory's test time was being worked down. Builds on [ADR 0007, components](0007-a-component-is-a-folder-with-its-own-tests-and-a-published-interface.md). This ADR records decisions. New components are written this way; older code is being moved toward it, and [the glossary](../glossary.md) marks items that are design.

## Context

A test that needs a real clock, a real process or a real file system is hard to write, slow to run and easy to break. In one stretch, eighteen test failures came from nothing but real process launches. The usual reading is that those tests need better waits or better machines.

The reading adopted here is that a hard-to-write test is information. It says the shape of the code under test is wrong: the code reaches too much, so the test must set up all of it. The cost shows up in review wait time, because a wide test is slow to run and slow to trust.

An earlier attempt went the other way and tried to predict when a small local model, used as a cheap first-pass reviewer, could check code. A rule that picked out answerable questions by their shape had to be at least 70% precise on held-out cases, a bar set in advance, and it was not. The rule was dropped, and analyses of code shape such as nesting and function length produced no rule either. What survived is narrower and about tests: a precondition that lives only in someone's head cannot be verified by anyone, so shape the code before anyone has to check it.

## Decision

**Use a seam to narrow what the code under test can reach.** A seam is a place where the real thing and a stand-in can swap. Its purpose is the narrowing: the test sets up less, and the code has less surface and less complexity. Faster tests follow from it.

**Write the simplest thing that passes the test.** A wide seam leaves gaps, and the gaps get covered one edge-case test at a time. Those tests make real system calls that wait, and the suite slows. A tight seam needs fewer tests and fewer system calls. A test that is getting hard to write is the signal to narrow the seam first.

**Tests check the factory's own logic with the operating system faked, and a few end-to-end tests check the assumptions about the real one.** Signals, locks and file renames stay real where the real behavior is what is being checked.

**Time is injected.** Code that depends on the date takes a clock as an argument. Tests do not move the system clock.

**The direction is a functional core inside an imperative shell.** The decision is a pure function, checked with a table of inputs and the verdict each should produce, and only a thin shell touches files, the clock or processes. This is a known pattern, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) (Gary Bernhardt, 2012). Business rules are written as pure functions from a request and the current state to new state or a refusal, and I/O stays at the edges.

## An example, and how far it goes

A component that checks whether a periodic heartbeat is still alive was written with the seams from its first commit. It takes the current time as an argument, and keeps its saved position and its alert record behind two small interfaces. In production those are files, and in tests they are small in-memory classes. A test for "the last tick is three minutes old and the limit is two" needs no sleeping, no files and no process, and the component's tests run in about two seconds.

It is only partway to the functional core. Its time and storage are injected, but its decision is still mixed in with the writing of alerts, so its tests are scenarios, not a table. Separating the decision is the next step and the direction for new components.

A smaller case: one test file for a tool that checks whether an agent session can be closed got faster when fixed sleeps were replaced by a short poll for the exact process the test was waiting on.

## Considered and rejected

- **Predicting when a model can check code, from the shape of the question or of the code.** The question-shape rule missed its bar, and the code-shape analyses produced no rule.
- **Tests that move the system clock.** An earlier retrospective replaced them with an injected clock.

## Consequences

- A test that is hard to write sends the reader to the code's shape first.
- Review gets cheaper for every reviewer, human or model, because a narrow piece of code has less to check.
- The seam is one more promise to maintain. A seam wider than it needs to be loses the benefit, and a stand-in that drifts from the real thing makes tests pass for the wrong reason, which is why a few real tests stay.
- The gain is hard to measure. The time a change waits fell after this work, but other changes landed at the same time, so no number here is credited to the seams alone.
