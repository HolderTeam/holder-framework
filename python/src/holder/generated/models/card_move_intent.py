from enum import StrEnum


class CardMoveIntent(StrEnum):
    AFTER = "after"
    BEFORE = "before"
    INTO = "into"
    LEFT = "left"
    RIGHT = "right"
    TO_END = "to_end"
    TO_START = "to_start"
    UP_LEVEL = "up_level"

    def __str__(self) -> str:
        return str(self.value)
