from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardMoveResult")


@_attrs_define
class CardMoveResult:
    """
    Attributes:
        card_id (str):
        parent_card_id (None | str):
        sort_key (float):
        revision (int):
        moved_into_title (None | str | Unset):
    """

    card_id: str
    parent_card_id: None | str
    sort_key: float
    revision: int
    moved_into_title: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        parent_card_id: None | str
        parent_card_id = self.parent_card_id

        sort_key = self.sort_key

        revision = self.revision

        moved_into_title: None | str | Unset
        if isinstance(self.moved_into_title, Unset):
            moved_into_title = UNSET
        else:
            moved_into_title = self.moved_into_title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "parent_card_id": parent_card_id,
                "sort_key": sort_key,
                "revision": revision,
            }
        )
        if moved_into_title is not UNSET:
            field_dict["moved_into_title"] = moved_into_title

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        card_id = d.pop("card_id")

        def _parse_parent_card_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        parent_card_id = _parse_parent_card_id(d.pop("parent_card_id"))

        sort_key = d.pop("sort_key")

        revision = d.pop("revision")

        def _parse_moved_into_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        moved_into_title = _parse_moved_into_title(d.pop("moved_into_title", UNSET))

        card_move_result = cls(
            card_id=card_id,
            parent_card_id=parent_card_id,
            sort_key=sort_key,
            revision=revision,
            moved_into_title=moved_into_title,
        )

        card_move_result.additional_properties = d
        return card_move_result

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
