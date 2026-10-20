"""closed readiness schema and declared field precedence."""

import pytest
from mp_examples import RAW, STORY, readiness_cases
from mp_ports import Refusal
from mp_story import load

CASES = readiness_cases()


@pytest.mark.parametrize("raw, reason", [(raw, reason) for _, raw, reason in CASES],
                         ids=[name for name, _, _ in CASES])
def test_readiness(raw, reason):
    assert load(raw) == Refusal(reason)
    print(f"readiness {reason}")


def test_smallest_story():
    assert load(RAW) == STORY
