from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_local_model_config_data import AiLocalModelConfigData
    from ..models.caste_info import CasteInfo
    from ..models.caste_recommended_model import CasteRecommendedModel
    from ..models.local_model import LocalModel


T = TypeVar("T", bound="RunnerCapabilitiesData")


@_attrs_define
class RunnerCapabilitiesData:
    """
    Attributes:
        runner_available (bool):
        last_checked (int):
        local_model_config (AiLocalModelConfigData):
        models (list[LocalModel]):
        recommended_models (list[CasteRecommendedModel]):
        recommended_install (list[CasteRecommendedModel]):
        spawn_attempted (bool | Unset):
        version (str | Unset):
        error (None | str | Unset):
        caste (CasteInfo | None | Unset):
    """

    runner_available: bool
    last_checked: int
    local_model_config: AiLocalModelConfigData
    models: list[LocalModel]
    recommended_models: list[CasteRecommendedModel]
    recommended_install: list[CasteRecommendedModel]
    spawn_attempted: bool | Unset = UNSET
    version: str | Unset = UNSET
    error: None | str | Unset = UNSET
    caste: CasteInfo | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.caste_info import CasteInfo

        runner_available = self.runner_available

        last_checked = self.last_checked

        local_model_config = self.local_model_config.to_dict()

        models = []
        for models_item_data in self.models:
            models_item = models_item_data.to_dict()
            models.append(models_item)

        recommended_models = []
        for recommended_models_item_data in self.recommended_models:
            recommended_models_item = recommended_models_item_data.to_dict()
            recommended_models.append(recommended_models_item)

        recommended_install = []
        for recommended_install_item_data in self.recommended_install:
            recommended_install_item = recommended_install_item_data.to_dict()
            recommended_install.append(recommended_install_item)

        spawn_attempted = self.spawn_attempted

        version = self.version

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        caste: dict[str, Any] | None | Unset
        if isinstance(self.caste, Unset):
            caste = UNSET
        elif isinstance(self.caste, CasteInfo):
            caste = self.caste.to_dict()
        else:
            caste = self.caste

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runner_available": runner_available,
                "last_checked": last_checked,
                "local_model_config": local_model_config,
                "models": models,
                "recommended_models": recommended_models,
                "recommended_install": recommended_install,
            }
        )
        if spawn_attempted is not UNSET:
            field_dict["spawn_attempted"] = spawn_attempted
        if version is not UNSET:
            field_dict["version"] = version
        if error is not UNSET:
            field_dict["error"] = error
        if caste is not UNSET:
            field_dict["caste"] = caste

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_local_model_config_data import (
            AiLocalModelConfigData,
        )
        from ..models.caste_info import CasteInfo
        from ..models.caste_recommended_model import (
            CasteRecommendedModel,
        )
        from ..models.local_model import LocalModel

        d = dict(src_dict)
        runner_available = d.pop("runner_available")

        last_checked = d.pop("last_checked")

        local_model_config = AiLocalModelConfigData.from_dict(
            d.pop("local_model_config")
        )

        models = []
        _models = d.pop("models")
        for models_item_data in _models:
            models_item = LocalModel.from_dict(models_item_data)

            models.append(models_item)

        recommended_models = []
        _recommended_models = d.pop("recommended_models")
        for recommended_models_item_data in _recommended_models:
            recommended_models_item = CasteRecommendedModel.from_dict(
                recommended_models_item_data
            )

            recommended_models.append(recommended_models_item)

        recommended_install = []
        _recommended_install = d.pop("recommended_install")
        for recommended_install_item_data in _recommended_install:
            recommended_install_item = CasteRecommendedModel.from_dict(
                recommended_install_item_data
            )

            recommended_install.append(recommended_install_item)

        spawn_attempted = d.pop("spawn_attempted", UNSET)

        version = d.pop("version", UNSET)

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_caste(data: object) -> CasteInfo | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                caste_type_1 = CasteInfo.from_dict(data)

                return caste_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CasteInfo | None | Unset, data)

        caste = _parse_caste(d.pop("caste", UNSET))

        runner_capabilities_data = cls(
            runner_available=runner_available,
            last_checked=last_checked,
            local_model_config=local_model_config,
            models=models,
            recommended_models=recommended_models,
            recommended_install=recommended_install,
            spawn_attempted=spawn_attempted,
            version=version,
            error=error,
            caste=caste,
        )

        runner_capabilities_data.additional_properties = d
        return runner_capabilities_data

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
