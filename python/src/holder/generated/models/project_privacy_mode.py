from enum import StrEnum


class ProjectPrivacyMode(StrEnum):
    ENCRYPTED_GIT = "encrypted_git"
    PLAIN = "plain"

    def __str__(self) -> str:
        return str(self.value)
