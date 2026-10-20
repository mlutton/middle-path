"""merge evidence matrix using published port values at two heads."""

from dataclasses import replace

import pytest
from mp_examples import PACKET
from mp_merge import decide
from mp_ports import Decision, MergeDecision, Refusal, ReviewResult, Role, SuiteReport, Verdict


@pytest.mark.parametrize("head", ["a" * 40, "b" * 40])
@pytest.mark.parametrize("case, reason", [
    ("green", None), ("amend", "verdict-not-merge"), ("absent", "verdict-missing"),
    ("stale", "stale-head"), ("surplus", "verdict-surplus"),
    ("red", "suite-not-green"), ("no-suite", "suite-missing"),
    ("old-suite", "suite-stale-head"), ("blocker", "open-blocker"),
    ("invalid", "packet-invalid"), ("refused", "packet-invalid"),
])
def test_decision_matrix(head, case, reason):
    verdict = Verdict(Decision.AMEND if case == "amend" else Decision.BLOCK if case == "blocker" else Decision.MERGE,
                      "c" * 40 if case == "stale" else head, "reviewer-example", Role.PRIMARY)
    verdicts = () if case == "absent" else (verdict, verdict) if case == "surplus" else (verdict,)
    suite = None if case == "no-suite" else SuiteReport("other" if case == "old-suite" else head,
                                                       1 if case == "red" else 0)
    packet = (replace(PACKET, required_verdicts=2) if case == "invalid" else
              Refusal("bad-id") if case == "refused" else PACKET)
    review = ReviewResult(verdicts, Refusal("verdict-missing") if not verdicts else
                          Refusal("verdict-surplus") if len(verdicts) > 1 else None)
    result = decide(packet, review, suite, head)
    assert result == MergeDecision("MERGE" if reason is None else Refusal(reason))
    print(f"{head} {case}: {result}")


def test_stale_block_is_reported_as_stale_head():
    review = ReviewResult((Verdict(Decision.BLOCK, "b" * 40, "reviewer", Role.PRIMARY),))
    assert decide(PACKET, review, None, "a" * 40) == MergeDecision(Refusal("stale-head"))
