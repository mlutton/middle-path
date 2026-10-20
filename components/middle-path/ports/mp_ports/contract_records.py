"""Reusable Records cases: an adapter supplies only a fresh factory."""

from collections.abc import Callable

from .protocols import Records
from .records import RecordsRefused
from .types import Event

OPEN = Event("record-opened", "tick-1")
NEXT = Event("build-requested", "tick-2")


def _refused(records: Records, action: Callable[[], object], reason: str) -> None:
    before = records.history("S-001")
    try:
        action()
    except RecordsRefused as exc:
        assert exc.reason == reason
    else:
        raise AssertionError(f"expected {reason}")
    assert records.history("S-001") == before
    assert records.history("S-999") is None


def contract_records_cases() -> tuple[tuple[str, Callable[[Records], None]], ...]:
    def duplicate(records: Records) -> None:
        assert records.open("S-001", OPEN) == 1
        _refused(records, lambda: records.open("S-001", OPEN), "record-duplicate")
        assert records.append("S-001", NEXT, 1) == 2

    def unknown_append(records: Records) -> None:
        _refused(records, lambda: records.append("S-999", NEXT, 0), "record-unknown")

    def unknown_close(records: Records) -> None:
        _refused(records, lambda: records.close("S-999", "done", "MERGE", 0), "record-unknown")

    def stale_append(records: Records) -> None:
        records.open("S-001", OPEN)
        _refused(records, lambda: records.append("S-001", NEXT, 0), "version-stale")
        assert records.append("S-001", NEXT, 1) == 2

    def stale_close(records: Records) -> None:
        records.open("S-001", OPEN)
        _refused(records, lambda: records.close("S-001", "done", "MERGE", 0), "version-stale")
        assert records.close("S-001", "done", "MERGE", 1) == 2

    def closed_append(records: Records) -> None:
        records.open("S-001", OPEN)
        assert records.close("S-001", "done", "MERGE", 1) == 2
        _refused(records, lambda: records.append("S-001", NEXT, 2), "record-closed")

    def closed_close(records: Records) -> None:
        records.open("S-001", OPEN)
        records.close("S-001", "done", "MERGE", 1)
        _refused(records, lambda: records.close("S-001", "done", "MERGE", 2), "record-closed")

    def history(records: Records) -> None:
        assert records.history("S-001") is None
        records.open("S-001", OPEN)
        saved = records.history("S-001")
        records.append("S-001", NEXT, 1)
        assert saved == (OPEN,)
        assert records.history("S-001") == (OPEN, NEXT)

    return tuple((case.__name__, case) for case in (
        duplicate, unknown_append, unknown_close, stale_append, stale_close,
        closed_append, closed_close, history,
    ))
