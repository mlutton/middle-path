# Required SDLC methods

These are task methods: documents that are read and applied, not tools to
install or invoke. The table says what must be read **before** the relevant
decisions or edits.

Related decisions: [the factory's objects and roles](adr/0001-the-factorys-objects-and-roles.md)
and [audience and the two doors](adr/0002-audience-and-the-two-doors.md).

## Select by activity

| Activity | Required reading | Evidence in the existing artifact |
| --- | --- | --- |
| Planning implementation, refining a Specification, or choosing interfaces and test seams | Codebase design; also Deepening when evaluating a cluster or its dependencies | Implementation and Verification Decisions identify the chosen interfaces/seams, complexity hidden from callers, dependency strategy, and rationale. For a small change, state how the existing seam suffices. |
| Exploring alternative interfaces when the task calls for alternatives | Design It Twice, with the design and deepening references | Compared alternatives and the reason for the selected design. This branch is not required for every plan. |
| Implementing or changing behavior with an observable red state | The existing TDD reference, its test examples, and its mocking guidance | The packet names the agreed seams. The handback maps behavior to tests, independent expected-value sources, and observed failing/passing runs, using `<self_check>` and `<red>`. |
| Writing or editing agent-facing instructions: entry files, packets, role cards, skills, or referenced guidance | Writing for agents; also Skill mechanics for skill packaging | The handback or author review identifies trigger/pointer changes, checkable completion criteria, and the authoritative home for changed rules. Existing satisfactory elements may be named as such. |
| Verifying any of the above work | The same selected method files and local adaptations supplied to the author/Engineer | The verification plan names applicable expectations and evidence; findings cite those expectations and distinguish observed evidence from claims of method use. |

Read each selected document in full. Supporting documents are conditional only
where the table says so. A skill name in a packet or a claim of invocation
does not establish that the method was followed.

The design, writing and TDD methods above are adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT licensed).
The method documents themselves arrive in a later slice, with their license.

## Apply within the protocol

The aligned Specification, packet, project glossary, and governing ADRs retain
their authority. These references supply methods within that scope:

- TDD uses the seams already agreed during the design round; existing
  authorization satisfies the reference's request to confirm seams. A missing
  or conflicting seam is a readiness gap, routed to the Tech Lead.
- Engineers apply one test/implementation slice at a time, through the agreed
  interface, with independently grounded expected values. The full TDD
  reference and its support files govern this work, beyond merely observing
  red before green. Documentation, configuration, or pure moves with no
  meaningful red state use the packet's stated validation instead.
- A planning heuristic cannot overturn an ADR, rename canonical domain
  vocabulary, expand scope, or authorize a refactor or deletion. Surface a
  conflict in the existing decision process. Engineer refactoring
  remains subject to the vendored TDD adaptation and role separation.
- Skill mechanics describes the source runtime's packaging conventions. Use
  the target runtime's supported metadata; reading shared reference text
  does not invoke another skill.
- Testers assess declared expectations, with correctness against declared
  standards and against the specification separately identifiable in their
  report. A generic design suggestion without a declared expectation is
  non-blocking feedback, never a new blocking requirement. Verification
  remains a separate session.

## Deliver the text to every role

A packet is the brief a round receives; its sections are named with
XML-style tags such as `<read_first>` and `<done_means>`.

The packet author selects the methods before the design round and states
their application and expected evidence in `<done_means>`. The Tech Lead
supplies those same expectations and references to the
verification-plan run.

A product worktree need not contain the orchestration repository. For a
round, the Tech Lead stages unchanged reference files from a committed
orchestration revision, preserving their original relative paths and links,
while keeping dispatch inputs outside the deliverable.

Stage this document, the selected method files and applicable supporting
files, and their provenance and license record. List **each required read**
explicitly in `<read_first>`, after the project's shared instruction file;
declare provenance/license files in `<reference>`. Include any project
glossary/ADR that the selection requires among the allowed resources. Every
reference the agent must follow must be declared and available: a filename
mentioned only inside another document does not extend a closed resource set.
If an unexpected branch requires another document, return a resource gap.

Record the source repository and commit, delivered file paths, and SHA-256
digests in the packet's existing `<constraints>`. Copy that selection and
those bytes into the Tester's fresh session. Each reader checks the
delivered digests before using the methods and lists consulted paths in the
existing `<used>` field (or verification record); mismatches are input gaps.
Record applicable method deviations in `<deviations>` through the existing
sign-off process, reusing authorization already in force.

The packet's pins make the committed sources retrievable with the round.
When those sources will not remain available, the Tech Lead also archives the
delivered files with the private round evidence; nothing copies this bundle
automatically yet. Keep private packet context in its existing
audience; source references do not authorize publishing it.

These are explicit role instructions. Brief checks are intended to validate
declared paths and skill names, and handback checks are intended to validate
shape; they do not prove reading, digest comparison, or semantic adherence.
The Tester supplies that assessment using the work and its evidence.
