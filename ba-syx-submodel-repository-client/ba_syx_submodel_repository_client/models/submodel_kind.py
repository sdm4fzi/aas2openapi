from enum import Enum


class SubmodelKind(str, Enum):
    INSTANCE = "INSTANCE"
    TEMPLATE = "TEMPLATE"

    def __str__(self) -> str:
        return str(self.value)
