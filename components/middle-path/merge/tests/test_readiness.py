"""Review readiness at the published merge seam."""

from dataclasses import FrozenInstanceError

import pytest
from mp_merge import readiness
from mp_ports import Decision, NotReady, Ready, Role, Rule, Verdict, parse_head

H = "a" * 40
OLD = "b" * 40
RULE = Rule((Role.PRIMARY,))


def verdict(decision=Decision.MERGE, head=H, reviewer="r-primary", role=Role.PRIMARY):
    return Verdict(decision, parse_head(head), reviewer, role)


def test_current_merge_is_ready():
    assert readiness((verdict(),), parse_head(H), RULE) == Ready()


def test_verdict_is_frozen():
    with pytest.raises(FrozenInstanceError):
        verdict().reviewer = "changed"


def test_parse_head_requires_exact_lowercase_hex():
    from mp_ports import Refusal
    assert parse_head(H) == H
    assert all(isinstance(parse_head(value), Refusal)
               for value in (H[:-1], H + "a", H.upper(), 123))


@pytest.mark.parametrize("decision,head,reviewer,role", [
    (Decision.MERGE, "bad-head", "r", Role.PRIMARY),
    (Decision.MERGE, H.upper(), "r", Role.PRIMARY),
    (Decision.MERGE, H[:-1], "r", Role.PRIMARY),
    ("APPROVE", H, "r", Role.PRIMARY),
    ("MERGE", H, "r", Role.PRIMARY),
    (Decision.MERGE, H, "r", "third"),
    (Decision.MERGE, H, "r", "primary"),
    (Decision.MERGE, H, " ", Role.PRIMARY),
    (Decision.MERGE, H, None, Role.PRIMARY),
])
def test_verdict_refuses_invalid_fields(decision, head, reviewer, role):
    with pytest.raises((TypeError, ValueError)):
        Verdict(decision, head, reviewer, role)


@pytest.mark.parametrize("role", ["third", "primary"])
def test_rule_refuses_unknown_role(role):
    with pytest.raises((TypeError, ValueError)):
        Rule((role,))


def test_rule_refuses_empty_requirement():
    with pytest.raises(ValueError, match="at least one role"):
        Rule(())


def test_verdict_requires_explicit_reviewer_and_role():
    with pytest.raises(TypeError):
        Verdict(Decision.MERGE, H)


def test_readiness_refuses_invalid_head():
    with pytest.raises((TypeError, ValueError)):
        readiness((verdict(),), "bad-head", RULE)


def test_repeated_role_slot_needs_distinct_reviewers():
    assert readiness((verdict(),), H, Rule((Role.PRIMARY, Role.PRIMARY))) == NotReady(("missing-role:primary",))


def test_only_stale_verdict_is_not_ready():
    assert readiness((verdict(head=OLD),), parse_head(H), RULE) == NotReady(("stale-only",))


@pytest.mark.parametrize("decision", [Decision.AMEND, Decision.FIX_FIRST, Decision.BLOCK])
def test_each_non_merge_blocks(decision):
    assert readiness((verdict(decision),), parse_head(H), RULE) == NotReady(("non-merge-at-head",))


def test_missing_second_role():
    assert readiness((verdict(),), parse_head(H), Rule((Role.PRIMARY, Role.SECOND))) == NotReady(("missing-role:second",))


@pytest.mark.parametrize("first,second", [(Decision.MERGE, Decision.MERGE),
                                          (Decision.AMEND, Decision.MERGE),
                                          (Decision.MERGE, Decision.AMEND)])
def test_same_reviewer_never_fills_two_slots(first, second):
    pair = (verdict(first), verdict(second, role=Role.SECOND))
    assert readiness(pair, parse_head(H), Rule((Role.PRIMARY, Role.SECOND))) == NotReady(("duplicate-reviewer",))


def test_stale_objection_does_not_block():
    assert readiness((verdict(), verdict(Decision.AMEND, OLD, "other")), parse_head(H), RULE) == Ready()
