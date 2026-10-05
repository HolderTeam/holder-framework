from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_provider_catalog_provider_api_type_0 import (
        AiProviderCatalogProviderApiType0,
    )
    from ..models.ai_provider_catalog_provider_auth_type_0 import (
        AiProviderCatalogProviderAuthType0,
    )
    from ..models.ai_provider_catalog_provider_models_item import (
        AiProviderCatalogProviderModelsItem,
    )


T = TypeVar("T", bound="AiProviderCatalogProvider")


@_attrs_define
class AiProviderCatalogProvider:
    """
    Attributes:
        id (str):
        display_name (str):
        enabled (bool):
        configured (bool):
        api (AiProviderCatalogProviderApiType0 | None):
        auth (AiProviderCatalogProviderAuthType0 | None):
        models (list[AiProviderCatalogProviderModelsItem]):
        setup_url (None | str | Unset):
        docs_url (None | str | Unset):
        api_key_label (None | str | Unset):
        api_key_hint (None | str | Unset):
    """

    id: str
    display_name: str
    enabled: bool
    configured: bool
    api: AiProviderCatalogProviderApiType0 | None
    auth: AiProviderCatalogProviderAuthType0 | None
    models: list[AiProviderCatalogProviderModelsItem]
    setup_url: None | str | Unset = UNSET
    docs_url: None | str | Unset = UNSET
    api_key_label: None | str | Unset = UNSET
    api_key_hint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_provider_catalog_provider_api_type_0 import (
            AiProviderCatalogProviderApiType0,
        )
        from ..models.ai_provider_catalog_provider_auth_type_0 import (
            AiProviderCatalogProviderAuthType0,
        )

        id = self.id

        display_name = self.display_name

        enabled = self.enabled

        configured = self.configured

        api: dict[str, Any] | None
        if isinstance(self.api, AiProviderCatalogProviderApiType0):
            api = self.api.to_dict()
        else:
            api = self.api

        auth: dict[str, Any] | None
        if isinstance(self.auth, AiProviderCatalogProviderAuthType0):
            auth = self.auth.to_dict()
        else:
            auth = self.auth

        models = []
        for models_item_data in self.models:
            models_item = models_item_data.to_dict()
            models.append(models_item)

        setup_url: None | str | Unset
        if isinstance(self.setup_url, Unset):
            setup_url = UNSET
        else:
            setup_url = self.setup_url

        docs_url: None | str | Unset
        if isinstance(self.docs_url, Unset):
            docs_url = UNSET
        else:
            docs_url = self.docs_url

        api_key_label: None | str | Unset
        if isinstance(self.api_key_label, Unset):
            api_key_label = UNSET
        else:
            api_key_label = self.api_key_label

        api_key_hint: None | str | Unset
        if isinstance(self.api_key_hint, Unset):
            api_key_hint = UNSET
        else:
            api_key_hint = self.api_key_hint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "display_name": display_name,
                "enabled": enabled,
                "configured": configured,
                "api": api,
                "auth": auth,
                "models": models,
            }
        )
        if setup_url is not UNSET:
            field_dict["setup_url"] = setup_url
        if docs_url is not UNSET:
            field_dict["docs_url"] = docs_url
        if api_key_label is not UNSET:
            field_dict["api_key_label"] = api_key_label
        if api_key_hint is not UNSET:
            field_dict["api_key_hint"] = api_key_hint

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_provider_catalog_provider_api_type_0 import (
            AiProviderCatalogProviderApiType0,
        )
        from ..models.ai_provider_catalog_provider_auth_type_0 import (
            AiProviderCatalogProviderAuthType0,
        )
        from ..models.ai_provider_catalog_provider_models_item import (
            AiProviderCatalogProviderModelsItem,
        )

        d = dict(src_dict)
        id = d.pop("id")

        display_name = d.pop("display_name")

        enabled = d.pop("enabled")

        configured = d.pop("configured")

        def _parse_api(data: object) -> AiProviderCatalogProviderApiType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                api_type_0 = AiProviderCatalogProviderApiType0.from_dict(data)

                return api_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AiProviderCatalogProviderApiType0 | None, data)

        api = _parse_api(d.pop("api"))

        def _parse_auth(data: object) -> AiProviderCatalogProviderAuthType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                auth_type_0 = AiProviderCatalogProviderAuthType0.from_dict(data)

                return auth_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AiProviderCatalogProviderAuthType0 | None, data)

        auth = _parse_auth(d.pop("auth"))

        models = []
        _models = d.pop("models")
        for models_item_data in _models:
            models_item = AiProviderCatalogProviderModelsItem.from_dict(
                models_item_data
            )

            models.append(models_item)

        def _parse_setup_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        setup_url = _parse_setup_url(d.pop("setup_url", UNSET))

        def _parse_docs_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        docs_url = _parse_docs_url(d.pop("docs_url", UNSET))

        def _parse_api_key_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        api_key_label = _parse_api_key_label(d.pop("api_key_label", UNSET))

        def _parse_api_key_hint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        api_key_hint = _parse_api_key_hint(d.pop("api_key_hint", UNSET))

        ai_provider_catalog_provider = cls(
            id=id,
            display_name=display_name,
            enabled=enabled,
            configured=configured,
            api=api,
            auth=auth,
            models=models,
            setup_url=setup_url,
            docs_url=docs_url,
            api_key_label=api_key_label,
            api_key_hint=api_key_hint,
        )

        ai_provider_catalog_provider.additional_properties = d
        return ai_provider_catalog_provider

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
