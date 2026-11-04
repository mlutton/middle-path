"""The pure merge carry decision across a pure main merge."""

from mp_merge import MergeFacts, carry, readiness
from mp_ports import Decision, Ready, Role, Rule, Verdict

H = "a" * 40
M = "b" * 40
P = "c" * 40


def facts(**changes):
    values = dict(head=M, parents=(H, P), main_parent_in_main=True,
                  merge_tree_ok=True, tree_equal=True, pr_files=("src/a.py",),
                  main_files=("src/b.py",), security_path=False,
                  resolution_lines=0, unavailable=None)
    values.update(changes)
    return MergeFacts(**values)


def test_u1_pure_merge_carries_second_verdict():
    assert carry(H, M, facts()).carried


def test_d_carried_second_and_direct_primary_are_ready():
    first = Verdict(Decision.MERGE, M, "reviewer-a", Role.PRIMARY)
    second = Verdict(Decision.MERGE, M, "reviewer-b", Role.SECOND,
                   provenance="carried", carried_from=H)
    assert readiness((first, second), M, Rule((Role.PRIMARY, Role.SECOND))) == Ready()
