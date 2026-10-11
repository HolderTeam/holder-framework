from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_move_request import CardMoveRequest
from ...models.card_move_response import CardMoveResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    card_id: str,
    *,
    body: CardMoveRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cards/{card_id}/move".format(
            card_id=quote(str(card_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardMoveResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardMoveResponse.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CardMoveResponse | ErrorResponse]:
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
    body: CardMoveRequest,
) -> Response[CardMoveResponse | ErrorResponse]:
    """Move/reparent/reorder a card using card move intent

     Placement is resolved and written under the project lock. When the card's new neighbours leave no
    room between their sort keys (tied keys, or a gap used up by repeated moves), nearby siblings are
    re-spaced in the same commit, keeping their order. The response describes only the moved card, so a
    client holding other cards' sort_key values should refresh the listing.

    Args:
        card_id (str):
        body (CardMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardMoveResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardMoveRequest,
) -> CardMoveResponse | ErrorResponse | None:
    """Move/reparent/reorder a card using card move intent

     Placement is resolved and written under the project lock. When the card's new neighbours leave no
    room between their sort keys (tied keys, or a gap used up by repeated moves), nearby siblings are
    re-spaced in the same commit, keeping their order. The response describes only the moved card, so a
    client holding other cards' sort_key values should refresh the listing.

    Args:
        card_id (str):
        body (CardMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardMoveResponse | ErrorResponse
    """

    return sync_detailed(
        card_id=card_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardMoveRequest,
) -> Response[CardMoveResponse | ErrorResponse]:
    """Move/reparent/reorder a card using card move intent

     Placement is resolved and written under the project lock. When the card's new neighbours leave no
    room between their sort keys (tied keys, or a gap used up by repeated moves), nearby siblings are
    re-spaced in the same commit, keeping their order. The response describes only the moved card, so a
    client holding other cards' sort_key values should refresh the listing.

    Args:
        card_id (str):
        body (CardMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardMoveResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardMoveRequest,
) -> CardMoveResponse | ErrorResponse | None:
    """Move/reparent/reorder a card using card move intent

     Placement is resolved and written under the project lock. When the card's new neighbours leave no
    room between their sort keys (tied keys, or a gap used up by repeated moves), nearby siblings are
    re-spaced in the same commit, keeping their order. The response describes only the moved card, so a
    client holding other cards' sort_key values should refresh the listing.

    Args:
        card_id (str):
        body (CardMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardMoveResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            card_id=card_id,
            client=client,
            body=body,
        )
    ).parsed
