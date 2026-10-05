from enum import StrEnum


class CardReferenceResolveRequestScope(StrEnum):
    EITHER = "either"
    LIVE = "live"
    TRASHED = "trashed"

    def __str__(self) -> str:
        return str(self.value)
