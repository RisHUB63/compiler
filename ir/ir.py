from ir.instruction import Instruction


class IR:

    def __init__(self):
        self.instructions = []


    def emit(self, opcode, operand=None):
        instruction = Instruction(
            opcode,
            operand
        )

        self.instructions.append(
            instruction
        )


    def dump(self):

        for instruction in self.instructions:
            print(instruction)
