"""Reusable Agents cases; factory configures two ids and absent evidence."""

from collections.abc import Callable
from dataclasses import replace

from .agents import AgentsRefused
from .protocols import Agents
from .types import BuildResult, Decision, EffectLog, Packet, Role, Story, SuiteReport, Verdict

AgentFactory = Callable[[EffectLog, dict[str, BuildResult], dict[str, Verdict | None]], Agents]


def contract_agents_cases() -> tuple[tuple[str, Callable[[AgentFactory], None]], ...]:
    head = "a" * 40
    packet = Packet(Story("S-001", "Example", "Useful", ("One line",), "medium"), "base")
    other = replace(packet, story=replace(packet.story, id="S-002"))
    unknown = replace(packet, story=replace(packet.story, id="S-999"))

    def keyed(factory: AgentFactory) -> None:
        log = EffectLog()
        first = BuildResult(head, SuiteReport(head, 0))
        second = BuildResult("head-2", None)
        verdict = Verdict(Decision.MERGE, head, "reviewer-example", Role.PRIMARY)
        agents = factory(log, {packet.id: first, other.id: second}, {packet.id: verdict, other.id: None})
        assert agents.build(packet) == first
        assert agents.build(other) == second
        assert agents.review(head, packet) == verdict
        assert agents.review("head-2", other) is None
        assert [(e.operation, e.arguments) for e in log.entries] == [
            ("build", (packet,)), ("build", (other,)),
            ("review", (head, packet)), ("review", ("head-2", other)),
        ]

    def unknown_build(factory: AgentFactory) -> None:
        _unknown(factory, unknown, False)

    def unknown_review(factory: AgentFactory) -> None:
        _unknown(factory, unknown, True)

    return (("keyed-arguments-and-absence", keyed), ("unknown-build", unknown_build),
            ("unknown-review", unknown_review))


def _unknown(factory: AgentFactory, packet: Packet, review: bool) -> None:
    log = EffectLog()
    agents = factory(log, {}, {})
    try:
        agents.review("head-1", packet) if review else agents.build(packet)
    except AgentsRefused as exc:
        assert exc.reason == "packet-unknown"
    else:
        raise AssertionError("unknown packet accepted")
    assert log.entries[0].arguments == (("head-1", packet) if review else (packet,))
