from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.milestone_response import MilestoneResponse
from ...models.milestone_update_request import MilestoneUpdateRequest
from ...types import Response


def _get_kwargs(
    card_id: str,
    milestone_id: UUID,
    *,
    body: MilestoneUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/cards/{card_id}/milestones/{milestone_id}".format(
            card_id=quote(str(card_id), safe=""),
            milestone_id=quote(str(milestone_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MilestoneResponse | None:
    if response.status_code == 200:
        response_200 = MilestoneResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | MilestoneResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    card_id: str,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MilestoneUpdateRequest,
) -> Response[ErrorResponse | MilestoneResponse]:
    """Partially update a milestone on a live card

     Updates only supplied fields while preserving milestone identity and creation metadata.

    Args:
        card_id (str):
        milestone_id (UUID):
        body (MilestoneUpdateRequest): Partial milestone update. Omitted properties remain
            unchanged; null clears a nullable property.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MilestoneResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        milestone_id=milestone_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    card_id: str,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MilestoneUpdateRequest,
) -> ErrorResponse | MilestoneResponse | None:
    """Partially update a milestone on a live card

     Updates only supplied fields while preserving milestone identity and creation metadata.

    Args:
        card_id (str):
        milestone_id (UUID):
        body (MilestoneUpdateRequest): Partial milestone update. Omitted properties remain
            unchanged; null clears a nullable property.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MilestoneResponse
    """

    return sync_detailed(
        card_id=card_id,
        milestone_id=milestone_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    card_id: str,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MilestoneUpdateRequest,
) -> Response[ErrorResponse | MilestoneResponse]:
    """Partially update a milestone on a live card

     Updates only supplied fields while preserving milestone identity and creation metadata.

    Args:
        card_id (str):
        milestone_id (UUID):
        body (MilestoneUpdateRequest): Partial milestone update. Omitted properties remain
            unchanged; null clears a nullable property.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MilestoneResponse]
    """

    kwargs = _get_kwargs(
        card_id=card_id,
        milestone_id=milestone_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    card_id: str,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MilestoneUpdateRequest,
) -> ErrorResponse | MilestoneResponse | None:
    """Partially update a milestone on a live card

     Updates only supplied fields while preserving milestone identity and creation metadata.

    Args:
        card_id (str):
        milestone_id (UUID):
        body (MilestoneUpdateRequest): Partial milestone update. Omitted properties remain
            unchanged; null clears a nullable property.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MilestoneResponse
    """

    return (
        await asyncio_detailed(
            card_id=card_id,
            milestone_id=milestone_id,
            client=client,
            body=body,
        )
    ).parsed
