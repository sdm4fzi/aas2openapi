from enum import Enum


class ReferenceType(str, Enum):
    EXTERNAL_REFERENCE = "ExternalReference"
    MODEL_REFERENCE = "ModelReference"

    def __str__(self) -> str:
        return str(self.value)
