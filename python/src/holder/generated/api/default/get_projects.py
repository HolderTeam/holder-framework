from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_projects_order import GetProjectsOrder
from ...models.project_list_response import ProjectListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: str | Unset = UNSET,
    updated_after: int | Unset = UNSET,
    updated_before: int | Unset = UNSET,
    order: GetProjectsOrder | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    count: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["name"] = name

    params["updated_after"] = updated_after

    params["updated_before"] = updated_before

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["limit"] = limit

    params["offset"] = offset

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ProjectListResponse | None:
    if response.status_code == 200:
        response_200 = ProjectListResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | ProjectListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    name: str | Unset = UNSET,
    updated_after: int | Unset = UNSET,
    updated_before: int | Unset = UNSET,
    order: GetProjectsOrder | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    count: bool | Unset = False,
) -> Response[ErrorResponse | ProjectListResponse]:
    """List projects

    Args:
        name (str | Unset):
        updated_after (int | Unset):
        updated_before (int | Unset):
        order (GetProjectsOrder | Unset):
        limit (int | Unset):
        offset (int | Unset):
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ProjectListResponse]
    """

    kwargs = _get_kwargs(
        name=name,
        updated_after=updated_after,
        updated_before=updated_before,
        order=order,
        limit=limit,
        offset=offset,
        count=count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    name: str | Unset = UNSET,
    updated_after: int | Unset = UNSET,
    updated_before: int | Unset = UNSET,
    order: GetProjectsOrder | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    count: bool | Unset = False,
) -> ErrorResponse | ProjectListResponse | None:
    """List projects

    Args:
        name (str | Unset):
        updated_after (int | Unset):
        updated_before (int | Unset):
        order (GetProjectsOrder | Unset):
        limit (int | Unset):
        offset (int | Unset):
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ProjectListResponse
    """

    return sync_detailed(
        client=client,
        name=name,
        updated_after=updated_after,
        updated_before=updated_before,
        order=order,
        limit=limit,
        offset=offset,
        count=count,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    name: str | Unset = UNSET,
    updated_after: int | Unset = UNSET,
    updated_before: int | Unset = UNSET,
    order: GetProjectsOrder | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    count: bool | Unset = False,
) -> Response[ErrorResponse | ProjectListResponse]:
    """List projects

    Args:
        name (str | Unset):
        updated_after (int | Unset):
        updated_before (int | Unset):
        order (GetProjectsOrder | Unset):
        limit (int | Unset):
        offset (int | Unset):
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ProjectListResponse]
    """

    kwargs = _get_kwargs(
        name=name,
        updated_after=updated_after,
        updated_before=updated_before,
        order=order,
        limit=limit,
        offset=offset,
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    name: str | Unset = UNSET,
    updated_after: int | Unset = UNSET,
    updated_before: int | Unset = UNSET,
    order: GetProjectsOrder | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    count: bool | Unset = False,
) -> ErrorResponse | ProjectListResponse | None:
    """List projects

    Args:
        name (str | Unset):
        updated_after (int | Unset):
        updated_before (int | Unset):
        order (GetProjectsOrder | Unset):
        limit (int | Unset):
        offset (int | Unset):
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ProjectListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            updated_after=updated_after,
            updated_before=updated_before,
            order=order,
            limit=limit,
            offset=offset,
            count=count,
        )
    ).parsed
