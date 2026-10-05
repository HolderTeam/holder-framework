from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.card_history_diff_line import CardHistoryDiffLine
    from ..models.card_history_version import CardHistoryVersion


T = TypeVar("T", bound="CardHistoryComparisonData")


@_attrs_define
class CardHistoryComparisonData:
    """
    Attributes:
        from_ (CardHistoryVersion):
        to (CardHistoryVersion):
        summary (str):
        lines (list[CardHistoryDiffLine]):
        truncated (bool):
    """

    from_: CardHistoryVersion
    to: CardHistoryVersion
    summary: str
    lines: list[CardHistoryDiffLine]
    truncated: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_.to_dict()

        to = self.to.to_dict()

        summary = self.summary

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        truncated = self.truncated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
                "summary": summary,
                "lines": lines,
                "truncated": truncated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_history_diff_line import CardHistoryDiffLine
        from ..models.card_history_version import CardHistoryVersion

        d = dict(src_dict)
        from_ = CardHistoryVersion.from_dict(d.pop("from"))

        to = CardHistoryVersion.from_dict(d.pop("to"))

        summary = d.pop("summary")

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = CardHistoryDiffLine.from_dict(lines_item_data)

            lines.append(lines_item)

        truncated = d.pop("truncated")

        card_history_comparison_data = cls(
            from_=from_,
            to=to,
            summary=summary,
            lines=lines,
            truncated=truncated,
        )

        card_history_comparison_data.additional_properties = d
        return card_history_comparison_data

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
