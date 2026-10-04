from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_history_restore_response import CardHistoryRestoreResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    project_id: str,
    card_id: str,
    *,
    oid: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["oid"] = oid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/history/cards/{card_id}/restore".format(
            project_id=quote(str(project_id), safe=""),
            card_id=quote(str(card_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardHistoryRestoreResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardHistoryRestoreResponse.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CardHistoryRestoreResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    oid: str,
) -> Response[CardHistoryRestoreResponse | ErrorResponse]:
    """Restore a card to a saved snapshot

     Restores the complete card snapshot at the selected commit and records the result as a new commit
    without rewriting history.

    Args:
        project_id (str):
        card_id (str):
        oid (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardHistoryRestoreResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        card_id=card_id,
        oid=oid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    oid: str,
) -> CardHistoryRestoreResponse | ErrorResponse | None:
    """Restore a card to a saved snapshot

     Restores the complete card snapshot at the selected commit and records the result as a new commit
    without rewriting history.

    Args:
        project_id (str):
        card_id (str):
        oid (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardHistoryRestoreResponse | ErrorResponse
    """

    return sync_detailed(
        project_id=project_id,
        card_id=card_id,
        client=client,
        oid=oid,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    oid: str,
) -> Response[CardHistoryRestoreResponse | ErrorResponse]:
    """Restore a card to a saved snapshot

     Restores the complete card snapshot at the selected commit and records the result as a new commit
    without rewriting history.

    Args:
        project_id (str):
        card_id (str):
        oid (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardHistoryRestoreResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        card_id=card_id,
        oid=oid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    oid: str,
) -> CardHistoryRestoreResponse | ErrorResponse | None:
    """Restore a card to a saved snapshot

     Restores the complete card snapshot at the selected commit and records the result as a new commit
    without rewriting history.

    Args:
        project_id (str):
        card_id (str):
        oid (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardHistoryRestoreResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            card_id=card_id,
            client=client,
            oid=oid,
        )
    ).parsed
