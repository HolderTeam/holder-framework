from enum import StrEnum


class GetCardsView(StrEnum):
    ALL = "all"
    RECENT = "recent"
    TREE = "tree"

    def __str__(self) -> str:
        return str(self.value)
