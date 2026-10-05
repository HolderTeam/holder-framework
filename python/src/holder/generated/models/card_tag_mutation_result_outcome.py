from enum import StrEnum


class CardTagMutationResultOutcome(StrEnum):
    ADDED = "added"
    ALREADY_PRESENT = "already_present"
    NOT_PRESENT = "not_present"
    PRESENT_OUTSIDE_EDITABLE_TAG_LINE = "present_outside_editable_tag_line"
    REMOVED = "removed"

    def __str__(self) -> str:
        return str(self.value)
