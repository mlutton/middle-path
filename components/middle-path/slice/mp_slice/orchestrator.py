"""Drive the supplied layers and ports without importing a sibling layer."""

from collections.abc import Callable

from mp_ports import (
    Agents,
    BuildResult,
    CloseReason,
    Event,
    Forge,
    ForgeRefused,
    Layers,
    Packet,
    Records,
    RecordsRefused,
    Refusal,
    ReviewResult,
    Trace,
)


def run(story_raw: object, base_sha: str, *, layers: Layers, records: Records,
        forge: Forge, agents: Agents, clock: Callable[[], str]) -> Trace:
    steps = ["story-received"]
    story = layers.story(story_raw)
    if isinstance(story, Refusal):
        return Trace(tuple(steps), story)
    packet = layers.packet(story, base_sha)
    if isinstance(packet, Refusal):
        return Trace(tuple(steps), packet)
    steps.append("packet-ready")
    session = _Run(packet, layers, records, forge, agents, clock, steps)
    try:
        session.version = records.open(packet.id, session.event("record-opened"))
    except RecordsRefused as exc:
        return Trace(tuple(steps), Refusal(exc.reason))
    steps.append("record-opened")
    return session.execute()


class _Run:
    def __init__(self, packet: Packet, layers: Layers, records: Records, forge: Forge,
                 agents: Agents, clock: Callable[[], str], steps: list[str]) -> None:
        self.packet = packet
        self.layers = layers
        self.records = records
        self.forge = forge
        self.agents = agents
        self.clock = clock
        self.steps = steps
        self.version = 0

    def event(self, step: str, **payload: str | int | None) -> Event:
        common: dict[str, str | int | None] = {
            "story_id": self.packet.id, "packet_digest": self.packet.digest,
        }
        return Event(step, self.clock(), tuple({**common, **payload}.items()))

    def append(self, step: str, **payload: str | int | None) -> None:
        self.version = self.records.append(self.packet.id, self.event(step, **payload), self.version)

    def finish(self, outcome: str | Refusal) -> Trace:
        reason: CloseReason = "abandoned" if isinstance(outcome, Refusal) else "done"
        detail = outcome.reason if isinstance(outcome, Refusal) else "MERGE"
        self.records.close(self.packet.id, reason, detail, self.version)
        self.steps.append("record-closed")
        return Trace(tuple(self.steps), outcome if isinstance(outcome, Refusal) else "MERGE")

    def build(self) -> BuildResult | Refusal:
        self.append("build-requested")
        self.steps.append("build-requested")
        try:
            result = self.agents.build(self.packet)
        except Exception:
            return Refusal("build-failed")
        self.append("build-returned", build_head=result.head_sha)
        self.steps.append("build-returned")
        return result

    def review(self, pr: int, head: str) -> ReviewResult | Refusal:
        try:
            verdict = self.agents.review(head, self.packet)
        except Exception:
            return Refusal("review-failed")
        if verdict is not None:
            try:
                self.forge.post_verdict(pr, verdict)
            except ForgeRefused:
                return Refusal("verdict-post-refused")
            self.steps.append("verdict-posted")
        self.append("verdict-recorded", verdict_head=verdict.head_sha if verdict else None,
                    kind=verdict.kind if verdict else None)
        return self.layers.review(self.packet, () if verdict is None else (verdict,))

    def execute(self) -> Trace:
        issue = self.forge.create_issue(self.packet.story.title, self.packet.body)
        self.steps.append("issue-created")
        result = self.build()
        if isinstance(result, Refusal):
            return self.finish(result)
        pr = self.forge.create_pr(issue, result.head_sha)
        self.steps.append("pr-created")
        head = self.forge.pr_head(pr)
        review = self.review(pr, head)
        if isinstance(review, Refusal):
            return self.finish(review)
        suite = result.suite
        self.append("suite-recorded", suite_head=suite.head_sha if suite else None,
                    suite_exit=suite.exit if suite else None)
        self.steps.append("suite-recorded")
        observed = self.forge.pr_head(pr)
        # Decide against the reviewed snapshot; Forge atomically refuses any later head.
        decision = self.layers.merge(self.packet, review, suite, head)
        self.append("merge-decided", head=head, observed_head=observed,
                    decision=decision.outcome.reason if isinstance(decision.outcome, Refusal) else "MERGE")
        self.steps.append("merge-decided")
        if isinstance(decision.outcome, Refusal):
            return self.finish(decision.outcome)
        try:
            self.forge.merge(pr, expected_head=head)
        except ForgeRefused:
            return self.finish(Refusal("merge-refused"))
        return self.finish(decision.outcome)
