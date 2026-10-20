"""Pure merge evidence boundary."""

from mp_ports import Decision, Packet, Refusal, ReviewResult, Sha, SuiteReport


def decide(packet: Packet | Refusal, review: ReviewResult,
           suite: SuiteReport | None, pr_head: Sha) -> Decision:
    if not isinstance(packet, Packet) or not packet.valid:
        return Decision(Refusal("packet-invalid"))
    if review.refusal:
        return Decision(review.refusal)
    if len(review.verdicts) != 1:
        return Decision(Refusal("verdict-missing" if not review.verdicts else "verdict-surplus"))
    verdict = review.verdicts[0]
    if verdict.kind != "MERGE":
        return Decision(Refusal("verdict-not-merge"))
    if verdict.head_sha != pr_head:
        return Decision(Refusal("stale-head"))
    if suite is None:
        return Decision(Refusal("suite-missing"))
    return _suite_decision(suite, pr_head, verdict.open_blocker)


def _suite_decision(suite: SuiteReport, pr_head: Sha, blocker: bool) -> Decision:
    if suite.head_sha != pr_head:
        return Decision(Refusal("suite-stale-head"))
    if type(suite.exit) is not int or suite.exit != 0:
        return Decision(Refusal("suite-not-green"))
    if blocker:
        return Decision(Refusal("open-blocker"))
    return Decision("MERGE")
