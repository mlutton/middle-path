# How the private factory plugs into Middle Path

Middle Path is a kit for running a software factory. This repository holds the
kit's public part. The private factory that built the kit, and that uses it day to day,
is a separate setup, kept outside this repository. This page says how the two relate, and only what
this repository's code does.

## What this repository contains today

<!-- facts-block:start (generated; do not edit by hand) -->
Tags, in the order they were published: v0.1.0-skeleton, v0.1.1-docs, v0.1.2-merge-gate, v0.1.3-extra-roles.
Packages in `components/middle-path`: ports, story, packet, review, merge, slice.
Published seam: `mp_ports.__all__` (the list of names is generated from the package).
<!-- facts-block:end -->

Each package does one job:
- **ports** holds the shared frozen values (verdicts, rules, heads, readiness results), the closed sets of decisions and roles, the protocols, and in-memory stand-ins.
- **story** loads a story.
- **packet** builds a packet from a story.
- **review** collects review verdicts.
- **merge** decides readiness from verdicts and makes the merge decision.
- **slice** wires the other four together and drives one walk through the flow.

All of it runs with fakes in place of GitHub and of the agents. The
[what's next](whats-next.md) page lists the stages that are not built yet.

## The private factory

The private factory is the setup that uses Middle Path. It consumes the kit.
Over time, more of what the private factory does is meant to move into Middle Path.

## What lands in Middle Path and what stays separate

The exact setup of the private factory, and the information about its state,
stay separate from Middle Path. Refinements to both Middle Path and the private
factory go through an internal process, with its own internal GitHub repository,
before they are pushed to Middle Path.

## The one boundary

A package is reached through its published interface and nothing else
([ADR 0007](adr/0007-a-component-is-a-folder-with-its-own-tests-and-a-published-interface.md)).
Here, the shared values and protocols live in `mp_ports`, and only the slice
package's wiring module imports the other packages. Anything that uses Middle
Path, the private factory included, goes through those published names and
reads nothing else of the package.

## What this page does not say

It does not say which parts of the private factory run on Middle Path code, which
version of Middle Path any factory runs, or how any factory is set up inside.
Those are each factory's own business and are not recorded here. Nothing in this
repository enforces extra roles or any other rule on a factory; a caller
decides what it passes in.
