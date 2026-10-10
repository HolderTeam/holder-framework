from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_move_intent import CardMoveIntent
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardMoveRequest")


@_attrs_define
class CardMoveRequest:
    """
    Attributes:
        project_id (str):
        intent (CardMoveIntent):
        target_card_id (None | str | Unset): Required for intents into/before/after.
        parent_card_id (None | str | Unset): Destination parent scope for intents to_start/to_end/left/right. If
            omitted, source card's current parent scope is used. An explicit null is the project's top level.
        if_revision (int | None | Unset): Optional optimistic-concurrency revision guard.
    """

    project_id: str
    intent: CardMoveIntent
    target_card_id: None | str | Unset = UNSET
    parent_card_id: None | str | Unset = UNSET
    if_revision: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        intent = self.intent.value

        target_card_id: None | str | Unset
        if isinstance(self.target_card_id, Unset):
            target_card_id = UNSET
        else:
            target_card_id = self.target_card_id

        parent_card_id: None | str | Unset
        if isinstance(self.parent_card_id, Unset):
            parent_card_id = UNSET
        else:
            parent_card_id = self.parent_card_id

        if_revision: int | None | Unset
        if isinstance(self.if_revision, Unset):
            if_revision = UNSET
        else:
            if_revision = self.if_revision

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "intent": intent,
            }
        )
        if target_card_id is not UNSET:
            field_dict["target_card_id"] = target_card_id
        if parent_card_id is not UNSET:
            field_dict["parent_card_id"] = parent_card_id
        if if_revision is not UNSET:
            field_dict["if_revision"] = if_revision

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        intent = CardMoveIntent(d.pop("intent"))

        def _parse_target_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_card_id = _parse_target_card_id(d.pop("target_card_id", UNSET))

        def _parse_parent_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_card_id = _parse_parent_card_id(d.pop("parent_card_id", UNSET))

        def _parse_if_revision(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        if_revision = _parse_if_revision(d.pop("if_revision", UNSET))

        card_move_request = cls(
            project_id=project_id,
            intent=intent,
            target_card_id=target_card_id,
            parent_card_id=parent_card_id,
            if_revision=if_revision,
        )

        card_move_request.additional_properties = d
        return card_move_request

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
