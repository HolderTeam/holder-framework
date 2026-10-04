from enum import StrEnum


class CardHistoryDiffLineOrigin(StrEnum):
    VALUE_0 = " "
    VALUE_1 = "+"
    VALUE_2 = "-"

    def __str__(self) -> str:
        return str(self.value)
