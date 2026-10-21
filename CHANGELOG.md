# Changelog

Entries name what changed in this repository and nothing else.

## v0.1.1-docs, 2026-10-21

A documentation tag, published after the walking skeleton and after
v0.1.2-merge-gate, so its number is lower than the tag before it. Nothing here
is a supported version.

- README rewritten: what Middle Path is, the skeleton, what you can do with the
  repository today, the nine decisions, the case study and a list of what is not
  here yet.
- SECURITY.md added: what holds today, what does not hold yet, and how to
  report a problem.
- The vision, verification, lifecycle and security pages carry the review rule
  as one identical sentence: "Every change is reviewed by a model other than its
  author; security-boundary and other high-risk changes need two vendors; a
  review never passes for lack of capacity: the work waits." The lifecycle step
  is now named "Independent review", and the flows page uses the new name.
- The vision page says more plainly what is design and what holds today, and
  the verification page states the relaxation of review findings at class level.
- The vision page's "Where it stands" paragraph now says nine decisions are
  published; it said two.
- The README and the glossary's Merge-ready entry say, in the future tense, that R1.3 is planned to make the readiness decision authoritative.
- A `.gitignore` is added so running the skeleton's suite leaves a clean working
  tree.
- The other pages and ADRs 0001 to 0009 are as published before this tag.

## v0.1.2-merge-gate, 2026-10-20

The skeleton gains a typed review verdict and a pure readiness decision. The
ports package owns a frozen verdict, closed decision and role values, a rule
naming the required roles, and a head check that accepts exactly 40 lowercase
hexadecimal characters. The merge layer's review-readiness function decides whether the
review evidence at one head meets the rule, with a closed set of reasons. The
earlier synthetic merge result is renamed. GitHub and the agents are still
faked. It is not a supported version.

## v0.1.0-skeleton, 2026-10-20

First code: a walking skeleton in `components/middle-path/`. A story (the input for one
change) becomes a packet (the checked unit of work), opens a work record, gets a build, a pull request, one review verdict,
a suite result and a merge decision, and the record closes as done or as
abandoned with a reason. GitHub and the agents are faked. Run
`components/middle-path/run-suite` to see it pass. It is not a supported
version.

## Before v0.1.0-skeleton

Documentation was published in three batches, from the first decisions to the
round-cap decision. The glossary, roles, vision, lifecycle, flows, methods and
verification pages were part of them.
