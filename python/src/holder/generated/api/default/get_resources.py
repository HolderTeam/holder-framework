from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.resource_list_response import ResourceListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    card_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    project_id: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["card_id"] = card_id

    params["limit"] = limit

    params["offset"] = offset

    params["project_id"] = project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/resources",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ResourceListResponse | None:
    if response.status_code == 200:
        response_200 = ResourceListResponse.from_dict(response.json())

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

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | ResourceListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    card_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    project_id: str,
) -> Response[ErrorResponse | ResourceListResponse]:
    """List project resources or attachments to a live card

     With card_id, returns an authoritative live-card attachment join in updated_at descending,
    resource_id ascending order. Without card_id, preserves the unpaginated project resource list.
    Detach preserves project resources; delete removes them globally.

    Args:
        card_id (str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ResourceListResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        limit=limit,
        offset=offset,
        project_id=project_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    card_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    project_id: str,
) -> ErrorResponse | ResourceListResponse | None:
    """List project resources or attachments to a live card

     With card_id, returns an authoritative live-card attachment join in updated_at descending,
    resource_id ascending order. Without card_id, preserves the unpaginated project resource list.
    Detach preserves project resources; delete removes them globally.

    Args:
        card_id (str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ResourceListResponse
    """

    return sync_detailed(
        client=client,
        card_id=card_id,
        limit=limit,
        offset=offset,
        project_id=project_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    card_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    project_id: str,
) -> Response[ErrorResponse | ResourceListResponse]:
    """List project resources or attachments to a live card

     With card_id, returns an authoritative live-card attachment join in updated_at descending,
    resource_id ascending order. Without card_id, preserves the unpaginated project resource list.
    Detach preserves project resources; delete removes them globally.

    Args:
        card_id (str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ResourceListResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        limit=limit,
        offset=offset,
        project_id=project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    card_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    project_id: str,
) -> ErrorResponse | ResourceListResponse | None:
    """List project resources or attachments to a live card

     With card_id, returns an authoritative live-card attachment join in updated_at descending,
    resource_id ascending order. Without card_id, preserves the unpaginated project resource list.
    Detach preserves project resources; delete removes them globally.

    Args:
        card_id (str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ResourceListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            card_id=card_id,
            limit=limit,
            offset=offset,
            project_id=project_id,
        )
    ).parsed
