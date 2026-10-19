"""Pure synthetic single-reviewer collection boundary."""

from mp_ports import Packet, Refusal, ReviewResult, Verdict


def collect(packet: Packet, verdicts: tuple[Verdict, ...]) -> ReviewResult:
    refusal = None
    if not verdicts:
        refusal = Refusal("verdict-missing")
    elif len(verdicts) != packet.required_verdicts:
        refusal = Refusal("verdict-surplus")
    return ReviewResult(verdicts, refusal)
