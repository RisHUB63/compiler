from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # Identifier
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()

    # Symbols
    LPAREN = auto()
    RPAREN = auto()

    LBRACE = auto()
    RBRACE = auto()

    SEMICOLON = auto()

    COMMA = auto()

    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DEF = auto()
    RETURN = auto()
    PRINT = auto()

    # Special
    NEWLINE = auto()
    EOF = auto()

    LET = auto()

    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()



@dataclass
class Token:
    token_type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token("
            f"{self.token_type.name}, "
            f"{repr(self.value)}, "
            f"line={self.line}, "
            f"column={self.column})"
        )
