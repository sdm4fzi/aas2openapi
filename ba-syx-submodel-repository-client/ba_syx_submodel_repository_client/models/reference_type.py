from enum import Enum


class ReferenceType(str, Enum):
    EXTERNAL_REFERENCE = "EXTERNAL_REFERENCE"
    MODEL_REFERENCE = "MODEL_REFERENCE"

    def __str__(self) -> str:
        return str(self.value)
