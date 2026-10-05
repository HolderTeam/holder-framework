from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.card_history_entry import CardHistoryEntry


T = TypeVar("T", bound="CardHistoryPageData")


@_attrs_define
class CardHistoryPageData:
    """
    Attributes:
        head_oid (None | str):
        entries (list[CardHistoryEntry]):
        next_cursor (None | str):
        scan_limited (bool): True when History examined its bounded number of revisions before reaching the end;
            next_cursor continues the scan.
    """

    head_oid: None | str
    entries: list[CardHistoryEntry]
    next_cursor: None | str
    scan_limited: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        head_oid: None | str
        head_oid = self.head_oid

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        scan_limited = self.scan_limited

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "head_oid": head_oid,
                "entries": entries,
                "next_cursor": next_cursor,
                "scan_limited": scan_limited,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_history_entry import CardHistoryEntry

        d = dict(src_dict)

        def _parse_head_oid(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        head_oid = _parse_head_oid(d.pop("head_oid"))

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = CardHistoryEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        scan_limited = d.pop("scan_limited")

        card_history_page_data = cls(
            head_oid=head_oid,
            entries=entries,
            next_cursor=next_cursor,
            scan_limited=scan_limited,
        )

        card_history_page_data.additional_properties = d
        return card_history_page_data

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
