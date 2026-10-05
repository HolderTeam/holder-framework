from enum import StrEnum


class CardReferenceResolveDataStatus(StrEnum):
    AMBIGUOUS = "ambiguous"
    NOT_FOUND = "not_found"
    RESOLVED = "resolved"

    def __str__(self) -> str:
        return str(self.value)
