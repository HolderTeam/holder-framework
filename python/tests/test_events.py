"""SSE framing tests and delayed delivery over real loopback HTTP connections."""

import asyncio
from contextlib import asynccontextmanager

import httpx
import pytest

from holder.events import ChangeStream, Event
from holder.generated import AuthenticatedClient


class ByteStream(httpx.AsyncByteStream):
    def __init__(self, chunks):
        self.chunks = chunks
        self.closed = False

    async def __aiter__(self):
        for chunk in self.chunks:
            if isinstance(chunk, Exception):
                raise chunk
            yield chunk

    async def aclose(self):
        self.closed = True


def client_for(handler):
    return AuthenticatedClient(
        base_url="http://holder.test",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )


def test_framing_utf8_comments_multiline_and_incomplete_eof():
    async def run():
        payload = (
            "\ufeff: heartbeat\r\nid: opaque:1\r\nevent: card.changed\r\n"
            'data: {"title":\r\ndata: "café\u2028line"}\r\n\r\n'
            "id: ignored\n\ndata: plain\nid: bad\x00id\n\n"
            "id: incomplete\ndata: not-delivered"
        ).encode()
        body = ByteStream([bytes([b]) for b in payload])
        async with client_for(
            lambda request: httpx.Response(
                200,
                stream=body,
                headers={"Content-Type": "text/event-stream"},
            )
        ) as client:
            async with ChangeStream(client, reconnect_delay=100) as events:
                event = await anext(events)
                assert event == Event(
                    "card.changed", '{"title":\n"café\u2028line"}', "opaque:1"
                )
                assert event.json() == {"title": "café\u2028line"}
                assert events.cursor is None
                assert await anext(events) == Event("message", "plain")
                assert events.cursor == "opaque:1"
                pending = asyncio.create_task(anext(events))
                await asyncio.sleep(0)
                await events.aclose()
                with pytest.raises(asyncio.CancelledError):
                    await pending
                assert events.cursor == "opaque:1"
            assert body.closed
            assert not client.get_async_httpx_client().is_closed
        assert client.get_async_httpx_client().is_closed

    asyncio.run(run())


def test_interrupted_replay_keeps_ready_id_and_discards_partial_frame():
    async def run():
        bodies = [
            ByteStream(
                [
                    b'id: old:1\nevent: ready\ndata: {"cursor":"new:9"}\n\n',
                    b"id: old:2\nevent: card.changed\ndata: {}\n\n",
                    b"id: old:3\ndata: partial",
                    httpx.ReadError("disconnected"),
                ]
            ),
            ByteStream(
                [
                    b'id: old:2\nevent: ready\ndata: {"cursor":"new:9"}\n\n',
                    b"id: old:3\nevent: card.changed\ndata: {}\n\n",
                    b'id: new:9\nevent: resync_required\ndata: {"reason":"history_unavailable"}\n\n',
                ]
            ),
        ]
        requests = []

        def respond(request):
            assert request.headers["Authorization"] == "Bearer test-token"
            assert request.headers["Accept"] == "text/event-stream"
            assert dict(request.url.params) == {
                "project_id": "project & one",
                "last_revision": "a" * 40,
            }
            requests.append(request)
            return httpx.Response(
                200,
                stream=bodies[len(requests) - 1],
                headers={"Content-Type": "text/event-stream"},
            )

        async with (
            client_for(respond) as client,
            ChangeStream(
                client,
                project_id="project & one",
                last_revision="a" * 40,
                last_event_id="old:1",
                reconnect_delay=0,
            ) as events,
        ):
            assert (await anext(events)).event == "ready"
            assert (await anext(events)).id == "old:2"
            assert events.cursor == "old:1"
            assert (await anext(events)).event == "ready"
            assert events.cursor == "old:2"
            assert requests[1].headers["Last-Event-ID"] == "old:2"
            assert bodies[0].closed
            assert (await anext(events)).id == "old:3"
            assert (await anext(events)).event == "resync_required"
            assert events.cursor == "old:3"
            assert bodies[1].closed
            with pytest.raises(StopAsyncIteration):
                await anext(events)
        assert len(requests) == 2

    asyncio.run(run())


@asynccontextmanager
async def server_for(handler):
    tasks = set()
    failures = []

    async def serve(reader, writer):
        task = asyncio.current_task()
        tasks.add(task)
        try:
            request = await reader.readuntil(b"\r\n\r\n")
            writer.write(
                b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\nConnection: close\r\n\r\n"
            )
            await writer.drain()
            await handler(request, reader, writer)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - fail the test for server task errors
            failures.append(exc)
        finally:
            writer.close()
            await writer.wait_closed()
            tasks.remove(task)

    server = await asyncio.start_server(serve, "127.0.0.1", 0)
    try:
        yield f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
    finally:
        server.close()
        await server.wait_closed()
        remaining = list(tasks)
        for task in remaining:
            task.cancel()
        await asyncio.gather(*remaining, return_exceptions=True)
        assert not failures


@pytest.mark.parametrize("stop", ["cancel", "close", "break"])
def test_delayed_delivery_and_socket_cleanup(stop):
    async def run():
        release = asyncio.Event()
        disconnected = asyncio.Event()

        async def handler(request, reader, writer):
            assert b"Authorization: Bearer test-token" in request
            writer.write(b"id: p:1\nevent: ready\ndata: {}\n\n")
            await writer.drain()
            await release.wait()
            writer.write(b"id: p:2\nevent: card.changed\ndata: {}\n\n")
            await writer.drain()
            assert await reader.read() == b""
            disconnected.set()

        async with (
            server_for(handler) as url,
            AuthenticatedClient(base_url=url, token="test-token") as client,
        ):
            async with ChangeStream(client) as events:
                # The server cannot deliver its second frame until this arrives.
                assert (await asyncio.wait_for(anext(events), 2)).id == "p:1"
                pending = asyncio.create_task(anext(events))
                await asyncio.sleep(0.05)
                assert not pending.done()
                release.set()
                assert (await asyncio.wait_for(pending, 2)).id == "p:2"
                if stop != "break":
                    pending = asyncio.create_task(anext(events))
                    await asyncio.sleep(0.05)
                    if stop == "cancel":
                        pending.cancel()
                    else:
                        await events.aclose()
                    with pytest.raises(asyncio.CancelledError):
                        await pending
            await asyncio.wait_for(disconnected.wait(), 2)
            assert not client.get_async_httpx_client().is_closed

    asyncio.run(run())


def test_eof_reconnect_on_real_socket():
    async def run():
        requests = []
        disconnected = asyncio.Event()

        async def handler(request, reader, writer):
            requests.append(request)
            if len(requests) == 1:
                writer.write(
                    b"id: p:1\nevent: card.changed\ndata: {}\n\nid: p:2\ndata: partial"
                )
                await writer.drain()
                return
            assert b"Last-Event-ID: p:1" in request
            writer.write(b'id: p:2\nevent: card.changed\ndata: {"replay":true}\n\n')
            await writer.drain()
            assert await reader.read() == b""
            disconnected.set()

        async with (
            server_for(handler) as url,
            AuthenticatedClient(base_url=url, token="test-token") as client,
        ):
            async with ChangeStream(client, reconnect_delay=0) as events:
                assert (await asyncio.wait_for(anext(events), 2)).id == "p:1"
                event = await asyncio.wait_for(anext(events), 2)
                assert event.id == "p:2" and event.json() == {"replay": True}
            await asyncio.wait_for(disconnected.wait(), 2)
        assert len(requests) == 2

    asyncio.run(run())


@pytest.mark.parametrize(
    "status,content_type,error",
    [
        (400, "application/json", httpx.HTTPStatusError),
        (401, "application/json", httpx.HTTPStatusError),
        (503, "application/json", httpx.HTTPStatusError),
        (200, "application/json", ValueError),
    ],
)
def test_http_and_protocol_errors_close_without_retry(status, content_type, error):
    async def run():
        body = ByteStream([b"{}"])
        async with (
            client_for(
                lambda request: httpx.Response(
                    status, stream=body, headers={"Content-Type": content_type}
                )
            ) as client,
            ChangeStream(client) as events,
        ):
            with pytest.raises(error):
                await anext(events)
            assert body.closed
            with pytest.raises(StopAsyncIteration):
                await anext(events)

    asyncio.run(run())


@pytest.mark.parametrize("phase", ["read", "eof"])
def test_repeated_cancellation_waits_for_response_cleanup(phase):
    async def run():
        reading = asyncio.Event()
        closing = asyncio.Event()
        finish_close = asyncio.Event()

        class SlowStream(httpx.AsyncByteStream):
            closed = False

            async def __aiter__(self):
                reading.set()
                if phase == "read":
                    await asyncio.Event().wait()
                yield b""

            async def aclose(self):
                closing.set()
                await finish_close.wait()
                self.closed = True

        body = SlowStream()
        async with (
            client_for(
                lambda request: httpx.Response(
                    200,
                    stream=body,
                    headers={"Content-Type": "text/event-stream"},
                )
            ) as client,
            ChangeStream(client) as events,
        ):
            pending = asyncio.create_task(anext(events))
            await asyncio.wait_for(reading.wait(), 2)
            if phase == "eof":
                await asyncio.wait_for(closing.wait(), 2)
            pending.cancel()
            await asyncio.wait_for(closing.wait(), 2)
            pending.cancel()
            await asyncio.sleep(0)
            assert not body.closed
            assert not pending.done()
            finish_close.set()
            with pytest.raises(asyncio.CancelledError):
                await pending
            assert body.closed
            assert events.cursor is None

    asyncio.run(run())


def test_cancellation_during_reconnect_delay_and_connect_failure():
    async def run():
        failed = asyncio.Event()
        requests = []

        def respond(request):
            requests.append(request)
            failed.set()
            raise httpx.ConnectError("offline", request=request)

        async with (
            client_for(respond) as client,
            ChangeStream(client, reconnect_delay=100) as events,
        ):
            pending = asyncio.create_task(anext(events))
            await asyncio.wait_for(failed.wait(), 2)
            await asyncio.sleep(0)
            await events.aclose()
            with pytest.raises(asyncio.CancelledError):
                await pending
            assert len(requests) == 1

    asyncio.run(run())


def test_consumer_exception_closes_response_without_acknowledging_event():
    async def run():
        body = ByteStream([b"id: p:1\ndata: {}\n\n"])
        async with client_for(
            lambda request: httpx.Response(
                200,
                stream=body,
                headers={"Content-Type": "text/event-stream"},
            )
        ) as client:
            with pytest.raises(ValueError, match="consumer"):
                async with ChangeStream(client, last_event_id="p:0") as events:
                    assert (await anext(events)).id == "p:1"
                    raise ValueError("consumer")
            assert body.closed
            assert events.cursor == "p:0"

    asyncio.run(run())
