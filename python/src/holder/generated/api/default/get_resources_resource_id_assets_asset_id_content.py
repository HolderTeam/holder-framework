from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    resource_id: str,
    asset_id: str,
    *,
    placement_id: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["placement_id"] = placement_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/resources/{resource_id}/assets/{asset_id}/content".format(
            resource_id=quote(str(resource_id), safe=""),
            asset_id=quote(str(asset_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | File | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

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

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    if response.status_code == 507:
        response_507 = ErrorResponse.from_dict(response.json())

        return response_507

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_id: str,
    asset_id: str,
    *,
    client: AuthenticatedClient | Client,
    placement_id: str | Unset = UNSET,
) -> Response[ErrorResponse | File]:
    """Stream verified asset content

     Authenticated binary download. Content-Type preserves the asset media type and Content-Disposition
    contains a sanitized quoted original filename. Successful content is arbitrary bytes, not a JSON
    envelope; failures use ErrorResponse. Without placement_id the daemon selects a stored placement.

    Args:
        resource_id (str):
        asset_id (str):
        placement_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | File]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        asset_id=asset_id,
        placement_id=placement_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_id: str,
    asset_id: str,
    *,
    client: AuthenticatedClient | Client,
    placement_id: str | Unset = UNSET,
) -> ErrorResponse | File | None:
    """Stream verified asset content

     Authenticated binary download. Content-Type preserves the asset media type and Content-Disposition
    contains a sanitized quoted original filename. Successful content is arbitrary bytes, not a JSON
    envelope; failures use ErrorResponse. Without placement_id the daemon selects a stored placement.

    Args:
        resource_id (str):
        asset_id (str):
        placement_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | File
    """

    return sync_detailed(
        resource_id=resource_id,
        asset_id=asset_id,
        client=client,
        placement_id=placement_id,
    ).parsed


async def asyncio_detailed(
    resource_id: str,
    asset_id: str,
    *,
    client: AuthenticatedClient | Client,
    placement_id: str | Unset = UNSET,
) -> Response[ErrorResponse | File]:
    """Stream verified asset content

     Authenticated binary download. Content-Type preserves the asset media type and Content-Disposition
    contains a sanitized quoted original filename. Successful content is arbitrary bytes, not a JSON
    envelope; failures use ErrorResponse. Without placement_id the daemon selects a stored placement.

    Args:
        resource_id (str):
        asset_id (str):
        placement_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | File]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        asset_id=asset_id,
        placement_id=placement_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_id: str,
    asset_id: str,
    *,
    client: AuthenticatedClient | Client,
    placement_id: str | Unset = UNSET,
) -> ErrorResponse | File | None:
    """Stream verified asset content

     Authenticated binary download. Content-Type preserves the asset media type and Content-Disposition
    contains a sanitized quoted original filename. Successful content is arbitrary bytes, not a JSON
    envelope; failures use ErrorResponse. Without placement_id the daemon selects a stored placement.

    Args:
        resource_id (str):
        asset_id (str):
        placement_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | File
    """

    return (
        await asyncio_detailed(
            resource_id=resource_id,
            asset_id=asset_id,
            client=client,
            placement_id=placement_id,
        )
    ).parsed
