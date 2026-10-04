from enum import StrEnum


class AssetImportJobStatus(StrEnum):
    COMMITTING = "committing"
    COMPLETED = "completed"
    FAILED = "failed"
    QUEUED = "queued"
    STAGING = "staging"
    STORING = "storing"

    def __str__(self) -> str:
        return str(self.value)
