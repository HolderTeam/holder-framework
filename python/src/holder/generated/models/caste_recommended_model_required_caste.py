from enum import StrEnum


class CasteRecommendedModelRequiredCaste(StrEnum):
    DEVELOPER = "developer"
    MINI = "mini"
    RIG = "rig"
    USER = "user"
    WORKSTATION = "workstation"

    def __str__(self) -> str:
        return str(self.value)
