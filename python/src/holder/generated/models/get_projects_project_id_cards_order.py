from enum import StrEnum


class GetProjectsProjectIdCardsOrder(StrEnum):
    CARD_ID_ASC = "card_id_asc"
    UPDATED_DESC = "updated_desc"

    def __str__(self) -> str:
        return str(self.value)
