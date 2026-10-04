from enum import StrEnum


class GetProjectsProjectIdHistoryCardsCardIdCompareMode(StrEnum):
    CHANGE = "change"
    SINCE = "since"

    def __str__(self) -> str:
        return str(self.value)
