from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.project_git_test_remote_request import ProjectGitTestRemoteRequest
from ...models.project_git_test_remote_response import ProjectGitTestRemoteResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    body: ProjectGitTestRemoteRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/git/test-remote".format(
            project_id=quote(str(project_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ProjectGitTestRemoteResponse | None:
    if response.status_code == 200:
        response_200 = ProjectGitTestRemoteResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | ProjectGitTestRemoteResponse]:
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
    body: ProjectGitTestRemoteRequest | Unset = UNSET,
) -> Response[ErrorResponse | ProjectGitTestRemoteResponse]:
    """Test project remote reachability/auth

     Connects and lists remote refs using daemon credentials. Does not fetch, create a project
    repository, or change stored project configuration or Git configuration.

    Args:
        project_id (str):
        body (ProjectGitTestRemoteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ProjectGitTestRemoteResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProjectGitTestRemoteRequest | Unset = UNSET,
) -> ErrorResponse | ProjectGitTestRemoteResponse | None:
    """Test project remote reachability/auth

     Connects and lists remote refs using daemon credentials. Does not fetch, create a project
    repository, or change stored project configuration or Git configuration.

    Args:
        project_id (str):
        body (ProjectGitTestRemoteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ProjectGitTestRemoteResponse
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProjectGitTestRemoteRequest | Unset = UNSET,
) -> Response[ErrorResponse | ProjectGitTestRemoteResponse]:
    """Test project remote reachability/auth

     Connects and lists remote refs using daemon credentials. Does not fetch, create a project
    repository, or change stored project configuration or Git configuration.

    Args:
        project_id (str):
        body (ProjectGitTestRemoteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ProjectGitTestRemoteResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProjectGitTestRemoteRequest | Unset = UNSET,
) -> ErrorResponse | ProjectGitTestRemoteResponse | None:
    """Test project remote reachability/auth

     Connects and lists remote refs using daemon credentials. Does not fetch, create a project
    repository, or change stored project configuration or Git configuration.

    Args:
        project_id (str):
        body (ProjectGitTestRemoteRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ProjectGitTestRemoteResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
