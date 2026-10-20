"""Drive the supplied layers and ports without importing a sibling layer."""

from collections.abc import Callable

from mp_ports import (
    AdapterError,
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
    try:
        return session.execute()
    except Exception:
        # Cleanup must not convert a programming error into an adapter refusal.
        if not session.close_attempted:
            session.finish(Refusal("unexpected-error"))
        raise


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
        self.close_attempted = False

    def event(self, step: str, **payload: str | int | None) -> Event:
        common: dict[str, str | int | None] = {
            "story_id": self.packet.id, "packet_digest": self.packet.digest,
        }
        return Event(step, self.clock(), tuple({**common, **payload}.items()))

    def append(self, step: str, **payload: str | int | None) -> None:
        self.version = self.records.append(self.packet.id, self.event(step, **payload), self.version)

    def step(self, name: str, **payload: str | int | None) -> None:
        self.append(name, **payload)
        self.note(name)

    def note(self, name: str) -> None:
        self.steps.append(name)

    def finish(self, outcome: str | Refusal) -> Trace:
        reason: CloseReason = "abandoned" if isinstance(outcome, Refusal) else "done"
        detail = outcome.reason if isinstance(outcome, Refusal) else "MERGE"
        self.close_attempted = True
        try:
            self.records.close(self.packet.id, reason, detail, self.version)
        except RecordsRefused:
            return Trace(tuple(self.steps), Refusal("close-refused"))
        self.note("record-closed")
        return Trace(tuple(self.steps), outcome if isinstance(outcome, Refusal) else "MERGE")

    def build(self) -> BuildResult | Refusal:
        self.step("build-requested")
        try:
            result = self.agents.build(self.packet)
        except AdapterError:
            return Refusal("build-failed")
        self.step("build-returned", build_head=result.head_sha)
        return result

    def review(self, pr: int, head: str) -> ReviewResult | Refusal:
        try:
            verdict = self.agents.review(head, self.packet)
        except AdapterError:
            return Refusal("review-failed")
        if verdict is not None:
            try:
                self.forge.post_verdict(pr, verdict)
            except ForgeRefused:
                return Refusal("verdict-post-refused")
            self.note("verdict-posted")
        self.append("verdict-recorded", verdict_head=verdict.head_sha if verdict else None,
                    kind=verdict.kind if verdict else None)
        return self.layers.review(self.packet, () if verdict is None else (verdict,))

    def execute(self) -> Trace:
        try:
            issue = self.forge.create_issue(self.packet.story.title, self.packet.body)
        except AdapterError:
            return self.finish(Refusal("issue-create-failed"))
        self.note("issue-created")
        result = self.build()
        if isinstance(result, Refusal):
            return self.finish(result)
        try:
            pr = self.forge.create_pr(issue, result.head_sha)
        except AdapterError:
            return self.finish(Refusal("pr-create-failed"))
        self.note("pr-created")
        head = self.forge.pr_head(pr)
        review = self.review(pr, head)
        if isinstance(review, Refusal):
            return self.finish(review)
        suite = result.suite
        self.step("suite-recorded", suite_head=suite.head_sha if suite else None,
                    suite_exit=suite.exit if suite else None)
        observed = self.forge.pr_head(pr)
        # Decide against the reviewed snapshot; Forge atomically refuses any later head.
        decision = self.layers.merge(self.packet, review, suite, head)
        self.step("merge-decided", head=head, observed_head=observed,
                    decision=decision.outcome.reason if isinstance(decision.outcome, Refusal) else "MERGE")
        if isinstance(decision.outcome, Refusal):
            return self.finish(decision.outcome)
        try:
            self.forge.merge(pr, expected_head=head)
        except ForgeRefused:
            return self.finish(Refusal("merge-refused"))
        return self.finish(decision.outcome)
