"""Synthetic inputs shared by seam tests."""

from mp_ports import Packet, Story

RAW = {"id": "S-001", "title": "Example change", "why": "Show the path",
       "acceptance": ["One observable result"], "risk_tier": "medium"}
STORY = Story("S-001", "Example change", "Show the path", ("One observable result",), "medium")
PACKET = Packet(STORY, "base-0")


def readiness_cases():
    cases = []
    for field in RAW:
        missing = dict(RAW)
        del missing[field]
        cases.append((f"missing-{field}", missing, f"missing-field:{field}"))
        for label, value in (("empty", [] if field == "acceptance" else ""),
                             ("space", ["   "] if field == "acceptance" else "   "),
                             ("type", 1)):
            cases.append((f"{label}-{field}", {**RAW, field: value}, f"{('wrong-type' if label == 'type' else 'empty-field')}:{field}"))
    for label, value, reason in (("empty-item", [""], "empty-field:acceptance"),
                                  ("item-type", [1], "wrong-type:acceptance"),
                                  ("container", "one", "wrong-type:acceptance")):
        cases.append((label, {**RAW, "acceptance": value}, reason))
    cases.extend((tier, {**RAW, "risk_tier": tier}, "tier-unsupported") for tier in ("light", "heavy"))
    cases.extend([
        ("unknown-tier", {**RAW, "risk_tier": "other"}, "wrong-type:risk_tier"),
        ("bad-id", {**RAW, "id": "bad"}, "bad-id"),
        ("precedence", {**RAW, "title": "", "why": 1}, "empty-field:title"),
        ("unknown-field", {**RAW, "extra": "value"}, "wrong-type:raw"),
    ])
    cases.extend((f"malformed-{i}", raw, "wrong-type:raw") for i, raw in enumerate((None, [], "story", 1)))
    return cases
