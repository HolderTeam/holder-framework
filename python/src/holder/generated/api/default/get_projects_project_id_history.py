from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_projects_project_id_history_kind import (
    GetProjectsProjectIdHistoryKind,
)
from ...models.project_history_page_response import ProjectHistoryPageResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    kind: GetProjectsProjectIdHistoryKind | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_kind: str | Unset = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/history".format(
            project_id=quote(str(project_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ProjectHistoryPageResponse | None:
    if response.status_code == 200:
        response_200 = ProjectHistoryPageResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

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
) -> Response[ErrorResponse | ProjectHistoryPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    kind: GetProjectsProjectIdHistoryKind | Unset = UNSET,
) -> Response[ErrorResponse | ProjectHistoryPageResponse]:
    """List project activity history

     Returns bounded, cursor-paginated Git activities for the project. Each activity groups its changed
    paths by recognised Holder object kind; unknown paths remain visible as unknown.

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        kind (GetProjectsProjectIdHistoryKind | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ProjectHistoryPageResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
        cursor=cursor,
        kind=kind,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    kind: GetProjectsProjectIdHistoryKind | Unset = UNSET,
) -> ErrorResponse | ProjectHistoryPageResponse | None:
    """List project activity history

     Returns bounded, cursor-paginated Git activities for the project. Each activity groups its changed
    paths by recognised Holder object kind; unknown paths remain visible as unknown.

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        kind (GetProjectsProjectIdHistoryKind | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ProjectHistoryPageResponse
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        limit=limit,
        cursor=cursor,
        kind=kind,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    kind: GetProjectsProjectIdHistoryKind | Unset = UNSET,
) -> Response[ErrorResponse | ProjectHistoryPageResponse]:
    """List project activity history

     Returns bounded, cursor-paginated Git activities for the project. Each activity groups its changed
    paths by recognised Holder object kind; unknown paths remain visible as unknown.

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        kind (GetProjectsProjectIdHistoryKind | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ProjectHistoryPageResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
        cursor=cursor,
        kind=kind,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    kind: GetProjectsProjectIdHistoryKind | Unset = UNSET,
) -> ErrorResponse | ProjectHistoryPageResponse | None:
    """List project activity history

     Returns bounded, cursor-paginated Git activities for the project. Each activity groups its changed
    paths by recognised Holder object kind; unknown paths remain visible as unknown.

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        kind (GetProjectsProjectIdHistoryKind | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ProjectHistoryPageResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            limit=limit,
            cursor=cursor,
            kind=kind,
        )
    ).parsed
