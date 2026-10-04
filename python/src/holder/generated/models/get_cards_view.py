from enum import StrEnum


class GetCardsView(StrEnum):
    RECENT = "recent"
    TREE = "tree"

    def __str__(self) -> str:
        return str(self.value)
