from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.event_checkpoint_git_revisions import EventCheckpointGitRevisions
    from ..models.event_checkpoint_history_urls import EventCheckpointHistoryUrls


T = TypeVar("T", bound="EventCheckpoint")


@_attrs_define
class EventCheckpoint:
    """
    Attributes:
        cursor (str): Opaque process-local SSE cursor. Persist it unchanged for Last-Event-ID.
        git_revisions (EventCheckpointGitRevisions): Observed project Git HEADs; null for missing or unborn
            repositories. Not a transaction marker for live database state.
        history_urls (EventCheckpointHistoryUrls): Existing project history endpoints for durable recovery. Refresh live
            state after inspecting history.
    """

    cursor: str
    git_revisions: EventCheckpointGitRevisions
    history_urls: EventCheckpointHistoryUrls
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cursor = self.cursor

        git_revisions = self.git_revisions.to_dict()

        history_urls = self.history_urls.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cursor": cursor,
                "git_revisions": git_revisions,
                "history_urls": history_urls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.event_checkpoint_git_revisions import (
            EventCheckpointGitRevisions,
        )
        from ..models.event_checkpoint_history_urls import (
            EventCheckpointHistoryUrls,
        )

        d = dict(src_dict)
        cursor = d.pop("cursor")

        git_revisions = EventCheckpointGitRevisions.from_dict(d.pop("git_revisions"))

        history_urls = EventCheckpointHistoryUrls.from_dict(d.pop("history_urls"))

        event_checkpoint = cls(
            cursor=cursor,
            git_revisions=git_revisions,
            history_urls=history_urls,
        )

        event_checkpoint.additional_properties = d
        return event_checkpoint

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
