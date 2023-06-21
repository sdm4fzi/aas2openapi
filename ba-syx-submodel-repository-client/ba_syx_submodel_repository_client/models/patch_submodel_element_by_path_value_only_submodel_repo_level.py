from enum import Enum


class PatchSubmodelElementByPathValueOnlySubmodelRepoLevel(str, Enum):
    CORE = "core"

    def __str__(self) -> str:
        return str(self.value)
