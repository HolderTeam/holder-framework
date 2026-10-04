from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.card_context_breadcrumb import CardContextBreadcrumb
    from ..models.card_context_card import CardContextCard
    from ..models.card_context_data_project import CardContextDataProject


T = TypeVar("T", bound="CardContextData")


@_attrs_define
class CardContextData:
    """
    Attributes:
        project (CardContextDataProject):
        current_parent_card_id (None | str):
        breadcrumbs (list[CardContextBreadcrumb]):
        cards (list[CardContextCard]):
    """

    project: CardContextDataProject
    current_parent_card_id: None | str
    breadcrumbs: list[CardContextBreadcrumb]
    cards: list[CardContextCard]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project.to_dict()

        current_parent_card_id: None | str
        current_parent_card_id = self.current_parent_card_id

        breadcrumbs = []
        for breadcrumbs_item_data in self.breadcrumbs:
            breadcrumbs_item = breadcrumbs_item_data.to_dict()
            breadcrumbs.append(breadcrumbs_item)

        cards = []
        for cards_item_data in self.cards:
            cards_item = cards_item_data.to_dict()
            cards.append(cards_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "current_parent_card_id": current_parent_card_id,
                "breadcrumbs": breadcrumbs,
                "cards": cards,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_context_breadcrumb import (
            CardContextBreadcrumb,
        )
        from ..models.card_context_card import CardContextCard
        from ..models.card_context_data_project import (
            CardContextDataProject,
        )

        d = dict(src_dict)
        project = CardContextDataProject.from_dict(d.pop("project"))

        def _parse_current_parent_card_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        current_parent_card_id = _parse_current_parent_card_id(
            d.pop("current_parent_card_id")
        )

        breadcrumbs = []
        _breadcrumbs = d.pop("breadcrumbs")
        for breadcrumbs_item_data in _breadcrumbs:
            breadcrumbs_item = CardContextBreadcrumb.from_dict(breadcrumbs_item_data)

            breadcrumbs.append(breadcrumbs_item)

        cards = []
        _cards = d.pop("cards")
        for cards_item_data in _cards:
            cards_item = CardContextCard.from_dict(cards_item_data)

            cards.append(cards_item)

        card_context_data = cls(
            project=project,
            current_parent_card_id=current_parent_card_id,
            breadcrumbs=breadcrumbs,
            cards=cards,
        )

        card_context_data.additional_properties = d
        return card_context_data

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
