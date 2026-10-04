from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_link_list_response import CardLinkListResponse
from ...models.error_response import ErrorResponse
from ...models.get_cards_card_id_backlinks_include_deleted import (
    GetCardsCardIdBacklinksIncludeDeleted,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    card_id: str,
    *,
    include_deleted: GetCardsCardIdBacklinksIncludeDeleted | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_include_deleted: int | Unset = UNSET
    if not isinstance(include_deleted, Unset):
        json_include_deleted = include_deleted.value

    params["include_deleted"] = json_include_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cards/{card_id}/backlinks".format(
            card_id=quote(str(card_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardLinkListResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardLinkListResponse.from_dict(response.json())

        return response_200

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
) -> Response[CardLinkListResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    include_deleted: GetCardsCardIdBacklinksIncludeDeleted | Unset = UNSET,
) -> Response[CardLinkListResponse | ErrorResponse]:
    """List backlinks to a card

    Args:
        card_id (str):
        include_deleted (GetCardsCardIdBacklinksIncludeDeleted | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardLinkListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        include_deleted=include_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    include_deleted: GetCardsCardIdBacklinksIncludeDeleted | Unset = UNSET,
) -> CardLinkListResponse | ErrorResponse | None:
    """List backlinks to a card

    Args:
        card_id (str):
        include_deleted (GetCardsCardIdBacklinksIncludeDeleted | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardLinkListResponse | ErrorResponse
    """

    return sync_detailed(
        card_id=card_id,
        client=client,
        include_deleted=include_deleted,
    ).parsed


async def asyncio_detailed(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    include_deleted: GetCardsCardIdBacklinksIncludeDeleted | Unset = UNSET,
) -> Response[CardLinkListResponse | ErrorResponse]:
    """List backlinks to a card

    Args:
        card_id (str):
        include_deleted (GetCardsCardIdBacklinksIncludeDeleted | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardLinkListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        include_deleted=include_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    include_deleted: GetCardsCardIdBacklinksIncludeDeleted | Unset = UNSET,
) -> CardLinkListResponse | ErrorResponse | None:
    """List backlinks to a card

    Args:
        card_id (str):
        include_deleted (GetCardsCardIdBacklinksIncludeDeleted | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardLinkListResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            card_id=card_id,
            client=client,
            include_deleted=include_deleted,
        )
    ).parsed
