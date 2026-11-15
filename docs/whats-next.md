# What's next

The v0.1.0-skeleton tag is a [walking skeleton](../components/middle-path/README.md):
one runnable slice through story, packet, review and merge, with GitHub and the
agents faked. The v0.1.2-merge-gate tag added a typed review verdict and a pure
readiness decision to the package; [the verdict format](verdict-format.md)
describes them. The v0.1.3-extra-roles tag added optional extra roles to that decision, verdict provenance, and a pure carry decision. The slice does not call `readiness` or `carry`: it still merges through `decide`.

This page names the stages that come next and, for those the [vision page](vision.md) covers, says where each sits in its picture. It gives no dates, and a stage may change or move as the work teaches us something.

## In the package: one readable example test

The package has a single readable test file that runs the walking skeleton on in-memory stand-ins built by hand: a story goes in, the layers run in order, and a merge decision comes out. [The README](../components/middle-path/README.md) says how to run it. It sits under the testing bar on the [vision page](vision.md): behavior pinned by tests that someone who was not there can recheck.

## Next: the slice asks the readiness decision

The slice still merges through `decide`. A coming stage makes the slice ask the published `readiness` decision about the review before it decides on the merge, with the reviewers and roles supplied by the caller. It sits under the engineering bar on the [vision page](vision.md), where every change is reviewed by a model other than its author.

## Later: carry in the slice

A later stage may let the slice use `carry`, the pure decision already in the package about whether a second-role verdict could cross a merge of main ([below](#in-the-package-since-v013-extra-roles-extra-roles-in-the-review-decision) and [the verdict format](verdict-format.md)).

## Later: a checked registry

Today the caller supplies reviewer identity and roles. A checked registry of reviewers and roles is a later stage.

## Where the skeleton's merge step sits

| Step | In the package | Used by the slice today | Later |
| --- | --- | --- | --- |
| Review requirement | `readiness` (a pure decision) | no | the slice asks it before the merge decision |
| Verdict crossing a merge of main | `carry` (a pure decision) | no | the slice may use it |
| Merge decision | `decide` | yes | stays for the packet check, the single-verdict rule and the suite checks |
| Who may review | not in the package; the caller supplies it | caller | a checked registry |

This is not a schedule or a promise. It shows what is published and what the slice does not yet use.

## In the package since v0.1.3-extra-roles: extra roles in the review decision

The review decision takes an optional `ExtraRoles` input that can only raise the required roles. Verdicts carry their provenance: direct, or carried from a different head. `carry()` is a pure decision about whether a second-role verdict could cross a merge of main, based on facts supplied by the caller; it builds no verdict. The review rule is unchanged: one verdict per head.

## The review rules in public

The Tester's rules, a verdict template and the Tester's runbook now live in this repository (docs/tester.md, docs/templates/verdict.md and docs/tester-runbook.md).

## An operator record

The operator record is where a factory keeps track of its work. This stage adds the code that sets up its structure and adds and updates records. Each factory's own records stay private to it.

## One real pass

A Tech Lead, an Engineer and a Tester, all real agents, will take one piece of work through the flow once, in a straight line, and leave a record of the change. Later stages add what happens when work needs another round. The runs themselves are not public.

## What is not planned here

There is no auto-merge. A human decides every merge and install. As execution
matures, a seam is automated only after measurement shows it is safe; install
is the first candidate.
