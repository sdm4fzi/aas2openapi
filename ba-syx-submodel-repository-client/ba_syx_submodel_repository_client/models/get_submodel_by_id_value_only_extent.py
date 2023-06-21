from enum import Enum


class GetSubmodelByIdValueOnlyExtent(str, Enum):
    WITHBLOBVALUE = "withBlobValue"
    WITHOUTBLOBVALUE = "withoutBlobValue"

    def __str__(self) -> str:
        return str(self.value)
