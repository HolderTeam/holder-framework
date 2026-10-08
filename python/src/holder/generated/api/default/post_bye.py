from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bye_response import ByeResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/bye",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ByeResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = ByeResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ByeResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ByeResponse | ErrorResponse]:
    """Say that this client is leaving

     A hint, never a command. A daemon started with `--idle-exit` normally waits out its whole idle
    period after the last client has gone; after this request it waits only a few seconds (3), and only
    while nothing else happens. Running work, an open event stream, a new connection or any other
    request keeps it running, so another client is never cut off by one client leaving. A daemon without
    `--idle-exit`, such as the systemd service, ignores it. There is no request body, and nothing is
    returned beyond acknowledgement. Clients call it best-effort as they close; a client that crashes
    simply never does, and the daemon then falls back to its idle period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ByeResponse | ErrorResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ByeResponse | ErrorResponse | None:
    """Say that this client is leaving

     A hint, never a command. A daemon started with `--idle-exit` normally waits out its whole idle
    period after the last client has gone; after this request it waits only a few seconds (3), and only
    while nothing else happens. Running work, an open event stream, a new connection or any other
    request keeps it running, so another client is never cut off by one client leaving. A daemon without
    `--idle-exit`, such as the systemd service, ignores it. There is no request body, and nothing is
    returned beyond acknowledgement. Clients call it best-effort as they close; a client that crashes
    simply never does, and the daemon then falls back to its idle period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ByeResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ByeResponse | ErrorResponse]:
    """Say that this client is leaving

     A hint, never a command. A daemon started with `--idle-exit` normally waits out its whole idle
    period after the last client has gone; after this request it waits only a few seconds (3), and only
    while nothing else happens. Running work, an open event stream, a new connection or any other
    request keeps it running, so another client is never cut off by one client leaving. A daemon without
    `--idle-exit`, such as the systemd service, ignores it. There is no request body, and nothing is
    returned beyond acknowledgement. Clients call it best-effort as they close; a client that crashes
    simply never does, and the daemon then falls back to its idle period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ByeResponse | ErrorResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ByeResponse | ErrorResponse | None:
    """Say that this client is leaving

     A hint, never a command. A daemon started with `--idle-exit` normally waits out its whole idle
    period after the last client has gone; after this request it waits only a few seconds (3), and only
    while nothing else happens. Running work, an open event stream, a new connection or any other
    request keeps it running, so another client is never cut off by one client leaving. A daemon without
    `--idle-exit`, such as the systemd service, ignores it. There is no request body, and nothing is
    returned beyond acknowledgement. Clients call it best-effort as they close; a client that crashes
    simply never does, and the daemon then falls back to its idle period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ByeResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
