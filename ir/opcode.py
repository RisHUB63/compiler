class OpCode(Enum):

    LOAD_CONST = auto()
    LOAD = auto()
    STORE = auto()

    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

    NEGATE = auto()

    PRINT = auto()


    # comparison

    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
