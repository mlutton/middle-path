"""Pure merge evidence boundary."""

from collections import Counter
from dataclasses import dataclass

from mp_ports import (
    Decision,
    ExtraRoles,
    Head,
    MergeDecision,
    NotReady,
    Packet,
    ReadinessReason,
    Ready,
    Refusal,
    ReviewResult,
    Role,
    Rule,
    Sha,
    SuiteReport,
    Verdict,
    parse_head,
)


@dataclass(frozen=True)
class MergeFacts:
    head: Head
    parents: tuple[Head, ...]
    main_parent_in_main: bool
    merge_tree_ok: bool
    tree_equal: bool
    pr_files: tuple[str, ...]
    main_files: tuple[str, ...]
    security_path: bool
    resolution_lines: int
    unavailable: str | None


@dataclass(frozen=True)
class Carry:
    carried: bool
    reason: str


def carry(old_head: Head, new_head: Head, facts: MergeFacts) -> Carry:
    """Decide whether a second-role verdict can cross this exact main merge."""
    if facts.unavailable:
        return Carry(False, f"carry-unavailable: {facts.unavailable}")
    if facts.head != new_head or len(facts.parents) != 2 or facts.parents[0] != old_head or not facts.main_parent_in_main:
        return Carry(False, "not-main-merge-head")
    if facts.security_path:
        return Carry(False, "security-path")
    if set(facts.pr_files) & set(facts.main_files):
        return Carry(False, "overlap")
    if not facts.merge_tree_ok:
        return Carry(False, "merge-tree-conflict")
    if not facts.tree_equal:
        return Carry(False, "tree-differs")
    return Carry(True, "carried")


def readiness(verdicts: tuple[Verdict, ...], head: Head, rule: Rule,
              *, extra: ExtraRoles = ExtraRoles.none()) -> Ready | NotReady:  # noqa: B008 - immutable value
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
    if not isinstance(extra, ExtraRoles):
        raise TypeError("extra must be ExtraRoles")
    if extra.state == "invalid":
        return NotReady(("extra-roles-invalid",))
    current = tuple(verdict for verdict in verdicts if verdict.head == head)
    if not current:
        return NotReady(("stale-only" if verdicts else "no-verdict-at-head",))
    reviewers = [verdict.reviewer.casefold() for verdict in current]
    if len(reviewers) != len(set(reviewers)):
        return NotReady(("duplicate-reviewer",))
    if any(verdict.decision != Decision.MERGE for verdict in current):
        return NotReady(("non-merge-at-head",))
    available = Counter(verdict.role for verdict in current)
    required = Counter(rule.required_roles) | Counter(extra.roles)
    missing: tuple[ReadinessReason, ...] = tuple(
        "missing-role:primary" if role.value == "primary" else "missing-role:second"
        for role in required
        if available[role] < required[role]
    )
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
