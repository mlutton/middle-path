# What's next

The v0.1.0-skeleton tag is a [walking skeleton](../components/middle-path/README.md):
one runnable slice through story, packet, review and merge, with GitHub and the
agents faked. The v0.1.2-merge-gate tag added a typed review verdict and a pure
readiness decision to it; [the verdict format](verdict-format.md) describes
them.

This page names the stages that come next. It gives no dates, and a stage may change or move as the work teaches us something.

## Now in the package: extra roles in the review decision

The review decision takes an optional `ExtraRoles` input that can only raise the required roles. Verdicts carry their provenance: direct, or carried from a different head. `carry()` is a pure decision about whether a second-role verdict can cross a merge of main, based on facts supplied by the caller.

## The review rules in public

The rules for how a change is reviewed and tested, along with the Tester's runbook and templates, will move into this repository. The factory will then use these copies.

## An operator record

The operator record is where a factory keeps track of its work. This stage adds the code that sets up its structure and adds and updates records. Each factory's own records stay private to it.

## One real pass

A Tech Lead, an Engineer and a Tester, all real agents, will take one piece of work through the flow once, in a straight line, and leave a record of the change. Later stages add what happens when work needs another round. The runs themselves are not public.

## What is not planned here

There is no auto-merge. A human decides every merge and install. As execution
matures, a seam is automated only after measurement shows it is safe; install
is the first candidate.
