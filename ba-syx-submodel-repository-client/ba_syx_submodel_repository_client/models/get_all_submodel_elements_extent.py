from enum import Enum


class GetAllSubmodelElementsExtent(str, Enum):
    WITHBLOBVALUE = "withBlobValue"
    WITHOUTBLOBVALUE = "withoutBlobValue"

    def __str__(self) -> str:
        return str(self.value)
