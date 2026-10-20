"""smallest packet and base commit are real inputs."""

from dataclasses import replace

import pytest
from mp_examples import STORY
from mp_packet import build
from mp_ports import Packet, Refusal


def test_packet_base_and_smallest():
    first = build(STORY, "base-0")
    second = build(STORY, "base-1")
    assert first == Packet(STORY, "base-0", 1)
    assert second == Packet(STORY, "base-1", 1)
    assert first.digest != second.digest


@pytest.mark.parametrize("story, base, reason", [
    (replace(STORY, title=""), "base", "empty-field:title"),
    (STORY, "", "empty-field:base_sha"), (STORY, "  ", "empty-field:base_sha"),
    (STORY, None, "wrong-type:base_sha"),
])
def test_packet_refuses(story, base, reason):
    assert build(story, base) == Refusal(reason)
