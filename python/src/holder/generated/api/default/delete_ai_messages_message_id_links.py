from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ai_message_create_response import AiMessageCreateResponse
from ...models.card_link_delete_request import CardLinkDeleteRequest
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    message_id: str,
    *,
    body: CardLinkDeleteRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/ai/messages/{message_id}/links".format(
            message_id=quote(str(message_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AiMessageCreateResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = AiMessageCreateResponse.from_dict(response.json())

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
) -> Response[AiMessageCreateResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardLinkDeleteRequest | Unset = UNSET,
) -> Response[AiMessageCreateResponse | ErrorResponse]:
    """Delete links from an AI message

     Provide to_card_id (and optional to_type/kind) to delete a specific link. If omitted, deletes all
    outgoing links.

    Args:
        message_id (str):
        body (CardLinkDeleteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AiMessageCreateResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardLinkDeleteRequest | Unset = UNSET,
) -> AiMessageCreateResponse | ErrorResponse | None:
    """Delete links from an AI message

     Provide to_card_id (and optional to_type/kind) to delete a specific link. If omitted, deletes all
    outgoing links.

    Args:
        message_id (str):
        body (CardLinkDeleteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AiMessageCreateResponse | ErrorResponse
    """

    return sync_detailed(
        message_id=message_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardLinkDeleteRequest | Unset = UNSET,
) -> Response[AiMessageCreateResponse | ErrorResponse]:
    """Delete links from an AI message

     Provide to_card_id (and optional to_type/kind) to delete a specific link. If omitted, deletes all
    outgoing links.

    Args:
        message_id (str):
        body (CardLinkDeleteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AiMessageCreateResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CardLinkDeleteRequest | Unset = UNSET,
) -> AiMessageCreateResponse | ErrorResponse | None:
    """Delete links from an AI message

     Provide to_card_id (and optional to_type/kind) to delete a specific link. If omitted, deletes all
    outgoing links.

    Args:
        message_id (str):
        body (CardLinkDeleteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AiMessageCreateResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            message_id=message_id,
            client=client,
            body=body,
        )
    ).parsed
