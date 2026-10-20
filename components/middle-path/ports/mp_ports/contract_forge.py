"""Reusable Forge cases with snapshots supplied by the adapter factory."""

from collections.abc import Callable

from .forge import ForgeRefused
from .protocols import Forge
from .types import Decision, Role, Verdict


def contract_forge_cases() -> tuple[tuple[str, Callable[[Forge, Callable[[], object]], None]], ...]:
    def refusal(forge: Forge, snapshot: Callable[[], object], operation: str) -> None:
        issue = forge.create_issue("Example", "Synthetic body")
        pr = forge.create_pr(issue, "head-1")
        if operation == "double-merge":
            forge.merge(pr, "head-1")
        actions: dict[str, tuple[str, Callable[[], object]]] = {
            "double-merge": ("already-merged", lambda: forge.merge(pr, "head-1")),
            "moved-head": ("head-moved", lambda: forge.merge(pr, "old-head")),
            "unknown-issue": ("issue-unknown", lambda: forge.create_pr(999, "head-1")),
            "unknown-head": ("pr-unknown", lambda: forge.pr_head(999)),
            "unknown-verdict": ("pr-unknown", lambda: forge.post_verdict(999, Verdict(Decision.MERGE, "a" * 40, "reviewer-example", Role.PRIMARY))),
            "unknown-merge": ("pr-unknown", lambda: forge.merge(999, "head-1")),
        }
        reason, action = actions[operation]
        before = snapshot()
        try:
            action()
        except ForgeRefused as exc:
            assert exc.reason == reason
        else:
            raise AssertionError(f"expected {reason}")
        assert snapshot() == before

    def case(operation: str) -> Callable[[Forge, Callable[[], object]], None]:
        return lambda forge, snapshot: refusal(forge, snapshot, operation)

    return tuple((name, case(name)) for name in (
        "double-merge", "moved-head", "unknown-issue", "unknown-head",
        "unknown-verdict", "unknown-merge",
    ))
