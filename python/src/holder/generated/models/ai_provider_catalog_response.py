from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.ai_provider_catalog_response_data import AiProviderCatalogResponseData


T = TypeVar("T", bound="AiProviderCatalogResponse")


@_attrs_define
class AiProviderCatalogResponse:
    """
    Attributes:
        ok (bool):
        data (AiProviderCatalogResponseData):
    """

    ok: bool
    data: AiProviderCatalogResponseData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        data = self.data.to_dict()

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
        from ..models.ai_provider_catalog_response_data import (
            AiProviderCatalogResponseData,
        )

        d = dict(src_dict)
        ok = d.pop("ok")

        data = AiProviderCatalogResponseData.from_dict(d.pop("data"))

        ai_provider_catalog_response = cls(
            ok=ok,
            data=data,
        )

        ai_provider_catalog_response.additional_properties = d
        return ai_provider_catalog_response

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
