# Middle path walking skeleton

Run `components/middle-path/run-suite` from any directory using its absolute
path, or run `./run-suite` here. Python 3.11 or later and pytest are required;
production packages use only the standard library. Each nested directory has
its own package, tests and standalone `run-suite`. The aggregate runs ports,
story, packet, review, merge and slice exactly once, prints each exit code, and
returns the first nonzero code after all six finish. A missing runner is also
a failure, and later runners still run.

The path is story -> packet -> work record OPENED -> build -> review verdict
-> merge decision -> work record CLOSED. The four pure layers expose
`mp_story.load`, `mp_packet.build`, `mp_review.collect` and `mp_merge.decide`.
Only `slice/mp_slice/wiring.py` imports sibling layers and constructs the
injected `Layers` value. The driver consumes those functions' returned values;
it does not reconstruct their decisions. `mp_ports.__all__` is the published
seam for frozen values, three protocols, in-memory adapters and reusable
contract cases. The tests guard both production and test imports.

Each standalone runner sets its own package root and the ports root on
`PYTHONPATH`. Slice additionally needs the story, packet, review and merge
roots for wiring; its conftest makes those same four roots visible. Test-only
examples and AST helpers live in `ports/tests` and are exposed by each
conftest. No production package imports them. The architecture helper is
named `check_tests_pure` so pytest collects only the explicit entrypoints.

Records, Forge and Agents are strict in-memory fakes. Records uses optimistic
versions, refuses duplicate ids and every write after close, and exposes
immutable history. Forge records issues, PRs and verdicts, then atomically
compares the expected head before merging. Agents returns canned build and
review evidence keyed by packet id, refuses unknown ids, and records full
arguments. They share an `EffectLog` so tests can compare effect order across
ports. The clock is an injected callable; there is no network, real agent,
vendor SDK, random id generator or production subprocess.

Readiness checks fields in this order: id, title, why, acceptance, risk_tier.
The first failure wins. Only medium tier is supported; light and heavy refuse
with `tier-unsupported`. Missing, empty (including whitespace) and wrong-type
fields have closed reasons. Malformed input and extra fields refuse with
`wrong-type:raw`. One nonempty acceptance line is sufficient. Packet adds the
supplied base SHA and requires exactly one verdict. No record or external
effect exists before readiness passes.

The merge policy is a synthetic single-reviewer policy at medium risk tier. It requires one
MERGE verdict at the PR head, a suite with exit zero at that same head, a valid
packet, and no open blocker. Zero verdicts, surplus verdicts in either order,
AMEND, missing evidence and stale evidence each refuse by name. It is a
deliberately small stand-in: it does not check which model family reviewed,
whether the reviewer is the author, or how the review was launched. Fixtures
keep builder and reviewer identities distinct, but nothing enforces it. This
slice shows the shape of the architecture. It says nothing about how any real
vendor's agents behave.

The returned Trace starts with `story-received` and `packet-ready`. Persisted
history starts at `record-opened` and carries the story id, canonical packet
digest, heads, evidence and decision. A successful record closes once with
reason `done`; refusals and supported failures close once with reason
`abandoned` and a separate detail. Adapters report expected failures through
the public `AdapterError` base with a stable `reason`; `ForgeRefused`,
`AgentsRefused` and `RecordsRefused` inherit it and retain their reasons.
Build and review catch only `AdapterError` and retain `build-failed` and
`review-failed`. Issue and PR creation failures close with `issue-create-failed`
and `pr-create-failed`, without further build, review or merge calls. Verdict-post and merge
refusals retain their named details. A refused close returns a Trace with
`close-refused` and no `record-closed` step; the adapter's record state remains
as it left it, and close is never retried. Other exceptions propagate after
one abandoned close attempt with detail `unexpected-error`.
Steps present in both histories write the Records event before the Trace note;
`verdict-recorded` remains Records-only, preserving the successful histories.
The decision uses the reviewed head snapshot;
the current head is also observed at decision time and Forge refuses a moved
head at the conditional merge. Both movement timings are tested. A replay
uses the story id again and refuses without new Forge or Agents activity.

Vocabulary: a story is the readiness input; a packet is the
readiness-checked per-change unit containing the story and base commit; a work
record is its versioned event history; a verdict is review evidence; a head
is a commit identifier; suite exit is the test process result. A subcomponent
is one nested package/test/runner unit.

The six architecture entrypoints assert their nonempty source inventories,
reject sibling and neighbouring-component imports, and guard source and test
purity. Subprocess is allowed only in the disposable wrapper tests. Port
contracts have collected `test_contract_*.py` entrypoints; future adapters can
run the same cases through their own factories. Binding to a real
record store is not part of this slice.
