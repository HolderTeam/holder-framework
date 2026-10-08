from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: str | Unset = UNSET,
    last_revision: str | Unset = UNSET,
    last_event_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(last_event_id, Unset):
        headers["Last-Event-ID"] = last_event_id

    params: dict[str, Any] = {}

    params["project_id"] = project_id

    params["last_revision"] = last_revision

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/events",
        "params": params,
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
    *,
    client: AuthenticatedClient | Client,
    project_id: str | Unset = UNSET,
    last_revision: str | Unset = UNSET,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Subscribe to committed daemon state changes (SSE)

     Sends ready, then project.changed, card.changed, resource.changed,
    location.changed, thread.changed, message.changed and run.changed invalidations.
    Intermediate states can coalesce. Each frame has an opaque id and JSON data.
    Without a cursor starts at the current tail. Last-Event-ID replays bounded
    in-memory history. Restart, an expired cursor or last_revision without a
    replayable cursor returns resync_required with current Git revisions and
    history URLs, then closes. This endpoint does not synthesize events from Git.
    Refresh current state on resync; Git is the durable project history.
    Comments provide heartbeats. Disconnecting unsubscribes without cancelling jobs.

    Args:
        project_id (str | Unset):
        last_revision (str | Unset):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        last_revision=last_revision,
        last_event_id=last_event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    project_id: str | Unset = UNSET,
    last_revision: str | Unset = UNSET,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Subscribe to committed daemon state changes (SSE)

     Sends ready, then project.changed, card.changed, resource.changed,
    location.changed, thread.changed, message.changed and run.changed invalidations.
    Intermediate states can coalesce. Each frame has an opaque id and JSON data.
    Without a cursor starts at the current tail. Last-Event-ID replays bounded
    in-memory history. Restart, an expired cursor or last_revision without a
    replayable cursor returns resync_required with current Git revisions and
    history URLs, then closes. This endpoint does not synthesize events from Git.
    Refresh current state on resync; Git is the durable project history.
    Comments provide heartbeats. Disconnecting unsubscribes without cancelling jobs.

    Args:
        project_id (str | Unset):
        last_revision (str | Unset):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        last_revision=last_revision,
        last_event_id=last_event_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: str | Unset = UNSET,
    last_revision: str | Unset = UNSET,
    last_event_id: str | Unset = UNSET,
) -> Response[ErrorResponse | str]:
    """Subscribe to committed daemon state changes (SSE)

     Sends ready, then project.changed, card.changed, resource.changed,
    location.changed, thread.changed, message.changed and run.changed invalidations.
    Intermediate states can coalesce. Each frame has an opaque id and JSON data.
    Without a cursor starts at the current tail. Last-Event-ID replays bounded
    in-memory history. Restart, an expired cursor or last_revision without a
    replayable cursor returns resync_required with current Git revisions and
    history URLs, then closes. This endpoint does not synthesize events from Git.
    Refresh current state on resync; Git is the durable project history.
    Comments provide heartbeats. Disconnecting unsubscribes without cancelling jobs.

    Args:
        project_id (str | Unset):
        last_revision (str | Unset):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        last_revision=last_revision,
        last_event_id=last_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    project_id: str | Unset = UNSET,
    last_revision: str | Unset = UNSET,
    last_event_id: str | Unset = UNSET,
) -> ErrorResponse | str | None:
    """Subscribe to committed daemon state changes (SSE)

     Sends ready, then project.changed, card.changed, resource.changed,
    location.changed, thread.changed, message.changed and run.changed invalidations.
    Intermediate states can coalesce. Each frame has an opaque id and JSON data.
    Without a cursor starts at the current tail. Last-Event-ID replays bounded
    in-memory history. Restart, an expired cursor or last_revision without a
    replayable cursor returns resync_required with current Git revisions and
    history URLs, then closes. This endpoint does not synthesize events from Git.
    Refresh current state on resync; Git is the durable project history.
    Comments provide heartbeats. Disconnecting unsubscribes without cancelling jobs.

    Args:
        project_id (str | Unset):
        last_revision (str | Unset):
        last_event_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            last_revision=last_revision,
            last_event_id=last_event_id,
        )
    ).parsed
