from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    run_id: str,
    *,
    last_event_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(last_event_id, Unset):
        headers["Last-Event-ID"] = last_event_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ai/runs/{run_id}/events".format(
            run_id=quote(str(run_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 405:
        response_405 = ErrorResponse.from_dict(response.json())

        return response_405

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Stream run events (SSE)

     Replays bounded retained run events with absolute event IDs; done or failed closes the stream.
    Missing in-memory history can recover persisted terminal status. An expired or foreign cursor emits
    resync_required; fetch the run before reconnecting.

    Args:
        run_id (str):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        run_id=run_id,
        last_event_id=last_event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    run_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Stream run events (SSE)

     Replays bounded retained run events with absolute event IDs; done or failed closes the stream.
    Missing in-memory history can recover persisted terminal status. An expired or foreign cursor emits
    resync_required; fetch the run before reconnecting.

    Args:
        run_id (str):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return sync_detailed(
        run_id=run_id,
        client=client,
        last_event_id=last_event_id,
    ).parsed


async def asyncio_detailed(
    run_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Stream run events (SSE)

     Replays bounded retained run events with absolute event IDs; done or failed closes the stream.
    Missing in-memory history can recover persisted terminal status. An expired or foreign cursor emits
    resync_required; fetch the run before reconnecting.

    Args:
        run_id (str):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        run_id=run_id,
        last_event_id=last_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    run_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Stream run events (SSE)

     Replays bounded retained run events with absolute event IDs; done or failed closes the stream.
    Missing in-memory history can recover persisted terminal status. An expired or foreign cursor emits
    resync_required; fetch the run before reconnecting.

    Args:
        run_id (str):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            run_id=run_id,
            client=client,
            last_event_id=last_event_id,
        )
    ).parsed
