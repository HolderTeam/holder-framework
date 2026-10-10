"""Connection and request handling for the synchronous Holder client."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Iterator
from typing import Any, Self

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    ClosedError,
    ConnectionError,
    NotFoundError,
    ProtocolError,
)
from .generated import AuthenticatedClient
from .generated.models import ErrorResponse
from .models.project import Project, ProjectCollection


class Holder:
    """Control your local knowledge, or connect with an explicit URL/token pair.

    Use as a context manager. Collection queries run only when consumed.
    Local discovery requires holderctl on PATH (or the holderctl argument).
    """

    def __init__(
        self,
        *,
        url: str | None = None,
        token: str | None = None,
        holderctl: str = "holderctl",
        timeout: float | httpx.Timeout = 10.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if (url is None) != (token is None):
            raise ValueError("Supply url and token together, or omit both")
        self._url = url
        self._token = token
        self._local = url is None
        self._holderctl = holderctl
        self._timeout = timeout
        self._transport = transport
        self._client: AuthenticatedClient | None = None
        self._closed = False
        self.projects = ProjectCollection(self)

    def _command(self, *args: str) -> str:
        try:
            result = subprocess.run(
                [self._holderctl, *args],
                capture_output=True,
                text=True,
                timeout=65,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise ConnectionError(
                "Could not run holderctl; install Holder or supply url and token"
            ) from None
        if result.returncode:
            # CLI output and stderr may contain local credentials; never echo them.
            raise ConnectionError(
                f"holderctl {args[0]} failed (exit {result.returncode})"
            )
        return result.stdout

    def _discover(self) -> None:
        try:
            result = json.loads(
                self._command(
                    "ensure",
                    "--json",
                    "--api-min",
                    "0.1",
                    "--api-max-exclusive",
                    "1.0",
                )
            )
            url = result["daemon"]["url"]
            if result.get("ok") is not True or not isinstance(url, str) or not url:
                raise ValueError
            token = self._command("token").strip()
            if not token:
                raise ValueError
        except (ValueError, KeyError, TypeError):
            raise ConnectionError(
                "holderctl did not return valid daemon connection details"
            ) from None
        self._url, self._token = url, token

    def _connect(self) -> None:
        if self._local:
            self._discover()
        self._client = AuthenticatedClient(
            base_url=self._url,
            token=self._token,
            timeout=httpx.Timeout(self._timeout),
            httpx_args={"transport": self._transport} if self._transport else {},
        )
        self._client.__enter__()

    def __enter__(self) -> Self:
        if self._closed or self._client is not None:
            raise ClosedError("Holder contexts cannot be reused")
        self._connect()
        return self

    def __exit__(self, *args: object) -> None:
        self._closed = True
        if self._client is not None:
            self._client.__exit__(*args)

    def _active(self) -> AuthenticatedClient:
        if self._closed or self._client is None:
            raise ClosedError("Use Holder inside with Holder(...) as h")
        return self._client

    def __iter__(self) -> Iterator[Project]:
        return iter(self.projects)

    def _call(
        self, endpoint: Any, *args: Any, write: bool = False, **kwargs: Any
    ) -> Any:
        client = self._active()
        for attempt in range(2):
            try:
                response = endpoint.sync_detailed(*args, client=client, **kwargs)
            except httpx.TransportError:
                raise ConnectionError(
                    "Could not communicate with the Holder daemon"
                ) from None
            except (ValueError, KeyError, TypeError):
                raise ProtocolError("Invalid daemon response") from None
            if (
                response.status_code == 401
                and self._local
                and not write
                and attempt == 0
            ):
                self._discover()
                # Preserve the pool and custom transport while updating a restarted daemon.
                http_client = client.get_httpx_client()
                http_client.base_url = self._url
                http_client.headers["Authorization"] = f"Bearer {self._token}"
                continue
            if isinstance(response.parsed, ErrorResponse):
                error = response.parsed.error
                error_type = {401: AuthenticationError, 404: NotFoundError}.get(
                    response.status_code, APIError
                )
                raise error_type(int(response.status_code), error.code, error.message)
            if response.status_code >= 400:
                error_type = {401: AuthenticationError, 404: NotFoundError}.get(
                    response.status_code, APIError
                )
                # Undocumented statuses are not parsed by generated endpoints.
                try:
                    error = ErrorResponse.from_dict(json.loads(response.content)).error
                except (ValueError, KeyError, TypeError, AttributeError):
                    error = None
                if error is not None:
                    raise error_type(
                        int(response.status_code), error.code, error.message
                    )
                raise error_type(
                    int(response.status_code), "http_error", "Daemon request failed"
                )
            if (
                response.parsed is None
                or getattr(response.parsed, "ok", None) is not True
            ):
                raise ProtocolError("Invalid daemon success envelope")
            return response.parsed.data
        raise AuthenticationError(
            401, "unauthorized", "Daemon rejected refreshed credentials"
        )
