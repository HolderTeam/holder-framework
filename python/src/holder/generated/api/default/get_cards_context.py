from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_context_response import CardContextResponse
from ...models.error_response import ErrorResponse
from ...models.get_cards_context_order import GetCardsContextOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: str,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsContextOrder | Unset = GetCardsContextOrder.TREE_DEFAULT,
    count: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["project_id"] = project_id

    params["parent_card_id"] = parent_card_id

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cards/context",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardContextResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardContextResponse.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CardContextResponse | ErrorResponse]:
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
    parent_card_id: str | Unset = UNSET,
    order: GetCardsContextOrder | Unset = GetCardsContextOrder.TREE_DEFAULT,
    count: bool | Unset = False,
) -> Response[CardContextResponse | ErrorResponse]:
    """Read card context and breadcrumb path for a project level

    Args:
        project_id (str):
        parent_card_id (str | Unset):
        order (GetCardsContextOrder | Unset):  Default: GetCardsContextOrder.TREE_DEFAULT.
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardContextResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        parent_card_id=parent_card_id,
        order=order,
        count=count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsContextOrder | Unset = GetCardsContextOrder.TREE_DEFAULT,
    count: bool | Unset = False,
) -> CardContextResponse | ErrorResponse | None:
    """Read card context and breadcrumb path for a project level

    Args:
        project_id (str):
        parent_card_id (str | Unset):
        order (GetCardsContextOrder | Unset):  Default: GetCardsContextOrder.TREE_DEFAULT.
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardContextResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        parent_card_id=parent_card_id,
        order=order,
        count=count,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsContextOrder | Unset = GetCardsContextOrder.TREE_DEFAULT,
    count: bool | Unset = False,
) -> Response[CardContextResponse | ErrorResponse]:
    """Read card context and breadcrumb path for a project level

    Args:
        project_id (str):
        parent_card_id (str | Unset):
        order (GetCardsContextOrder | Unset):  Default: GetCardsContextOrder.TREE_DEFAULT.
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardContextResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        parent_card_id=parent_card_id,
        order=order,
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    project_id: str,
    parent_card_id: str | Unset = UNSET,
    order: GetCardsContextOrder | Unset = GetCardsContextOrder.TREE_DEFAULT,
    count: bool | Unset = False,
) -> CardContextResponse | ErrorResponse | None:
    """Read card context and breadcrumb path for a project level

    Args:
        project_id (str):
        parent_card_id (str | Unset):
        order (GetCardsContextOrder | Unset):  Default: GetCardsContextOrder.TREE_DEFAULT.
        count (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardContextResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            parent_card_id=parent_card_id,
            order=order,
            count=count,
        )
    ).parsed
