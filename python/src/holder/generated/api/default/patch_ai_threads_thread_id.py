from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ai_thread_patch_response import AiThreadPatchResponse
from ...models.ai_thread_update_request import AiThreadUpdateRequest
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    thread_id: str,
    *,
    body: AiThreadUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/ai/threads/{thread_id}".format(
            thread_id=quote(str(thread_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AiThreadPatchResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = AiThreadPatchResponse.from_dict(response.json())

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
) -> Response[AiThreadPatchResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AiThreadUpdateRequest,
) -> Response[AiThreadPatchResponse | ErrorResponse]:
    """Update AI thread metadata

    Args:
        thread_id (str):
        body (AiThreadUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AiThreadPatchResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AiThreadUpdateRequest,
) -> AiThreadPatchResponse | ErrorResponse | None:
    """Update AI thread metadata

    Args:
        thread_id (str):
        body (AiThreadUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AiThreadPatchResponse | ErrorResponse
    """

    return sync_detailed(
        thread_id=thread_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AiThreadUpdateRequest,
) -> Response[AiThreadPatchResponse | ErrorResponse]:
    """Update AI thread metadata

    Args:
        thread_id (str):
        body (AiThreadUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AiThreadPatchResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: AiThreadUpdateRequest,
) -> AiThreadPatchResponse | ErrorResponse | None:
    """Update AI thread metadata

    Args:
        thread_id (str):
        body (AiThreadUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AiThreadPatchResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            thread_id=thread_id,
            client=client,
            body=body,
        )
    ).parsed
