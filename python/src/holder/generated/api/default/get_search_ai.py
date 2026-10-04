from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.search_messages_response import SearchMessagesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: str,
    q: str,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["project_id"] = project_id

    params["q"] = q

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/search/ai",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SearchMessagesResponse | None:
    if response.status_code == 200:
        response_200 = SearchMessagesResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | SearchMessagesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    q: str,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> Response[ErrorResponse | SearchMessagesResponse]:
    """Search AI messages

    Args:
        project_id (str):
        q (str):
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchMessagesResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        q=q,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    q: str,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> ErrorResponse | SearchMessagesResponse | None:
    """Search AI messages

    Args:
        project_id (str):
        q (str):
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchMessagesResponse
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        q=q,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    q: str,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> Response[ErrorResponse | SearchMessagesResponse]:
    """Search AI messages

    Args:
        project_id (str):
        q (str):
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchMessagesResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        q=q,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    q: str,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> ErrorResponse | SearchMessagesResponse | None:
    """Search AI messages

    Args:
        project_id (str):
        q (str):
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchMessagesResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            q=q,
            limit=limit,
            offset=offset,
        )
    ).parsed
