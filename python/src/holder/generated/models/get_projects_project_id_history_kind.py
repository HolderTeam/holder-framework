from enum import StrEnum


class GetProjectsProjectIdHistoryKind(StrEnum):
    AI_DATA = "ai_data"
    CARD = "card"
    LOCATION = "location"
    PROJECT_SETTINGS = "project_settings"
    RESOURCE = "resource"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
