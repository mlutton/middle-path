"""Pure merge evidence boundary."""

from collections import Counter

from mp_ports import (Decision, Head, MergeDecision, NotReady, Packet, Ready, Refusal,
                      ReviewResult, Role, Rule, Sha, SuiteReport, Verdict, parse_head)


def readiness(verdicts: tuple[Verdict, ...], head: Head, rule: Rule) -> Ready | NotReady:
    """An approval counts only from a reviewer the caller maps to a required role;
    an objection from any well-formed reviewer is seen and blocks."""
    if isinstance(parse_head(head), Refusal):
        raise ValueError("head must be 40 lowercase hex characters")
    if not isinstance(rule, Rule) or not isinstance(rule.required_roles, tuple) or any(
        not isinstance(role, Role) for role in rule.required_roles
    ):
        raise TypeError("rule must contain Role values")
    if not isinstance(verdicts, tuple) or any(not isinstance(verdict, Verdict) for verdict in verdicts):
        raise TypeError("verdicts must be a tuple of Verdict values")
    current = tuple(verdict for verdict in verdicts if verdict.head == head)
    if not current:
        return NotReady(("stale-only" if verdicts else "no-verdict-at-head",))
    reviewers = [verdict.reviewer.casefold() for verdict in current]
    if len(reviewers) != len(set(reviewers)):
        return NotReady(("duplicate-reviewer",))
    if any(verdict.decision != Decision.MERGE for verdict in current):
        return NotReady(("non-merge-at-head",))
    available = Counter(verdict.role for verdict in current)
    required = Counter(rule.required_roles)
    missing = tuple("missing-role:primary" if role.value == "primary" else "missing-role:second"
                    for role in required
                    if available[role] < required[role])
    return NotReady(missing) if missing else Ready()


def decide(packet: Packet | Refusal, review: ReviewResult,
           suite: SuiteReport | None, pr_head: Sha) -> MergeDecision:
    if not isinstance(packet, Packet) or not packet.valid:
        return MergeDecision(Refusal("packet-invalid"))
    if review.refusal:
        return MergeDecision(review.refusal)
    if len(review.verdicts) != 1:
        return MergeDecision(Refusal("verdict-missing" if not review.verdicts else "verdict-surplus"))
    verdict = review.verdicts[0]
    if verdict.head != pr_head:
        return MergeDecision(Refusal("stale-head"))
    if verdict.decision == Decision.BLOCK:
        return MergeDecision(Refusal("open-blocker"))
    if verdict.decision != Decision.MERGE:
        return MergeDecision(Refusal("verdict-not-merge"))
    if suite is None:
        return MergeDecision(Refusal("suite-missing"))
    return _suite_decision(suite, pr_head)


def _suite_decision(suite: SuiteReport, pr_head: Sha) -> MergeDecision:
    if suite.head_sha != pr_head:
        return MergeDecision(Refusal("suite-stale-head"))
    if type(suite.exit) is not int or suite.exit != 0:
        return MergeDecision(Refusal("suite-not-green"))
    return MergeDecision("MERGE")
