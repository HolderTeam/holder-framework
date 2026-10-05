from enum import StrEnum


class ProjectGitTestRemoteResponseDataStatus(StrEnum):
    AUTH_FAILED = "auth_failed"
    INVALID_REMOTE_URL = "invalid_remote_url"
    NETWORK_ERROR = "network_error"
    NOT_FOUND = "not_found"
    REACHABLE = "reachable"
    REMOTE_UNSET = "remote_unset"
    UNKNOWN_ERROR = "unknown_error"

    def __str__(self) -> str:
        return str(self.value)
