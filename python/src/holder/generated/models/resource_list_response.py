from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource import Resource


T = TypeVar("T", bound="ResourceListResponse")


@_attrs_define
class ResourceListResponse:
    """
    Attributes:
        ok (bool):
        data (list[Resource]):
        card_id (str | Unset): Canonical live card ID, present only for card attachment lists.
        limit (int | Unset):
        offset (int | Unset):
        next_offset (int | None | Unset): Present for card lists; null when exhausted, otherwise continue here (the next
            page may be empty).
    """

    ok: bool
    data: list[Resource]
    card_id: str | Unset = UNSET
    limit: int | Unset = UNSET
    offset: int | Unset = UNSET
    next_offset: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        card_id = self.card_id

        limit = self.limit

        offset = self.offset

        next_offset: int | None | Unset
        if isinstance(self.next_offset, Unset):
            next_offset = UNSET
        else:
            next_offset = self.next_offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
                "data": data,
            }
        )
        if card_id is not UNSET:
            field_dict["card_id"] = card_id
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if next_offset is not UNSET:
            field_dict["next_offset"] = next_offset

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.resource import Resource

        d = dict(src_dict)
        ok = d.pop("ok")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Resource.from_dict(data_item_data)

            data.append(data_item)

        card_id = d.pop("card_id", UNSET)

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        def _parse_next_offset(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        next_offset = _parse_next_offset(d.pop("next_offset", UNSET))

        resource_list_response = cls(
            ok=ok,
            data=data,
            card_id=card_id,
            limit=limit,
            offset=offset,
            next_offset=next_offset,
        )

        resource_list_response.additional_properties = d
        return resource_list_response

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
