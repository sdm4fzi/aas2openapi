from enum import Enum


class GetSubmodelByIdExtent(str, Enum):
    WITHBLOBVALUE = "withBlobValue"
    WITHOUTBLOBVALUE = "withoutBlobValue"

    def __str__(self) -> str:
        return str(self.value)
