from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_history_diff_line_origin import CardHistoryDiffLineOrigin

T = TypeVar("T", bound="CardHistoryDiffLine")


@_attrs_define
class CardHistoryDiffLine:
    """
    Attributes:
        origin (CardHistoryDiffLineOrigin):
        text (str):
        old_line (int | None):
        new_line (int | None):
    """

    origin: CardHistoryDiffLineOrigin
    text: str
    old_line: int | None
    new_line: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        origin = self.origin.value

        text = self.text

        old_line: int | None
        old_line = self.old_line

        new_line: int | None
        new_line = self.new_line

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "origin": origin,
                "text": text,
                "old_line": old_line,
                "new_line": new_line,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        origin = CardHistoryDiffLineOrigin(d.pop("origin"))

        text = d.pop("text")

        def _parse_old_line(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        old_line = _parse_old_line(d.pop("old_line"))

        def _parse_new_line(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        new_line = _parse_new_line(d.pop("new_line"))

        card_history_diff_line = cls(
            origin=origin,
            text=text,
            old_line=old_line,
            new_line=new_line,
        )

        card_history_diff_line.additional_properties = d
        return card_history_diff_line

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
