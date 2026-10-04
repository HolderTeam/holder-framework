from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_provider_catalog_provider import AiProviderCatalogProvider


T = TypeVar("T", bound="AiProviderCatalogResponseData")


@_attrs_define
class AiProviderCatalogResponseData:
    """
    Attributes:
        providers (list[AiProviderCatalogProvider]):
        default_provider (None | str | Unset):
    """

    providers: list[AiProviderCatalogProvider]
    default_provider: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()
            providers.append(providers_item)

        default_provider: None | str | Unset
        if isinstance(self.default_provider, Unset):
            default_provider = UNSET
        else:
            default_provider = self.default_provider

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "providers": providers,
            }
        )
        if default_provider is not UNSET:
            field_dict["default_provider"] = default_provider

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_provider_catalog_provider import (
            AiProviderCatalogProvider,
        )

        d = dict(src_dict)
        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = AiProviderCatalogProvider.from_dict(providers_item_data)

            providers.append(providers_item)

        def _parse_default_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_provider = _parse_default_provider(d.pop("default_provider", UNSET))

        ai_provider_catalog_response_data = cls(
            providers=providers,
            default_provider=default_provider,
        )

        ai_provider_catalog_response_data.additional_properties = d
        return ai_provider_catalog_response_data

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
