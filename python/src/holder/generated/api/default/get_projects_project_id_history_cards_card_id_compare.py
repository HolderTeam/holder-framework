from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_history_comparison_response import CardHistoryComparisonResponse
from ...models.error_response import ErrorResponse
from ...models.get_projects_project_id_history_cards_card_id_compare_mode import (
    GetProjectsProjectIdHistoryCardsCardIdCompareMode,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    card_id: str,
    *,
    from_: str | Unset = UNSET,
    to: str,
    mode: GetProjectsProjectIdHistoryCardsCardIdCompareMode
    | Unset = GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["from"] = from_

    params["to"] = to

    json_mode: str | Unset = UNSET
    if not isinstance(mode, Unset):
        json_mode = mode.value

    params["mode"] = json_mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/history/cards/{card_id}/compare".format(
            project_id=quote(str(project_id), safe=""),
            card_id=quote(str(card_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardHistoryComparisonResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardHistoryComparisonResponse.from_dict(response.json())

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
) -> Response[CardHistoryComparisonResponse | ErrorResponse]:
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
    from_: str | Unset = UNSET,
    to: str,
    mode: GetProjectsProjectIdHistoryCardsCardIdCompareMode
    | Unset = GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE,
) -> Response[CardHistoryComparisonResponse | ErrorResponse]:
    """Compare saved card versions or the change introduced by one revision

     In since mode, compares the explicitly selected from and to snapshots. In change mode, compares the
    first parent of to with to; a root commit is compared with a previously nonexistent card. Merge
    commits use only their first parent, not a combined multi-parent diff.

    Args:
        project_id (str):
        card_id (str):
        from_ (str | Unset): Full Git commit object ID or a unique leading commit-ID prefix.
            Successful responses use the canonical full lowercase object ID.
        to (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.
        mode (GetProjectsProjectIdHistoryCardsCardIdCompareMode | Unset):  Default:
            GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardHistoryComparisonResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        card_id=card_id,
        from_=from_,
        to=to,
        mode=mode,
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
    from_: str | Unset = UNSET,
    to: str,
    mode: GetProjectsProjectIdHistoryCardsCardIdCompareMode
    | Unset = GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE,
) -> CardHistoryComparisonResponse | ErrorResponse | None:
    """Compare saved card versions or the change introduced by one revision

     In since mode, compares the explicitly selected from and to snapshots. In change mode, compares the
    first parent of to with to; a root commit is compared with a previously nonexistent card. Merge
    commits use only their first parent, not a combined multi-parent diff.

    Args:
        project_id (str):
        card_id (str):
        from_ (str | Unset): Full Git commit object ID or a unique leading commit-ID prefix.
            Successful responses use the canonical full lowercase object ID.
        to (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.
        mode (GetProjectsProjectIdHistoryCardsCardIdCompareMode | Unset):  Default:
            GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardHistoryComparisonResponse | ErrorResponse
    """

    return sync_detailed(
        project_id=project_id,
        card_id=card_id,
        client=client,
        from_=from_,
        to=to,
        mode=mode,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    from_: str | Unset = UNSET,
    to: str,
    mode: GetProjectsProjectIdHistoryCardsCardIdCompareMode
    | Unset = GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE,
) -> Response[CardHistoryComparisonResponse | ErrorResponse]:
    """Compare saved card versions or the change introduced by one revision

     In since mode, compares the explicitly selected from and to snapshots. In change mode, compares the
    first parent of to with to; a root commit is compared with a previously nonexistent card. Merge
    commits use only their first parent, not a combined multi-parent diff.

    Args:
        project_id (str):
        card_id (str):
        from_ (str | Unset): Full Git commit object ID or a unique leading commit-ID prefix.
            Successful responses use the canonical full lowercase object ID.
        to (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.
        mode (GetProjectsProjectIdHistoryCardsCardIdCompareMode | Unset):  Default:
            GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardHistoryComparisonResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        card_id=card_id,
        from_=from_,
        to=to,
        mode=mode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    card_id: str,
    *,
    client: AuthenticatedClient | Client,
    from_: str | Unset = UNSET,
    to: str,
    mode: GetProjectsProjectIdHistoryCardsCardIdCompareMode
    | Unset = GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE,
) -> CardHistoryComparisonResponse | ErrorResponse | None:
    """Compare saved card versions or the change introduced by one revision

     In since mode, compares the explicitly selected from and to snapshots. In change mode, compares the
    first parent of to with to; a root commit is compared with a previously nonexistent card. Merge
    commits use only their first parent, not a combined multi-parent diff.

    Args:
        project_id (str):
        card_id (str):
        from_ (str | Unset): Full Git commit object ID or a unique leading commit-ID prefix.
            Successful responses use the canonical full lowercase object ID.
        to (str): Full Git commit object ID or a unique leading commit-ID prefix. Successful
            responses use the canonical full lowercase object ID.
        mode (GetProjectsProjectIdHistoryCardsCardIdCompareMode | Unset):  Default:
            GetProjectsProjectIdHistoryCardsCardIdCompareMode.SINCE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardHistoryComparisonResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            card_id=card_id,
            client=client,
            from_=from_,
            to=to,
            mode=mode,
        )
    ).parsed
