# A component is a folder with its own tests and a published interface

**Status**: decided in October 2026; the merge rule came after. This ADR records decisions. The layout and the boundary tests are in use for new code. The nightly full run is being set up and does not run yet. Older code is still being untangled into components. [The glossary](../glossary.md) marks items that are design.

## Context

Before this decision, every change waited on the whole test suite. The suite ran about half an hour, because the code beneath it was tangled: a change in one place could break something far away, so the only safe evidence was to run everything. The wait fell on the Tech Lead, the Tester and the Owner alike, and it grew as tests were added.

Two things made it worse. Tests that need a real clock, a real process or a real file system are slow and fail for reasons unrelated to the change. And when a half-hour run fails, it says little about which change broke it.

## Decision

**New code lives in components. A component is a folder holding its packages, its own tests and its own way to run them.**

**A component is reached through its published interface and nothing else.** The interface is one module: the functions and data the component promises to others. Code outside the component does not read its internals or its files. A component imports its own packages, and the published interface of another component only from one small wiring module of its own, never anything deeper. A test enforces this at the boundary. The rule is general and applies to every store, adapter and view, not only to one component.

**Where the change touches only one component, the change merges on that component's tests.** A change merges on the component's own suite plus its boundary tests when every changed file is inside one component and the published interface is unchanged. A change to a published interface is treated as touching everything and runs the full suite. A small script decides, from the list of changed files, which suite a change must run, prints one line, and falls back to the full suite on anything it cannot classify or any error.

**Safety checks and tools keep the full suite.** Changes to the checks that guard what agents may do, the gate on model usage, the launcher and the factory's own tools, and anything outside a component, run everything. So does any change to a component that decides what counts as merge evidence, who reviews, or what an agent is permitted to do.

**A nightly run of the full suite on the main branch is meant to catch what the component suites miss.** When it fails on something a component suite passed, the fix includes a new test inside the component that broke, so that the component's own suite would have caught it. A miss becomes a test in the component where it belongs. The nightly run is being set up.

**Parallel workers shorten the runs that remain.** The full suite runs its test files on several workers at once. In one run, the full suite took 8 minutes 58 seconds in parallel and 30 minutes 7 seconds in series.

## Considered and rejected

- **The full suite on every change.** It is the safe rule and the one the factory started with. It put half an hour in front of every merge and told the reader almost nothing about the cause of a failure.
- **Detecting which other components use a changed interface, and running their suites.** A reviewer found the detection leaky. Treating any interface change as a full run is simpler, and a mistake there costs a longer wait, not a missed test.
- **Skipping the nightly run because the component suites pass.** The rule trusts the edges the components claim to have. The nightly run is how a wrong claim gets found.

## Consequences

- Seven changes merged under the rule in its first day waited between 0.7 and 2.8 seconds each. Three changes outside components waited for the full suite, 28 to 29 minutes each. The average wait per change was about nine minutes, against 27 to 29 before. Ten changes is not a sample. The figure depends on how many changes fit the rule, and some parts of the system will always need the full suite to judge whether they are good.
- A failing component suite points at one component and one change.
- The rule only works if it can be said, for each change, whether it stays inside one component. If it cannot, the change runs everything.
- Cutting the tangle is how more changes qualify. One shared library that the tooling imports went from about 1,100 lines to about 760 over three cuts, each moving a family of functions into a small module with no outside dependencies.
- The rule can be wrong. If the nightly run keeps catching misses on component-only changes, it goes back to the full suite for everything. The proposed threshold is two misses in the first ten component-only merges. It is a proposal and is not yet ruled.
