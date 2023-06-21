from enum import Enum


class QualifierKind(str, Enum):
    CONCEPT_QUALIFIER = "CONCEPT_QUALIFIER"
    TEMPLATE_QUALIFIER = "TEMPLATE_QUALIFIER"
    VALUE_QUALIFIER = "VALUE_QUALIFIER"

    def __str__(self) -> str:
        return str(self.value)
