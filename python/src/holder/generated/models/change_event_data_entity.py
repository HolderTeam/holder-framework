from enum import StrEnum


class ChangeEventDataEntity(StrEnum):
    CARD = "card"
    LOCATION = "location"
    MESSAGE = "message"
    PROJECT = "project"
    RESOURCE = "resource"
    RUN = "run"
    THREAD = "thread"

    def __str__(self) -> str:
        return str(self.value)
