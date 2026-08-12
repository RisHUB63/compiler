from dataclasses import dataclass
from semantic.types import Type


@dataclass
class Symbol:
    name: str
    type: Type
    mutable: bool = True
    initialized: bool = False