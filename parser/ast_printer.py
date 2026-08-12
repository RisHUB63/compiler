from parser.ast import *


class ASTPrinter:

    def print(self, node, indent=0):
        prefix = "│   " * indent

        # -------------------------------------------------
        # Program
        # -------------------------------------------------
        if isinstance(node, Program):
            print("Program")

            for statement in node.statements:
                self.print(statement, indent + 1)

        elif isinstance(node, VariableDeclaration):
            print(prefix + "├── VariableDeclaration")
            print(prefix + "│   Name: " + node.name)
            if node.value is not None:
                self.print(node.value, indent + 1)
        # -------------------------------------------------
        # Statements
        # -------------------------------------------------

        elif isinstance(node, AssignmentStatement):
            print(prefix + "├── Assignment")

            self.print(node.target, indent + 1)
            self.print(node.value, indent + 1)

        elif isinstance(node, PrintStatement):
            print(prefix + "├── Print")

            self.print(node.value, indent + 1)

        elif isinstance(node, ReturnStatement):
            print(prefix + "├── Return")

            if node.value:
                self.print(node.value, indent + 1)

        elif isinstance(node, IfStatement):
            print(prefix + "├── If")

            print(prefix + "│   Condition")
            self.print(node.condition, indent + 2)

            print(prefix + "│   Then")

            for statement in node.then_body:
                self.print(statement, indent + 2)

            if node.else_body:
                print(prefix + "│   Else")

                for statement in node.else_body:
                    self.print(statement, indent + 2)

        elif isinstance(node, WhileStatement):
            print(prefix + "├── While")

            print(prefix + "│   Condition")
            self.print(node.condition, indent + 2)

            print(prefix + "│   Body")

            for statement in node.body:
                self.print(statement, indent + 2)

        elif isinstance(node, FunctionDefinition):
            print(prefix + f"├── Function ({node.name})")

            if node.parameters:
                print(prefix + "│   Parameters")

                for parameter in node.parameters:
                    print(prefix + "│   ├── " + parameter)

            print(prefix + "│   Body")

            for statement in node.body:
                self.print(statement, indent + 2)

        # -------------------------------------------------
        # Expressions
        # -------------------------------------------------

        elif isinstance(node, BinaryExpression):
            print(prefix + f"├── Binary ({node.operator.name})")

            self.print(node.left, indent + 1)
            self.print(node.right, indent + 1)

        elif isinstance(node, UnaryExpression):
            print(prefix + f"├── Unary ({node.operator.name})")

            self.print(node.operand, indent + 1)

        elif isinstance(node, FunctionCall):
            print(prefix + f"├── Call ({node.name})")

            for argument in node.arguments:
                self.print(argument, indent + 1)

        elif isinstance(node, VariableExpression):
            print(prefix + f"├── Variable ({node.name})")

        elif isinstance(node, IntegerLiteral):
            print(prefix + f"├── Integer ({node.value})")

        elif isinstance(node, FloatLiteral):
            print(prefix + f"├── Float ({node.value})")

        elif isinstance(node, StringLiteral):
            print(prefix + f'├── String ("{node.value}")')
        
        elif isinstance(node, FloatLiteral):
            print(prefix + f"Float({node.value})")
        

        # -------------------------------------------------
        # Unknown
        # -------------------------------------------------

        else:
            raise Exception(
                f"Unknown AST node: {type(node).__name__}"
            )