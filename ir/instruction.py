from enum import Enum, auto


class OpCode(Enum):

    LOAD_CONST = auto()
    LOAD = auto()
    STORE = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    PRINT = auto()

    # Control Flow
    LABEL = auto()
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    NEGATE = auto()


class Instruction:

    def __init__(self, opcode, operand=None):

        self.opcode = opcode
        self.operand = operand


    def __repr__(self):

        if self.operand is not None:

            return f"{self.opcode.name} {self.operand}"

        return self.opcode.name
