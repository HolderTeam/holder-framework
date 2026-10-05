from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_context_breadcrumb_type import CardContextBreadcrumbType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardContextBreadcrumb")


@_attrs_define
class CardContextBreadcrumb:
    """
    Attributes:
        type_ (CardContextBreadcrumbType):
        title (str):
        project_id (None | str | Unset):
        card_id (None | str | Unset):
    """

    type_: CardContextBreadcrumbType
    title: str
    project_id: None | str | Unset = UNSET
    card_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        title = self.title

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        card_id: None | str | Unset
        if isinstance(self.card_id, Unset):
            card_id = UNSET
        else:
            card_id = self.card_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "title": title,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if card_id is not UNSET:
            field_dict["card_id"] = card_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = CardContextBreadcrumbType(d.pop("type"))

        title = d.pop("title")

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        card_id = _parse_card_id(d.pop("card_id", UNSET))

        card_context_breadcrumb = cls(
            type_=type_,
            title=title,
            project_id=project_id,
            card_id=card_id,
        )

        card_context_breadcrumb.additional_properties = d
        return card_context_breadcrumb

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
