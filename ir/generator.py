from parser.ast import *

from ir.ir import IR
from ir.instruction import OpCode
from lexer.token import TokenType


class IRGenerator:

    BINARY_OPERATORS = {
        TokenType.PLUS: OpCode.ADD,
        TokenType.MINUS: OpCode.SUB,
        TokenType.STAR: OpCode.MUL,
        TokenType.SLASH: OpCode.DIV,
        TokenType.GREATER: OpCode.GREATER,
        TokenType.LESS: OpCode.LESS,
        TokenType.GREATER_EQUAL: OpCode.GREATER_EQUAL,
        TokenType.LESS_EQUAL: OpCode.LESS_EQUAL,
        TokenType.EQUAL_EQUAL: OpCode.EQUAL,
        TokenType.NOT_EQUAL: OpCode.NOT_EQUAL,
    }

    def __init__(self):
        self.ir = IR()
        self.label_count = 0


    def generate(self, program):
        for statement in program.statements:
            self.visit(statement)
        return self.ir

    def visit(self, node):
        method = getattr(
            self,
            f"visit_{type(node).__name__}",
            None
        )

        if method is None:
            raise Exception(
                f"No IR generator for {type(node).__name__}"
            )

        return method(node)
    
    def visit_IntegerLiteral(self, node):

        self.ir.emit(
            OpCode.LOAD_CONST,
            node.value
        )
    
    def visit_FloatLiteral(self, node):

        self.ir.emit(
            OpCode.LOAD_CONST,
            node.value
        )
    
    def visit_StringLiteral(self, node):

        self.ir.emit(
            OpCode.LOAD_CONST,
            node.value
        )
    
    def visit_VariableDeclaration(self, node):

        self.visit(node.value)
        self.ir.emit(
            OpCode.STORE,
            node.variable.name
        )
    
    def visit_AssignmentStatement(self,node):

        self.visit(node.value)
        self.ir.emit(
            OpCode.STORE,
            node.target.name
        )
    
    def visit_VariableExpression(self,node):

        self.ir.emit(
            OpCode.LOAD,
            node.name
        )
    
    def visit_BinaryExpression(self,node):

        self.visit(node.left)
        self.visit(node.right)

    
        opcode = self.BINARY_OPERATORS[
            node.operator
        ]
        self.ir.emit(opcode)
    
    def visit_PrintStatement(self,node):

        self.visit(node.value)
        self.ir.emit(
            OpCode.PRINT
        )
    
    def create_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def visit_IfStatement(self,node):
        else_label = self.create_label()
        end_label = self.create_label()

        # condition
        self.visit(node.condition)
        self.ir.emit(
            OpCode.JUMP_IF_FALSE,
            else_label
        )

        # if body
        for statement in node.then_body:
            self.visit(statement)

        self.ir.emit(
            OpCode.JUMP,
            end_label
        )

        # else block
        self.ir.emit(
            OpCode.LABEL,
            else_label
        )
        if node.else_body:
            for statement in node.else_body:
                self.visit(statement)

        self.ir.emit(
            OpCode.LABEL,
            end_label
        )
    
    def visit_UnaryExpression(self,node):

        self.visit(node.operand)
        if node.operator.token_type == TokenType.MINUS:
            self.ir.emit(
                OpCode.NEGATE
            )
