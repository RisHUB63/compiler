from enum import Enum, auto


class Type(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    VOID = auto()
    UNKNOWN = auto()

    def __str__(self):
        return self.name