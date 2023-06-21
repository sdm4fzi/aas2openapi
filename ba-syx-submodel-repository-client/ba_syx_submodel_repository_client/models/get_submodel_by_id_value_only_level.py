from enum import Enum


class GetSubmodelByIdValueOnlyLevel(str, Enum):
    CORE = "core"
    DEEP = "deep"

    def __str__(self) -> str:
        return str(self.value)
