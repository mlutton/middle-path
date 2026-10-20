"""Pure story readiness boundary."""

from typing import Literal, cast

from mp_ports import Refusal, Story, validate_story


def load(raw: object) -> Story | Refusal:
    refusal = validate_story(raw)
    if refusal:
        return refusal
    assert isinstance(raw, dict)
    return Story(raw["id"], raw["title"], raw["why"], tuple(raw["acceptance"]),
                 cast(Literal["light", "medium", "heavy"], raw["risk_tier"]))
