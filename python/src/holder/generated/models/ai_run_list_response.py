from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.ai_run_item import AiRunItem


T = TypeVar("T", bound="AiRunListResponse")


@_attrs_define
class AiRunListResponse:
    """
    Attributes:
        ok (bool):
        data (list[AiRunItem]):
    """

    ok: bool
    data: list[AiRunItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_run_item import AiRunItem

        d = dict(src_dict)
        ok = d.pop("ok")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AiRunItem.from_dict(data_item_data)

            data.append(data_item)

        ai_run_list_response = cls(
            ok=ok,
            data=data,
        )

        ai_run_list_response.additional_properties = d
        return ai_run_list_response

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
