# A component is a subcomponent, a sibling repository, or private, by stated tests

**Status**: decided in October 2026. This ADR records decisions. The publication scan, the history check, the classification table and the `components/KINDS` file described below are design, not yet built.

**Depends on**: ADR 0007 (components), which is already in this repository.

## The rule in brief

Every component is classified as exactly one of three kinds.

1. **Subcomponent of middle-path.** A folder under `components/middle-path/`, released with the factory, one version for all. This is the default.
2. **Sibling repository.** Its own repository with its own releases, pinned into middle-path at a named version. The pin mechanism is decided by a separate ADR that does not exist yet; no sibling moves before it does.
3. **Private.** Stays in the private workspace.

A component is a sibling when it is usable standalone AND (it has a second consumer OR a different cadence). Otherwise it stays a subcomponent. A component is private when its source, fixtures, defaults or data files contain, or point at, a workspace path, a private name or data that must not be public and the fix would change what the component is, or when its purpose is to run experiments on the workspace itself. The Owner reviews any claim of privateness.

Evidence is a command and its output, pinned at a commit sha. Prose is not evidence.

The tests, the evidence rule and the consequences follow in detail.

## Tests in detail

### Context

New code lives in components (ADR 0007): a folder with its own packages, tests and run script. New components arrive in this repository, the public home of the factory (the set of tools and gates that run delivery work); each component needs a destination. Three destinations exist, and nothing says how to choose between them. Without a rule the choice is made per component by whoever is closest to it, and the repository fills with things that do not belong together, or things never arrive.

In this repository, ADR 0007 already lets a component import another's published interface through one small wiring module. The classification of a component, and the evidence it rests on, are recorded when the component moves (see the evidence rule below).

### Decision

**Every component is classified as exactly one of three kinds.**

1. **Subcomponent of middle-path.** A folder under `components/middle-path/`, released with the factory, one version for all. This is the default.
2. **Sibling repository.** Its own repository with its own releases, pinned into middle-path at a named version. The pin mechanism is decided by a separate ADR that does not exist yet; no sibling moves before it does.
3. **Private.** Stays in the private workspace.

**A component is a sibling when it is usable standalone AND (it has a second consumer OR a different cadence). Otherwise it stays a subcomponent.**

- **Usable standalone (necessary).** A reader who has never seen the factory can install it, run its tests and use it for something, with no workspace path, no private name and no other component, apart from a published interface it vendors or pins, installed in the clean-checkout run. A component that cannot stand alone never becomes a sibling, whatever else is true: the pin would be the only contact with something nobody else can run.
- **Second consumer (trigger).** An EXISTING, named consumer outside the factory imports or implements the component, with a link to it at the time of the claim. A forecast ("someone would") does not count. Another subcomponent of middle-path never counts: the same release is the same consumer. A repository created to name a consumer does not count: the consumer must be maintained by someone other than the component's authors and use the component for a purpose of its own; shipping independently is not enough alone. A published specification counts only when all four hold: the specification is published; the component is its reference implementation and ships a conformance test that the specification's readers can run; a named, existing implementer other than the component's authors uses it; and the claim links to that implementer. A specification the factory wrote for itself, with the factory's own code as its reference implementation, is the factory's own consumer and does not trigger.
- **Different cadence (trigger).** The component's changes follow a different schedule from the factory's. Metric: over the same 60-day window, the component has at least two tagged releases and at least twice as many as the factory itself (subcomponents are released with the factory and have no tags of their own), or at most one fifth of the median change count per 30 days of the factory's other components; either way, with at least 10 commits on the busier side. Evidence is the change history, a command and its output pinned at a sha, never a forecast. The test needs 60 days of history: until a component has them, its row says "cadence: not yet testable", not "equal". Bursts of commits or quick tags made to fire the trigger, and freezes made to suppress it, are disregarded when the Owner judges from the history that the change was made for that purpose, and records the reason in the row.
- **Usable standalone, checked.** A row will record a clean-checkout run: the component installed outside the workspace (no workspace environment, no sibling components other than a published interface it vendors or pins, installed in that run) and its tests run, as a command and its output pinned at a sha. A part split off to stay private is judged with the component: if the tests or the use need it, the component is not standalone.

**A component is private when its source, fixtures, defaults or data files contain, or point at, a workspace path, a private name or data that must not be public and the fix would change what the component is, or when its purpose is to run experiments on the workspace itself. The Owner reviews any claim of privateness, which states the data or the purpose it rests on.** A component that fails only because a path is hard-coded is not private forever: the path becomes an input and the component is reclassified. Every classification will record the missing fix before a move, or "none". A component joins the public repository only with zero scan hits (any allowance will be listed in the move row and approved by the Owner); before a component moves, the scan will report and not fail; from the move on, it will fail.

**Evidence rule.** A classification will cite the check it rests on as a command plus its output, pinned at a commit sha: the import graph, the scan for workspace paths and private names, and the change history. Prose is not evidence, and a classification without a sha goes stale without anyone seeing it. A claim about a second consumer names the consumer. Every row will record its missing fix, or none.

**The publication scan is design, defined separately, and will run as part of each component's own checks.** Before a component moves, it will report and not fail. From the move on, a component classified as subcomponent or sibling will fail its checks if its tree contains a workspace path, a private repository name, a personal detail or a secret-shaped string (the classes will be defined with the scan). It will run on every change to the component, not only at release. A move is a reviewed pull request, not a direct push, and the scan result will be an input to that review.

### Consequences

- Moving a component between kinds is a reclassification with a stated reason, not a rewrite. The reverse also holds: a sibling whose second consumer or cadence difference disappears may be folded back, with a stated reason; the re-run described below is the trigger.
- A sibling needs a stable published interface (ADR 0007) before it leaves, because the pin is the only contact. Stable means no change to the published surface in the last 30 days; the Owner confirms it at the classification from the change history.
- Moving a component carries its history. The scan will read the tree, not history, so a separate history check must pass before anything is published.
- A component stays a subcomponent unless it passes the rule with a named trigger. The classification will be re-run at each 60-day mark, scheduled by the Owner, and whenever a move is proposed.
- `components/KINDS` does not exist yet; until it does, there is no record of kinds, and the first classification will create the table. Once KINDS exists (one `name kind` pair per line) it is the single record of each component's kind, and where the two differ, KINDS wins.
- A data file that carries private names or values (for example a list of private repositories read by a tool) is not published with the tool: it is untracked or injected at run time, and the move row will record that.
- The publication scan will be a command-line tool that component checks will call. A component imports another only through its published interface, from one wiring module of its own (ADR 0007).
- Deployment granularity is separate from repository placement and is decided by a separate ADR on deploy units, which does not exist yet.

### Considered and rejected

- **Everything a subcomponent.** Simple, but a component others could use would never be usable outside the factory.
- **Everything a sibling.** Cleanest boundaries, but one repository per folder multiplies releases, pins and reviews for components with no second consumer.
- **Any one of the three tests is enough.** Lets cadence or a second consumer alone move a component that cannot stand alone.
- **Classify by size or age.** Both say little about who uses a component or whether it can leave the workspace.
