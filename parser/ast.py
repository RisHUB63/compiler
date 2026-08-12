"""
Abstract Syntax Tree (AST)

Every program is represented as a tree of nodes.

Example:

x = 5 + 10

Program
└── AssignmentStatement
    ├── VariableExpression("x")
    └── BinaryExpression(+)
        ├── IntegerLiteral(5)
        └── IntegerLiteral(10)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ============================================================
# Base Nodes
# ============================================================

class ASTNode:
    """Base class of every node."""
    pass


class Statement(ASTNode):
    """Base class of every statement."""
    pass


class Expression(ASTNode):
    """Base class of every expression."""
    pass


# ============================================================
# Program
# ============================================================

@dataclass
class Program(ASTNode):
    statements: List[Statement] = field(default_factory=list)


# ============================================================
# Literals
# ============================================================
@dataclass
class IntegerLiteral(Expression):
    value: int
    inferred_type: Type = None

@dataclass
class FloatLiteral(Expression):
    value: float
    inferred_type: object = None


@dataclass
class StringLiteral(Expression):
    value: str
    inferred_type: object = None


# ============================================================
# Variables
# ============================================================

@dataclass
class VariableExpression(Expression):
    name: str
    inferred_type: object = None


class UnaryExpression(Expression):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


# ============================================================
# Binary Expressions
# ============================================================

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: object
    right: Expression
    inferred_type: object = None


# ============================================================
# Unary Expressions
# ============================================================

@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression


# ============================================================
# Assignment
# ============================================================

@dataclass
class AssignmentStatement(Statement):
    target: VariableExpression
    value: Expression


# ============================================================
# Print
# ============================================================

@dataclass
class PrintStatement(Statement):
    value: Expression


# ============================================================
# Return
# ============================================================

@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression]


# ============================================================
# If
# ============================================================

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_body: List[Statement]
    else_body: Optional[List[Statement]] = None


# ============================================================
# While
# ============================================================

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: List[Statement]


# ============================================================
# Function Call
# ============================================================

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]


# ============================================================
# Function Definition
# ============================================================

@dataclass
class FunctionDefinition(Statement):
    name: str
    parameters: List[str]
    body: List[Statement]


# ============================================================
# Variable Definition
# ============================================================

@dataclass
class VariableDeclaration(Statement):
    variable: VariableExpression
    value: Expression | None

# ============================================================
# Print Statement Definition
# ============================================================

@dataclass
class PrintStatement(Statement):
    value: Expression
