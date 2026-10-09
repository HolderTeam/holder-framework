from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_list_response import CardListResponse
from ...models.error_response import ErrorResponse
from ...models.get_cards_order import GetCardsOrder
from ...models.get_cards_view import GetCardsView
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: str,
    tag: str | Unset = UNSET,
    view: GetCardsView | Unset = GetCardsView.TREE,
    after_card_id: str | Unset = UNSET,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsOrder | Unset = UNSET,
    count: bool | Unset = False,
    limit: int | Unset = 200,
    include_deleted: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["project_id"] = project_id

    params["tag"] = tag

    json_view: str | Unset = UNSET
    if not isinstance(view, Unset):
        json_view = view.value

    params["view"] = json_view

    params["after_card_id"] = after_card_id

    params["parent_card_id"] = parent_card_id

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["count"] = count

    params["limit"] = limit

    params["include_deleted"] = include_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cards",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardListResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardListResponse.from_dict(response.json())

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
) -> Response[CardListResponse | ErrorResponse]:
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
    tag: str | Unset = UNSET,
    view: GetCardsView | Unset = GetCardsView.TREE,
    after_card_id: str | Unset = UNSET,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsOrder | Unset = UNSET,
    count: bool | Unset = False,
    limit: int | Unset = 200,
    include_deleted: int | Unset = UNSET,
) -> Response[CardListResponse | ErrorResponse]:
    """List cards

    Args:
        project_id (str):
        tag (str | Unset):
        view (GetCardsView | Unset):  Default: GetCardsView.TREE.
        after_card_id (str | Unset):
        parent_card_id (str | Unset):
        order (GetCardsOrder | Unset):
        count (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 200.
        include_deleted (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        tag=tag,
        view=view,
        after_card_id=after_card_id,
        parent_card_id=parent_card_id,
        order=order,
        count=count,
        limit=limit,
        include_deleted=include_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    tag: str | Unset = UNSET,
    view: GetCardsView | Unset = GetCardsView.TREE,
    after_card_id: str | Unset = UNSET,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsOrder | Unset = UNSET,
    count: bool | Unset = False,
    limit: int | Unset = 200,
    include_deleted: int | Unset = UNSET,
) -> CardListResponse | ErrorResponse | None:
    """List cards

    Args:
        project_id (str):
        tag (str | Unset):
        view (GetCardsView | Unset):  Default: GetCardsView.TREE.
        after_card_id (str | Unset):
        parent_card_id (str | Unset):
        order (GetCardsOrder | Unset):
        count (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 200.
        include_deleted (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardListResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        tag=tag,
        view=view,
        after_card_id=after_card_id,
        parent_card_id=parent_card_id,
        order=order,
        count=count,
        limit=limit,
        include_deleted=include_deleted,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    tag: str | Unset = UNSET,
    view: GetCardsView | Unset = GetCardsView.TREE,
    after_card_id: str | Unset = UNSET,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsOrder | Unset = UNSET,
    count: bool | Unset = False,
    limit: int | Unset = 200,
    include_deleted: int | Unset = UNSET,
) -> Response[CardListResponse | ErrorResponse]:
    """List cards

    Args:
        project_id (str):
        tag (str | Unset):
        view (GetCardsView | Unset):  Default: GetCardsView.TREE.
        after_card_id (str | Unset):
        parent_card_id (str | Unset):
        order (GetCardsOrder | Unset):
        count (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 200.
        include_deleted (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        tag=tag,
        view=view,
        after_card_id=after_card_id,
        parent_card_id=parent_card_id,
        order=order,
        count=count,
        limit=limit,
        include_deleted=include_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    tag: str | Unset = UNSET,
    view: GetCardsView | Unset = GetCardsView.TREE,
    after_card_id: str | Unset = UNSET,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsOrder | Unset = UNSET,
    count: bool | Unset = False,
    limit: int | Unset = 200,
    include_deleted: int | Unset = UNSET,
) -> CardListResponse | ErrorResponse | None:
    """List cards

    Args:
        project_id (str):
        tag (str | Unset):
        view (GetCardsView | Unset):  Default: GetCardsView.TREE.
        after_card_id (str | Unset):
        parent_card_id (str | Unset):
        order (GetCardsOrder | Unset):
        count (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 200.
        include_deleted (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardListResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            tag=tag,
            view=view,
            after_card_id=after_card_id,
            parent_card_id=parent_card_id,
            order=order,
            count=count,
            limit=limit,
            include_deleted=include_deleted,
        )
    ).parsed
