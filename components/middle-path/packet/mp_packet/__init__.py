"""Pure packet construction boundary."""

from mp_ports import Packet, Refusal, Sha, Story


def build(story: Story, base_sha: Sha) -> Packet | Refusal:
    if story.refusal:
        return story.refusal
    if not isinstance(base_sha, str):
        return Refusal("wrong-type:base_sha")
    if not base_sha.strip():
        return Refusal("empty-field:base_sha")
    return Packet(story, base_sha)
