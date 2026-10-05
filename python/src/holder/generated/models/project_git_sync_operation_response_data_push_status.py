from enum import StrEnum


class ProjectGitSyncOperationResponseDataPushStatus(StrEnum):
    AUTH_FAILED = "auth_failed"
    NETWORK_ERROR = "network_error"
    NON_FAST_FORWARD = "non_fast_forward"
    NOT_FOUND = "not_found"
    PUSHED = "pushed"
    REMOTE_UNSET = "remote_unset"
    UNKNOWN_ERROR = "unknown_error"
    UP_TO_DATE = "up_to_date"

    def __str__(self) -> str:
        return str(self.value)
