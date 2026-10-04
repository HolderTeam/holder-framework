from enum import StrEnum


class CardReferenceResolveDataMatchKind(StrEnum):
    EXACT_TITLE = "exact_title"
    FULL_ID = "full_id"
    ID_PREFIX = "id_prefix"

    def __str__(self) -> str:
        return str(self.value)
