from enum import StrEnum


class ProjectGitSyncOperationResponseDataPullStatus(StrEnum):
    FAILED = "failed"
    NOT_ATTEMPTED = "not_attempted"
    REMOTE_UNSET = "remote_unset"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
