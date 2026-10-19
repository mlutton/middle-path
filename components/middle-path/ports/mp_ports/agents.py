"""Canned agent evidence, keyed by packet id, with complete call arguments."""

from .types import BuildResult, EffectLog, Packet, Sha, Verdict


class AgentsRefused(Exception):
    reason = "packet-unknown"


class MemoryAgents:
    def __init__(self, log: EffectLog, builds: dict[str, BuildResult],
                 reviews: dict[str, Verdict | None]) -> None:
        self.log = log
        self.builds = dict(builds)
        self.reviews = dict(reviews)

    def build(self, packet: Packet) -> BuildResult:
        self.log.add("agents", "build", packet)
        if packet.id not in self.builds:
            raise AgentsRefused()
        return self.builds[packet.id]

    def review(self, pr_head: Sha, packet: Packet) -> Verdict | None:
        self.log.add("agents", "review", pr_head, packet)
        if packet.id not in self.reviews:
            raise AgentsRefused()
        return self.reviews[packet.id]
