from enum import Enum


class GetSubmodelElementByPathValueOnlySubmodelRepoLevel(str, Enum):
    CORE = "core"
    DEEP = "deep"

    def __str__(self) -> str:
        return str(self.value)
