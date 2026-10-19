"""Three replaceable effect boundaries."""

from typing import Protocol

from .types import (
    BuildResult,
    CloseReason,
    Event,
    IssueId,
    Packet,
    PrId,
    Reason,
    Sha,
    Verdict,
    Version,
)


class Records(Protocol):
    def open(self, record_id: str, opened_event: Event) -> Version: ...
    def append(self, record_id: str, event: Event, expected_version: Version) -> Version: ...
    def close(self, record_id: str, reason: CloseReason, detail: Reason | str,
              expected_version: Version) -> Version: ...
    def history(self, record_id: str) -> tuple[Event, ...] | None: ...


class Forge(Protocol):
    def create_issue(self, title: str, body: str) -> IssueId: ...
    def create_pr(self, issue: IssueId, head_sha: Sha) -> PrId: ...
    def post_verdict(self, pr: PrId, verdict: Verdict) -> None: ...
    def pr_head(self, pr: PrId) -> Sha: ...
    def merge(self, pr: PrId, expected_head: Sha) -> None: ...


class Agents(Protocol):
    def build(self, packet: Packet) -> BuildResult: ...
    def review(self, pr_head: Sha, packet: Packet) -> Verdict | None: ...
