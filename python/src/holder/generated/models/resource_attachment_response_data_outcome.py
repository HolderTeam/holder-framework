from enum import StrEnum


class ResourceAttachmentResponseDataOutcome(StrEnum):
    ALREADY_ATTACHED = "already_attached"
    ATTACHED = "attached"
    DETACHED = "detached"
    NOT_ATTACHED = "not_attached"

    def __str__(self) -> str:
        return str(self.value)
