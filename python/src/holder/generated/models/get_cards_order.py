from enum import StrEnum


class GetCardsOrder(StrEnum):
    TITLE_ASC = "title_asc"
    TREE_DEFAULT = "tree_default"
    UPDATED_DESC = "updated_desc"

    def __str__(self) -> str:
        return str(self.value)
