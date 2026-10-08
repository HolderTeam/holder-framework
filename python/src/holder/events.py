"""Incremental asyncio transport for GET /events; no entity or recovery policy."""

import asyncio
import json
import math
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Self

import httpx

from .generated import AuthenticatedClient, Client


@dataclass(frozen=True)
class Event:
    """A complete SSE frame. IDs are opaque; data is retained as UTF-8 text."""

    event: str
    data: str
    id: str | None = None

    def json(self) -> Any:
        return json.loads(self.data)


async def _lines(response: httpx.Response) -> AsyncIterator[str]:
    # SSE recognizes only CR and LF, not Unicode separators inside JSON strings.
    response.encoding = "utf-8"
    line: list[str] = []
    after_cr = False
    async for chunk in response.aiter_text():
        for character in chunk:
            if after_cr and character == "\n":
                after_cr = False
                continue
            after_cr = character == "\r"
            if character in "\r\n":
                yield "".join(line)
                line.clear()
            else:
                line.append(character)
    # No synthetic newline at EOF: partial frames must replay after reconnect.


async def _frames(response: httpx.Response) -> AsyncIterator[Event]:
    data: list[str] = []
    name = "message"
    event_id = None
    first = True
    async for line in _lines(response):
        if first:
            line = line.removeprefix("\ufeff")
            first = False
        if not line:
            if data:
                yield Event(name, "\n".join(data), event_id)
            data, name, event_id = [], "message", None
            continue
        if line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        value = value.removeprefix(" ")
        if field == "data":
            data.append(value)
        elif field == "event":
            name = value or "message"
        elif field == "id" and "\x00" not in value:
            event_id = value
    # An unterminated frame is not delivered or acknowledged on disconnect.


class _ClosingStream(httpx.AsyncByteStream):
    """Protect cleanup both at HTTPX's automatic EOF close and context exit."""

    def __init__(self, stream: httpx.AsyncByteStream) -> None:
        self._stream = stream
        self._cleanup: asyncio.Task[None] | None = None

    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for chunk in self._stream:
            yield chunk

    async def aclose(self) -> None:
        if self._cleanup is None:
            self._cleanup = asyncio.create_task(self._stream.aclose())
        cleanup = self._cleanup
        # A second task cancellation must not interrupt socket/pool cleanup.
        cancelled = False
        while not cleanup.done():
            try:
                await asyncio.shield(cleanup)
            except asyncio.CancelledError:
                cancelled = True
        cleanup.result()
        if cancelled:
            raise asyncio.CancelledError


@asynccontextmanager
async def _connection(
    transport: httpx.AsyncClient, **kwargs: Any
) -> AsyncIterator[httpx.Response]:
    request = transport.build_request("GET", "/events", **kwargs)
    response = await transport.send(request, stream=True)
    response.stream = _ClosingStream(response.stream)
    try:
        yield response
    finally:
        await response.aclose()


class ChangeStream:
    """Context-managed asyncio iterator over daemon invalidations.

    Pass the same project filter used for /events/cursor. cursor advances when
    the consumer requests the next event (after processing the previous one).
    Persist cursor for a later subscription. A ready frame uses its ID, never
    the newer checkpoint in its data. resync_required is yielded once and stops
    iteration without advancing cursor: refresh state before subscribing again.

    EOF and HTTPX transport errors reconnect after reconnect_delay seconds.
    HTTP errors and invalid content types propagate without retry. Read timeout
    defaults to disabled; connection/write/pool timeouts remain bounded.
    Cancellation, aclose(), and context exit close the active response. The
    supplied generated client remains caller-owned. Use asyncio task cancellation
    or aclose() to interrupt a pending read; only one reader is supported.
    """

    def __init__(
        self,
        client: Client | AuthenticatedClient,
        *,
        project_id: str | None = None,
        last_revision: str | None = None,
        last_event_id: str | None = None,
        reconnect_delay: float = 1.0,
        timeout: httpx.Timeout | None = None,
    ) -> None:
        if not math.isfinite(reconnect_delay) or reconnect_delay < 0:
            raise ValueError("reconnect_delay must be finite and nonnegative")
        self.cursor = last_event_id
        self._client = client
        self._params = {
            key: value
            for key, value in {
                "project_id": project_id,
                "last_revision": last_revision,
            }.items()
            if value is not None
        }
        self._delay = reconnect_delay
        self._timeout = timeout if timeout is not None else httpx.Timeout(10, read=None)
        self._iterator = self._events()
        self._pending: asyncio.Task[Event] | None = None
        self._entered = False
        self._closed = False

    async def __aenter__(self) -> Self:
        if self._entered or self._closed:
            raise RuntimeError("ChangeStream contexts cannot be reused")
        self._entered = True
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Event:
        if not self._entered:
            raise RuntimeError("Use ChangeStream inside async with")
        if self._closed:
            raise StopAsyncIteration
        if self._pending is not None:
            raise RuntimeError("ChangeStream supports only one reader")
        pending = asyncio.create_task(anext(self._iterator))
        self._pending = pending
        try:
            return await pending
        except BaseException:
            self._closed = True
            await self._iterator.aclose()
            raise
        finally:
            self._pending = None

    async def aclose(self) -> None:
        """Stop iteration, including a blocked read or reconnect delay."""
        self._closed = True
        pending = self._pending
        if pending is not None:
            pending.cancel()
            try:
                await pending
            except (asyncio.CancelledError, StopAsyncIteration):
                pass
        await self._iterator.aclose()

    async def _events(self) -> AsyncIterator[Event]:
        transport = self._client.get_async_httpx_client()
        while not self._closed:
            headers = {
                "Accept": "text/event-stream",
                "Last-Event-ID": self.cursor or "",
            }
            terminal = None
            try:
                async with _connection(
                    transport,
                    params=self._params,
                    headers=headers,
                    timeout=self._timeout,
                ) as response:
                    response.raise_for_status()
                    if (
                        response.headers.get("content-type", "")
                        .split(";")[0]
                        .strip()
                        .lower()
                        != "text/event-stream"
                    ):
                        raise ValueError("Expected text/event-stream response")
                    async for event in _frames(response):
                        if event.event == "resync_required":
                            terminal = event
                            break
                        yield event
                        if event.id is not None:
                            self.cursor = event.id or None
            except httpx.TransportError:
                pass
            if terminal is not None:
                yield terminal
                return
            await asyncio.sleep(self._delay)
