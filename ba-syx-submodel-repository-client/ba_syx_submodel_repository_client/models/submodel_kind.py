from enum import Enum


class SubmodelKind(str, Enum):
    INSTANCE = "Instance"
    TEMPLATE = "Template"

    def __str__(self) -> str:
        return str(self.value)
