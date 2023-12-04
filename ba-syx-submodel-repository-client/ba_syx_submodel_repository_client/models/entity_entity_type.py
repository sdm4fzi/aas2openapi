from enum import Enum


class EntityEntityType(str, Enum):
    CO_MANAGED_ENTITY = "CO_MANAGED_ENTITY"
    SELF_MANAGED_ENTITY = "SELF_MANAGED_ENTITY"

    def __str__(self) -> str:
        return str(self.value)
