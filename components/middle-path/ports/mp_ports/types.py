"""Immutable seam values and the closed refusal vocabulary."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from hashlib import sha256
from json import dumps
from re import fullmatch
from typing import Literal, TypeAlias

SchemaReason: TypeAlias = Literal[
    "wrong-type:raw", "missing-field:id", "empty-field:id", "wrong-type:id", "bad-id",
    "missing-field:title", "empty-field:title", "wrong-type:title",
    "missing-field:why", "empty-field:why", "wrong-type:why",
    "missing-field:acceptance", "empty-field:acceptance", "wrong-type:acceptance",
    "missing-field:risk_tier", "empty-field:risk_tier", "wrong-type:risk_tier",
    "empty-field:base_sha", "wrong-type:base_sha", "tier-unsupported",
]
EvidenceReason: TypeAlias = Literal[
    "packet-invalid", "verdict-missing", "verdict-surplus", "verdict-not-merge",
    "stale-head", "suite-missing", "suite-not-green", "suite-stale-head", "open-blocker",
]
RecordReason: TypeAlias = Literal["record-duplicate", "record-unknown", "version-stale", "record-closed"]
ForgeReason: TypeAlias = Literal["issue-unknown", "pr-unknown", "head-moved", "already-merged", "verdict-refused"]
FailureReason: TypeAlias = Literal[
    "build-failed", "review-failed", "verdict-post-refused", "merge-refused",
    "issue-create-failed", "pr-create-failed", "close-refused", "unexpected-error",
]
Reason: TypeAlias = SchemaReason | EvidenceReason | RecordReason | FailureReason
CloseReason: TypeAlias = Literal["done", "abandoned"]
Version: TypeAlias = int
Sha: TypeAlias = str
IssueId: TypeAlias = int
PrId: TypeAlias = int


class AdapterError(Exception):
    """Expected failure reported by an adapter, carrying its stable reason."""

    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class Refusal:
    reason: Reason


@dataclass(frozen=True)
class Story:
    id: str
    title: str
    why: str
    acceptance: tuple[str, ...]
    risk_tier: Literal["light", "medium", "heavy"]

    def raw(self) -> dict[str, object]:
        return {**asdict(self), "acceptance": list(self.acceptance)}

    @property
    def refusal(self) -> Refusal | None:
        return validate_story(self.raw())


def _field(name: str, value: object) -> str | None:
    if name == "acceptance":
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            return "wrong-type"
        return "empty-field" if not value or any(not v.strip() for v in value) else None
    if not isinstance(value, str):
        return "wrong-type"
    if not value.strip():
        return "empty-field"
    if name == "id" and fullmatch(r"S-[0-9]{3}", value) is None:
        return "bad-id"
    if name == "risk_tier":
        if value not in ("light", "medium", "heavy"):
            return "wrong-type"
        if value != "medium":
            return "tier-unsupported"
    return None


# Explicit mapping keeps dynamic field validation inside the closed vocabulary.
_FIELD_CODES: tuple[tuple[str, tuple[SchemaReason, ...]], ...] = (
        ("id", ("missing-field:id", "empty-field:id", "wrong-type:id")),
        ("title", ("missing-field:title", "empty-field:title", "wrong-type:title")),
        ("why", ("missing-field:why", "empty-field:why", "wrong-type:why")),
        ("acceptance", ("missing-field:acceptance", "empty-field:acceptance", "wrong-type:acceptance")),
        ("risk_tier", ("missing-field:risk_tier", "empty-field:risk_tier", "wrong-type:risk_tier")),
)
_SCHEMA: dict[str, SchemaReason] = {
    f"{prefix}:{name}": code
    for name, codes in _FIELD_CODES
    for prefix, code in zip(("missing-field", "empty-field", "wrong-type"), codes, strict=True)
}


def validate_story(raw: object) -> Refusal | None:
    if not isinstance(raw, dict):
        return Refusal("wrong-type:raw")
    names = ("id", "title", "why", "acceptance", "risk_tier")
    for name in names:
        problem = "missing-field" if name not in raw else _field(name, raw[name])
        if problem in ("bad-id", "tier-unsupported"):
            return Refusal("bad-id" if problem == "bad-id" else "tier-unsupported")
        if problem:
            return Refusal(_SCHEMA[f"{problem}:{name}"])
    return Refusal("wrong-type:raw") if set(raw) != set(names) else None


@dataclass(frozen=True)
class Packet:
    story: Story
    base_sha: Sha
    required_verdicts: int = 1

    @property
    def valid(self) -> bool:
        return (isinstance(self.story, Story) and self.story.refusal is None
                and isinstance(self.base_sha, str) and bool(self.base_sha.strip())
                and type(self.required_verdicts) is int and self.required_verdicts == 1)

    @property
    def body(self) -> str:
        return dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @property
    def digest(self) -> str:
        return sha256(self.body.encode()).hexdigest()

    @property
    def id(self) -> str:
        return self.story.id


@dataclass(frozen=True)
class Verdict:
    head_sha: Sha
    kind: Literal["MERGE", "AMEND"] = "MERGE"
    open_blocker: bool = False
    reviewer: str = "reviewer-example"


@dataclass(frozen=True)
class ReviewResult:
    verdicts: tuple[Verdict, ...]
    refusal: Refusal | None = None


@dataclass(frozen=True)
class SuiteReport:
    head_sha: Sha
    exit: int


@dataclass(frozen=True)
class BuildResult:
    head_sha: Sha
    suite: SuiteReport | None
    builder: str = "builder-example"


@dataclass(frozen=True)
class Decision:
    outcome: Literal["MERGE"] | Refusal


@dataclass(frozen=True)
class Event:
    step: str
    at: str
    payload: tuple[tuple[str, str | int | None], ...] = ()


@dataclass(frozen=True)
class Effect:
    port: str
    operation: str
    arguments: tuple[object, ...]


@dataclass
class EffectLog:
    entries: list[Effect] = field(default_factory=list)

    def add(self, port: str, operation: str, *arguments: object) -> None:
        self.entries.append(Effect(port, operation, arguments))


@dataclass(frozen=True)
class Layers:
    story: Callable[[object], Story | Refusal]
    packet: Callable[[Story, Sha], Packet | Refusal]
    review: Callable[[Packet, tuple[Verdict, ...]], ReviewResult]
    merge: Callable[[Packet | Refusal, ReviewResult, SuiteReport | None, Sha], Decision]


@dataclass(frozen=True)
class Trace:
    steps: tuple[str, ...]
    outcome: Literal["MERGE"] | Refusal
