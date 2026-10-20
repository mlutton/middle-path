"""exactly one verdict, independently of ordering."""

import pytest
from mp_examples import PACKET
from mp_ports import Decision, Refusal, Role, Verdict
from mp_review import collect

MERGE = Verdict(Decision.MERGE, "a" * 40, "reviewer-example", Role.PRIMARY)
AMEND = Verdict(Decision.AMEND, "a" * 40, "reviewer-example", Role.PRIMARY)
BLOCK = Verdict(Decision.BLOCK, "a" * 40, "reviewer-example", Role.PRIMARY)
SURPLUS = [(a, b) for a, b in ((MERGE, MERGE), (MERGE, AMEND), (MERGE, BLOCK),
                              (AMEND, MERGE), (BLOCK, MERGE))]


@pytest.mark.parametrize("verdicts", SURPLUS)
def test_surplus(verdicts):
    assert collect(PACKET, verdicts).refusal == Refusal("verdict-surplus")


def test_missing():
    assert collect(PACKET, ()).refusal == Refusal("verdict-missing")


def test_exactly_one():
    result = collect(PACKET, (MERGE,))
    assert result.refusal is None
    assert result.verdicts == (MERGE,)
