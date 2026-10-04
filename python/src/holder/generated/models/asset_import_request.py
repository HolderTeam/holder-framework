from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AssetImportRequest")


@_attrs_define
class AssetImportRequest:
    """
    Attributes:
        project_id (str):
        card_id (str):
        location_id (str):
        source_path (str): Local readable regular file; never persisted into project metadata.
    """

    project_id: str
    card_id: str
    location_id: str
    source_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        card_id = self.card_id

        location_id = self.location_id

        source_path = self.source_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "card_id": card_id,
                "location_id": location_id,
                "source_path": source_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        card_id = d.pop("card_id")

        location_id = d.pop("location_id")

        source_path = d.pop("source_path")

        asset_import_request = cls(
            project_id=project_id,
            card_id=card_id,
            location_id=location_id,
            source_path=source_path,
        )

        asset_import_request.additional_properties = d
        return asset_import_request

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
