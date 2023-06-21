from enum import Enum


class MessageMessageType(str, Enum):
    ERROR = "Error"
    EXCEPTION = "Exception"
    INFO = "Info"
    UNDEFINED = "Undefined"
    WARNING = "Warning"

    def __str__(self) -> str:
        return str(self.value)
