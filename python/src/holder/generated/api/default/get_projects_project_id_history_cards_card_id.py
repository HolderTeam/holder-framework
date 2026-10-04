from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_history_page_response import CardHistoryPageResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    card_id: str,
    *,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/history/cards/{card_id}".format(
            project_id=quote(str(project_id), safe=""),
            card_id=quote(str(card_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardHistoryPageResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardHistoryPageResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = ErrorResponse.from_dict(response.json())

        return response_413

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CardHistoryPageResponse | ErrorResponse]:
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
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
) -> Response[CardHistoryPageResponse | ErrorResponse]:
    """List saved history for a card

     Returns commits reachable from the captured project HEAD that changed the card. Adjacent autosaves
    may be grouped into one entry.

    Args:
        project_id (str):
        card_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardHistoryPageResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        card_id=card_id,
        limit=limit,
        cursor=cursor,
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
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
) -> CardHistoryPageResponse | ErrorResponse | None:
    """List saved history for a card

     Returns commits reachable from the captured project HEAD that changed the card. Adjacent autosaves
    may be grouped into one entry.

    Args:
        project_id (str):
        card_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardHistoryPageResponse | ErrorResponse
    """

    return sync_detailed(
        project_id=project_id,
        card_id=card_id,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
) -> Response[CardHistoryPageResponse | ErrorResponse]:
    """List saved history for a card

     Returns commits reachable from the captured project HEAD that changed the card. Adjacent autosaves
    may be grouped into one entry.

    Args:
        project_id (str):
        card_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardHistoryPageResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        card_id=card_id,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
) -> CardHistoryPageResponse | ErrorResponse | None:
    """List saved history for a card

     Returns commits reachable from the captured project HEAD that changed the card. Adjacent autosaves
    may be grouped into one entry.

    Args:
        project_id (str):
        card_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardHistoryPageResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            card_id=card_id,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
