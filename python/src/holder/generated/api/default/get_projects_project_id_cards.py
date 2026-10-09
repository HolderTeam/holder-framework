from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_page_response import CardPageResponse
from ...models.error_response import ErrorResponse
from ...models.get_projects_project_id_cards_order import GetProjectsProjectIdCardsOrder
from ...models.get_projects_project_id_cards_parent_type_0 import (
    GetProjectsProjectIdCardsParentType0,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    tag: str | Unset = UNSET,
    parent: GetProjectsProjectIdCardsParentType0 | Unset | UUID = UNSET,
    include_deleted: bool | Unset = False,
    order: GetProjectsProjectIdCardsOrder
    | Unset = GetProjectsProjectIdCardsOrder.CARD_ID_ASC,
    limit: int | Unset = 200,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["tag"] = tag

    json_parent: str | Unset
    if isinstance(parent, Unset):
        json_parent = UNSET
    elif isinstance(parent, GetProjectsProjectIdCardsParentType0):
        json_parent = parent.value
    else:
        json_parent = str(parent)

    params["parent"] = json_parent

    params["include_deleted"] = include_deleted

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/cards".format(
            project_id=quote(str(project_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardPageResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardPageResponse.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CardPageResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    tag: str | Unset = UNSET,
    parent: GetProjectsProjectIdCardsParentType0 | Unset | UUID = UNSET,
    include_deleted: bool | Unset = False,
    order: GetProjectsProjectIdCardsOrder
    | Unset = GetProjectsProjectIdCardsOrder.CARD_ID_ASC,
    limit: int | Unset = 200,
    cursor: str | Unset = UNSET,
) -> Response[CardPageResponse | ErrorResponse]:
    """Page through a project's cards

     Filters combine. Each page reads current data; iteration is not a snapshot.

    Args:
        project_id (str):
        tag (str | Unset):
        parent (GetProjectsProjectIdCardsParentType0 | Unset | UUID):
        include_deleted (bool | Unset):  Default: False.
        order (GetProjectsProjectIdCardsOrder | Unset):  Default:
            GetProjectsProjectIdCardsOrder.CARD_ID_ASC.
        limit (int | Unset):  Default: 200.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardPageResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        tag=tag,
        parent=parent,
        include_deleted=include_deleted,
        order=order,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    tag: str | Unset = UNSET,
    parent: GetProjectsProjectIdCardsParentType0 | Unset | UUID = UNSET,
    include_deleted: bool | Unset = False,
    order: GetProjectsProjectIdCardsOrder
    | Unset = GetProjectsProjectIdCardsOrder.CARD_ID_ASC,
    limit: int | Unset = 200,
    cursor: str | Unset = UNSET,
) -> CardPageResponse | ErrorResponse | None:
    """Page through a project's cards

     Filters combine. Each page reads current data; iteration is not a snapshot.

    Args:
        project_id (str):
        tag (str | Unset):
        parent (GetProjectsProjectIdCardsParentType0 | Unset | UUID):
        include_deleted (bool | Unset):  Default: False.
        order (GetProjectsProjectIdCardsOrder | Unset):  Default:
            GetProjectsProjectIdCardsOrder.CARD_ID_ASC.
        limit (int | Unset):  Default: 200.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardPageResponse | ErrorResponse
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        tag=tag,
        parent=parent,
        include_deleted=include_deleted,
        order=order,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    tag: str | Unset = UNSET,
    parent: GetProjectsProjectIdCardsParentType0 | Unset | UUID = UNSET,
    include_deleted: bool | Unset = False,
    order: GetProjectsProjectIdCardsOrder
    | Unset = GetProjectsProjectIdCardsOrder.CARD_ID_ASC,
    limit: int | Unset = 200,
    cursor: str | Unset = UNSET,
) -> Response[CardPageResponse | ErrorResponse]:
    """Page through a project's cards

     Filters combine. Each page reads current data; iteration is not a snapshot.

    Args:
        project_id (str):
        tag (str | Unset):
        parent (GetProjectsProjectIdCardsParentType0 | Unset | UUID):
        include_deleted (bool | Unset):  Default: False.
        order (GetProjectsProjectIdCardsOrder | Unset):  Default:
            GetProjectsProjectIdCardsOrder.CARD_ID_ASC.
        limit (int | Unset):  Default: 200.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardPageResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        tag=tag,
        parent=parent,
        include_deleted=include_deleted,
        order=order,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    tag: str | Unset = UNSET,
    parent: GetProjectsProjectIdCardsParentType0 | Unset | UUID = UNSET,
    include_deleted: bool | Unset = False,
    order: GetProjectsProjectIdCardsOrder
    | Unset = GetProjectsProjectIdCardsOrder.CARD_ID_ASC,
    limit: int | Unset = 200,
    cursor: str | Unset = UNSET,
) -> CardPageResponse | ErrorResponse | None:
    """Page through a project's cards

     Filters combine. Each page reads current data; iteration is not a snapshot.

    Args:
        project_id (str):
        tag (str | Unset):
        parent (GetProjectsProjectIdCardsParentType0 | Unset | UUID):
        include_deleted (bool | Unset):  Default: False.
        order (GetProjectsProjectIdCardsOrder | Unset):  Default:
            GetProjectsProjectIdCardsOrder.CARD_ID_ASC.
        limit (int | Unset):  Default: 200.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardPageResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            tag=tag,
            parent=parent,
            include_deleted=include_deleted,
            order=order,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
