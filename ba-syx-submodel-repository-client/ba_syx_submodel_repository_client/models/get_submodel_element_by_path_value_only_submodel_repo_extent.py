from enum import Enum


class GetSubmodelElementByPathValueOnlySubmodelRepoExtent(str, Enum):
    WITHBLOBVALUE = "withBlobValue"
    WITHOUTBLOBVALUE = "withoutBlobValue"

    def __str__(self) -> str:
        return str(self.value)
