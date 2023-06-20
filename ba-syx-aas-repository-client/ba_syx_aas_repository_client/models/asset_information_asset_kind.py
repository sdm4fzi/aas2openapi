from enum import Enum


class AssetInformationAssetKind(str, Enum):
    INSTANCE = "INSTANCE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    TYPE = "TYPE"

    def __str__(self) -> str:
        return str(self.value)
