from enum import StrEnum


class AssetPlacementEncoding(StrEnum):
    HOLDER_ASSET_V1 = "holder_asset_v1"
    PLAIN = "plain"

    def __str__(self) -> str:
        return str(self.value)
