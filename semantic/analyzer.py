from parser.ast import *

from semantic.scope import Scope
from semantic.symbol import Symbol
from semantic.types import Type
from semantic.errors import SemanticError
from lexer.token import TokenType


class SemanticAnalyzer:

    def __init__(self):
        self.scope = Scope()

    def analyze(self, program):
        for statement in program.statements:
            self.visit(statement)

    def visit(self, node):
        method = getattr(
            self,
            f"visit_{type(node).__name__}",
            None
        )

        if method is None:
            raise SemanticError(
                f"No visitor for {type(node).__name__}"
            )

        return method(node)
    
    def visit_VariableDeclaration(self, node):

        value_type = Type.UNKNOWN

        if node.value:
            value_type = self.visit(node.value)

        symbol = Symbol(
            name=node.variable.name,
            type=value_type,
            initialized=node.value is not None
        )
        self.scope.table.declare(symbol)
    
    def visit_IntegerLiteral(self,node):
        node.inferred_type = Type.INTEGER
        return Type.INTEGER
    
    def visit_VariableExpression(self, node):
        symbol = self.scope.lookup(node.name)
        node.inferred_type = symbol.type
        return symbol.type
    
    def visit_AssignmentStatement(self, node):

        symbol = self.scope.table.lookup(
            node.target.name
        )
        value_type = self.visit(node.value)

        if symbol.type != Type.UNKNOWN:

            if symbol.type != value_type:
                raise SemanticError(
                    f"Cannot assign {value_type} "
                    f"to {symbol.type}"
                )

        symbol.type = value_type
        symbol.initialized = True
        
    def visit_PrintStatement(self, node):

        # Check the expression inside print()
        expression_type = self.visit(node.value)

        return Type.VOID
    
    def visit_BinaryExpression(self, node):
        if node.operator in [
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL
        ]:

            node.inferred_type = Type.BOOLEAN

            return Type.BOOLEAN

        left_type = self.visit(node.left)

        right_type = self.visit(node.right)


        if left_type == right_type:
            return left_type
        
        if (
            left_type == Type.INTEGER
            and right_type == Type.FLOAT
        ):
            node.inferred_type = Type.FLOAT
            return Type.FLOAT

        raise SemanticError(
            f"Cannot apply operator {node.operator} "
            f"between {left_type} and {right_type}"
        )
    
    def visit_StringLiteral(self, node):
        node.inferred_type = Type.STRING
        return Type.STRING
    
    def visit_FloatLiteral(self, node):
        node.inferred_type = Type.FLOAT
        return Type.FLOAT
    

    def visit_IfStatement(self, node):

        condition_type = self.visit(node.condition)

        if condition_type != Type.BOOLEAN:
            raise SemanticError(
                "If condition must be BOOLEAN"
            )

        # create new scope
        self.enter_scope()

        for statement in node.then_body:
            self.visit(statement)

        self.exit_scope()

        if node.else_body:
            self.enter_scope()
            for statement in node.else_body:
                self.visit(statement)

            self.exit_scope()
    

    def enter_scope(self):
        self.scope = Scope(
            parent=self.scope
        )

    def exit_scope(self):
        self.scope = self.scope.parent
    
    def visit_UnaryExpression(self, node):
        operand_type = self.visit(node.operand)

        if node.operator.token_type == TokenType.MINUS:
            if operand_type not in [
                Type.INTEGER,
                Type.FLOAT
            ]:
                raise SemanticError(
                    "Unary '-' can only be applied to numbers"
                )
            return operand_type

        raise SemanticError(
            f"Unsupported unary operator {node.operator.token_type}"
        )