from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.post_cards_card_id_resources_body import PostCardsCardIdResourcesBody
from ...models.resource_attachment_response import ResourceAttachmentResponse
from ...types import Response


def _get_kwargs(
    card_id: str,
    *,
    body: PostCardsCardIdResourcesBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cards/{card_id}/resources".format(
            card_id=quote(str(card_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ResourceAttachmentResponse | None:
    if response.status_code == 200:
        response_200 = ResourceAttachmentResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | ResourceAttachmentResponse]:
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
    body: PostCardsCardIdResourcesBody,
) -> Response[ErrorResponse | ResourceAttachmentResponse]:
    """Attach a project resource to a live card (idempotent)

    Args:
        card_id (str):
        body (PostCardsCardIdResourcesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ResourceAttachmentResponse]
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
    body: PostCardsCardIdResourcesBody,
) -> ErrorResponse | ResourceAttachmentResponse | None:
    """Attach a project resource to a live card (idempotent)

    Args:
        card_id (str):
        body (PostCardsCardIdResourcesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ResourceAttachmentResponse
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
    body: PostCardsCardIdResourcesBody,
) -> Response[ErrorResponse | ResourceAttachmentResponse]:
    """Attach a project resource to a live card (idempotent)

    Args:
        card_id (str):
        body (PostCardsCardIdResourcesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ResourceAttachmentResponse]
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
    body: PostCardsCardIdResourcesBody,
) -> ErrorResponse | ResourceAttachmentResponse | None:
    """Attach a project resource to a live card (idempotent)

    Args:
        card_id (str):
        body (PostCardsCardIdResourcesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ResourceAttachmentResponse
    """

    return (
        await asyncio_detailed(
            card_id=card_id,
            client=client,
            body=body,
        )
    ).parsed
