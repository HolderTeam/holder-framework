from enum import StrEnum


class EventResyncDataReason(StrEnum):
    HISTORY_UNAVAILABLE = "history_unavailable"
    OBSERVER_UNAVAILABLE = "observer_unavailable"

    def __str__(self) -> str:
        return str(self.value)
