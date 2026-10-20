"""observable path through real wiring and strict fake ports."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
from mp_examples import PACKET, RAW, STORY, readiness_cases
from mp_ports import (
    AgentsRefused,
    BuildResult,
    Decision,
    MergeDecision,
    EffectLog,
    ForgeRefused,
    MemoryAgents,
    MemoryForge,
    MemoryRecords,
    Refusal,
    ReviewResult,
    Role,
    SuiteReport,
    Verdict,
)
from mp_slice import run
from mp_slice.wiring import layers

H1 = "a" * 40
H2 = "b" * 40
GREEN_VERDICT = Verdict(Decision.MERGE, H1, "reviewer-example", Role.PRIMARY)
GREEN_SUITE = SuiteReport(H1, 0)
TRACE = ("story-received", "packet-ready", "record-opened", "issue-created",
         "build-requested", "build-returned", "pr-created", "verdict-posted",
         "suite-recorded", "merge-decided", "record-closed")
HISTORY = ("record-opened", "build-requested", "build-returned", "verdict-recorded",
           "suite-recorded", "merge-decided", "record-closed")


def setup(verdict=GREEN_VERDICT, suite=GREEN_SUITE, forge_type=MemoryForge,
          agent_type=MemoryAgents):
    log = EffectLog()
    records = MemoryRecords(log)
    forge = forge_type(log)
    agents = agent_type(log, {"S-001": BuildResult(H1, suite)}, {"S-001": verdict})
    return log, records, forge, agents


def drive(state, raw=RAW, base="base-0", composition=None, tick="tick-1"):
    _, records, forge, agents = state
    return run(raw, base, layers=composition or layers(), records=records,
               forge=forge, agents=agents, clock=lambda: tick)


def calls(log, port, operation):
    return [entry.arguments for entry in log.entries
            if entry.port == port and entry.operation == operation]


def assert_abandoned(state, trace, detail, attempts=0):
    log, records, forge, _ = state
    history = records.history("S-001")
    assert trace.outcome == Refusal(detail)
    assert history[-1].step == "record-closed"
    assert dict(history[-1].payload) == {"reason": "abandoned", "detail": detail}
    assert len(calls(log, "records", "close")) == 1
    assert len(calls(log, "forge", "merge")) == attempts
    assert forge.merges == []
    print(f"abandoned detail={detail} closes=1 merge-attempts={attempts} successes=0")


def test_happy_path():
    raw = json.loads((Path(__file__).parent / "fixtures" / "story.json").read_text())
    state = setup()
    trace = drive(state, raw)
    log, records, forge, _ = state
    assert trace.steps == TRACE
    assert trace.outcome == "MERGE"
    history = records.history("S-001")
    assert tuple(e.step for e in history) == HISTORY
    common = {"story_id": "S-001", "packet_digest": PACKET.digest}
    assert [dict(e.payload) for e in history] == [
        common, common, {**common, "build_head": H1},
        {**common, "verdict_head": H1, "kind": "MERGE"},
        {**common, "suite_head": H1, "suite_exit": 0},
        {**common, "head": H1, "observed_head": H1, "decision": "MERGE"},
        {"reason": "done", "detail": "MERGE"},
    ]
    assert forge.issues == {1: (STORY.title, PACKET.body)}
    assert forge.prs == {1: (1, H1)}
    assert forge.verdicts == [(1, GREEN_VERDICT)]
    assert forge.merges == [(1, H1)]
    assert calls(log, "agents", "build") == [(PACKET,)]
    assert calls(log, "agents", "review") == [(H1, PACKET)]
    assert len(calls(log, "records", "close")) == 1
    operations = [(e.port, e.operation) for e in log.entries]
    assert operations.index(("forge", "post_verdict")) < operations.index(("forge", "merge"))
    assert BuildResult(H1, None).builder != GREEN_VERDICT.reviewer
    other = setup()
    drive(other, base="base-9")
    assert calls(other[0], "agents", "build") == [(replace(PACKET, base_sha="base-9"),)]
    assert other[2].issues[1][1] != forge.issues[1][1]
    print(f"Trace={trace.steps}; history={history}; calls={log.entries}")


@pytest.mark.parametrize("layer", ["story", "packet", "review", "merge"])
def test_layer_output_used(layer):
    composition = layers()
    state = setup()
    seen = []
    if layer == "story":
        varied = replace(STORY, title="Varied story")
        original = composition.packet
        def packet(story, base):
            seen.append(story)
            return original(story, base)
        composition = replace(composition, story=lambda raw: varied, packet=packet)
    elif layer == "packet":
        varied = replace(PACKET, story=replace(STORY, title="Varied packet"), base_sha="varied")
        composition = replace(composition, packet=lambda story, base: varied)
    elif layer == "review":
        varied = ReviewResult((Verdict(Decision.AMEND, H1, "reviewer-example", Role.PRIMARY),))
        original = composition.merge
        def merge(packet, review, suite, head):
            seen.append(review)
            return original(packet, review, suite, head)
        composition = replace(composition, review=lambda packet, verdicts: varied, merge=merge)
    else:
        varied = MergeDecision(Refusal("open-blocker"))
        composition = replace(composition, merge=lambda *args: varied)
    trace = drive(state, composition=composition)
    if layer in ("story", "review"):
        assert seen == [varied]
    if layer == "packet":
        assert state[2].issues == {1: (varied.story.title, varied.body)}
        assert calls(state[0], "agents", "build") == [(varied,)]
    if layer in ("review", "merge"):
        assert_abandoned(state, trace, "verdict-not-merge" if layer == "review" else "open-blocker")
    print(f"{layer} actual output used downstream")


@pytest.mark.parametrize("raw, reason", [(raw, reason) for _, raw, reason in readiness_cases()],
                         ids=[name for name, _, _ in readiness_cases()])
def test_readiness_no_effects(raw, reason):
    state = setup()
    trace = drive(state, raw)
    assert trace.outcome == Refusal(reason)
    assert trace.steps == ("story-received",)
    assert state[1].history("S-001") is None
    assert state[0].entries == []
    print(f"{reason} records=0 forge=0 agents=0")


@pytest.mark.parametrize("reason", [
    "verdict-missing", "verdict-surplus", "verdict-not-merge", "stale-head",
    "suite-missing", "suite-not-green", "suite-stale-head", "open-blocker", "packet-invalid",
])
def test_slice_refusals(reason):
    verdict = None if reason == "verdict-missing" else Verdict(
        Decision.BLOCK if reason == "open-blocker" else
        Decision.AMEND if reason == "verdict-not-merge" else Decision.MERGE,
        H2 if reason == "stale-head" else H1, "reviewer-example", Role.PRIMARY)
    suite = None if reason == "suite-missing" else SuiteReport(
        H2 if reason == "suite-stale-head" else H1, 7 if reason == "suite-not-green" else 0)
    composition = layers()
    if reason == "verdict-surplus":
        original = composition.review
        composition = replace(composition, review=lambda p, vs: original(p, (*vs, *vs)))
    if reason == "packet-invalid":
        composition = replace(composition, packet=lambda s, b: replace(PACKET, required_verdicts=2))
    state = setup(verdict, suite)
    assert_abandoned(state, drive(state, composition=composition), reason)
    print(f"{reason}")


class FailingAgents(MemoryAgents):
    failure = "build"

    def build(self, packet):
        if self.failure == "build":
            self.log.add("agents", "build", packet)
            raise AgentsRefused()
        return super().build(packet)

    def review(self, head, packet):
        self.log.add("agents", "review", head, packet)
        raise AgentsRefused()


class RefusingForge(MemoryForge):
    def post_verdict(self, pr, verdict):
        self.log.add("forge", "post_verdict", pr, verdict)
        raise ForgeRefused("verdict-refused")


@pytest.mark.parametrize("failure", ["build", "review", "verdict-post"])
def test_post_open_failures(failure):
    state = setup(forge_type=RefusingForge if failure == "verdict-post" else MemoryForge,
                  agent_type=MemoryAgents if failure == "verdict-post" else FailingAgents)
    state[3].failure = failure
    detail = "verdict-post-refused" if failure == "verdict-post" else f"{failure}-failed"
    assert_abandoned(state, drive(state), detail)
    print(f"failure={failure}")


class MovingForge(MemoryForge):
    timing = "after-review"
    observations = 0

    def pr_head(self, pr):
        self.observations += 1
        if self.timing == "after-review" and self.observations == 2:
            self.prs[pr] = (self.prs[pr][0], H2)
        return super().pr_head(pr)

    def merge(self, pr, expected_head):
        if self.timing == "before-merge":
            self.prs[pr] = (self.prs[pr][0], H2)
        super().merge(pr, expected_head)


@pytest.mark.parametrize("timing", ["after-review", "before-merge"])
def test_head_moves(timing):
    state = setup(forge_type=MovingForge)
    state[2].timing = timing
    trace = drive(state)
    assert_abandoned(state, trace, "merge-refused", attempts=1)
    assert calls(state[0], "forge", "merge") == [(1, H1)]
    assert state[2].observations == 2
    print(f"timing={timing} expected_head={H1} actual_head={state[2].prs[1][1]}")


def test_replay_and_closed_writes():
    state = setup()
    drive(state)
    history = state[1].history("S-001")
    effects = [e for e in state[0].entries if e.port != "records"]
    trace = drive(state, tick="tick-9")
    assert trace.outcome == Refusal("record-duplicate")
    assert state[1].history("S-001") == history
    assert [e for e in state[0].entries if e.port != "records"] == effects
    assert len(calls(state[0], "records", "close")) == 1
    print("replay refused; original history unchanged; closes=1; new forge/agents=0")
