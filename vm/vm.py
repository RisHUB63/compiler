from vm.stack import Stack
from vm.memory import Memory

from ir.instruction import OpCode


class VirtualMachine:

    def __init__(self):
        self.stack = Stack()
        self.memory = Memory()
        self.ip = 0

    def run(self, instructions):
        self.ip = 0

        while self.ip < len(instructions):
            instruction = instructions[self.ip]
            self.execute(instruction)
            self.ip += 1
    
    def execute(self, instruction):

        opcode = instruction.opcode

        if opcode == OpCode.LOAD_CONST:
            self.stack.push(
                instruction.operand
            )

        elif opcode == OpCode.STORE:
            value = self.stack.pop()
            self.memory.store(
                instruction.operand,
                value
            )
        
        elif opcode == OpCode.NEGATE:
            value = self.stack.pop()
            self.stack.push(
                -value
            )

        elif opcode == OpCode.LOAD:
            value = self.memory.load(
                instruction.operand
            )
            self.stack.push(value)

        elif opcode == OpCode.PRINT:
            value = self.stack.pop()
            print(value)
        
        elif opcode == OpCode.ADD:

            right = self.stack.pop()
            left = self.stack.pop()

            self.stack.push(
                left + right
            )


        elif opcode == OpCode.SUB:

            right = self.stack.pop()
            left = self.stack.pop()

            self.stack.push(
                left - right
            )


        elif opcode == OpCode.MUL:

            right = self.stack.pop()
            left = self.stack.pop()

            self.stack.push(
                left * right
            )


        elif opcode == OpCode.DIV:

            right = self.stack.pop()
            left = self.stack.pop()

            self.stack.push(
                left / right
            )