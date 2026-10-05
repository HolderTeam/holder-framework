from enum import StrEnum


class CardContextBreadcrumbType(StrEnum):
    CARD = "card"
    PROJECT = "project"

    def __str__(self) -> str:
        return str(self.value)
