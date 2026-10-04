from enum import StrEnum


class ProjectEncryptionCheckResponseDataPrivacyMode(StrEnum):
    ENCRYPTED_GIT = "encrypted_git"
    PLAIN = "plain"

    def __str__(self) -> str:
        return str(self.value)
