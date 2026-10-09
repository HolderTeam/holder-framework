"""Errors raised by the high-level Holder API."""


class HolderError(Exception):
    """Base error for the high-level client."""


class ConnectionError(HolderError):
    """Daemon discovery, startup or transport failed."""


class ClosedError(HolderError):
    """The client is outside its active context."""


class ProtocolError(HolderError):
    """The daemon returned an invalid or incompatible response."""


class APIError(HolderError):
    """A failed daemon request, with its status and error envelope."""

    def __init__(self, status: int, code: str, message: str) -> None:
        self.status = status
        self.code = code
        self.message = message
        super().__init__(f"{status} {code}: {message}")


class AuthenticationError(APIError):
    """The daemon rejected the credentials."""


class NotFoundError(APIError):
    """The requested object was not found within its scope."""
