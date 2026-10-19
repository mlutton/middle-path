"""Versioned in-memory Records adapter. Refusals never change history."""

from .types import CloseReason, EffectLog, Event, RecordReason, Version


class RecordsRefused(Exception):
    def __init__(self, reason: RecordReason) -> None:
        self.reason = reason
        super().__init__(reason)


class MemoryRecords:
    def __init__(self, log: EffectLog) -> None:
        self.log = log
        self._histories: dict[str, tuple[Event, ...]] = {}
        self._closed: set[str] = set()

    def open(self, record_id: str, opened_event: Event) -> Version:
        self.log.add("records", "open", record_id, opened_event)
        if record_id in self._histories:
            raise RecordsRefused("record-duplicate")
        self._histories[record_id] = (opened_event,)
        return 1

    def _check(self, record_id: str, expected_version: Version) -> tuple[Event, ...]:
        if record_id not in self._histories:
            raise RecordsRefused("record-unknown")
        if record_id in self._closed:
            raise RecordsRefused("record-closed")
        history = self._histories[record_id]
        if expected_version != len(history):
            raise RecordsRefused("version-stale")
        return history

    def append(self, record_id: str, event: Event, expected_version: Version) -> Version:
        self.log.add("records", "append", record_id, event, expected_version)
        history = self._check(record_id, expected_version)
        self._histories[record_id] = (*history, event)
        return len(history) + 1

    def close(self, record_id: str, reason: CloseReason, detail: str,
              expected_version: Version) -> Version:
        self.log.add("records", "close", record_id, reason, detail, expected_version)
        history = self._check(record_id, expected_version)
        event = Event("record-closed", history[-1].at, (("reason", reason), ("detail", detail)))
        self._histories[record_id] = (*history, event)
        self._closed.add(record_id)
        return len(history) + 1

    def history(self, record_id: str) -> tuple[Event, ...] | None:
        return self._histories.get(record_id)
