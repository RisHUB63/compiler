from lexer.token import TokenType

from parser.ast import (
    Program,
    AssignmentStatement,
    VariableExpression,
    IntegerLiteral,
    BinaryExpression,
    PrintStatement,
    IfStatement,
    VariableDeclaration,
    StringLiteral,
    FloatLiteral,
    UnaryExpression
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    # ----------------------------------------------------
    # Helpers
    # ----------------------------------------------------

    @property
    def current(self):
        return self.tokens[self.position]

    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1

    def peek(self):
        if self.position + 1 >= len(self.tokens):
            return self.tokens[-1]

        return self.tokens[self.position + 1]

    def consume(self, expected_type):

        token = self.current

        if token.token_type != expected_type:
            raise Exception(
                f"Expected {expected_type.name}, "
                f"got {token.token_type.name}"
            )

        self.advance()

        return token

    # ----------------------------------------------------
    # Entry
    # ----------------------------------------------------

    def parse(self):

        statements = []

        while self.current.token_type != TokenType.EOF:

            if self.current.token_type == TokenType.NEWLINE:
                self.advance()
                continue

            statements.append(self.parse_statement())

        return Program(statements)

    # ----------------------------------------------------
    # Statements
    # ----------------------------------------------------

    def parse_statement(self):

        if (
            self.current.token_type == TokenType.IDENTIFIER
            and self.peek().token_type == TokenType.ASSIGN
        ):
            return self.parse_assignment()

        if self.current.token_type == TokenType.PRINT:
            return self.parse_print()

        if self.current.token_type == TokenType.IF:
            return self.parse_if()
        
        if self.current.token_type == TokenType.LET:
            return self.parse_variable_declaration()

        raise Exception(
            f"Unknown statement starting with {self.current.token_type.name}"
        )

    def parse_assignment(self):

        variable = VariableExpression(
            self.consume(TokenType.IDENTIFIER).value
        )

        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)

        return AssignmentStatement(
            target=variable,
            value=value,
        )

    # ----------------------------------------------------
    # Expressions
    # ----------------------------------------------------

    def parse_expression(self):

        node = self.parse_term()

        while self.current.token_type in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL
        ):

            operator = self.current.token_type

            self.advance()

            right = self.parse_term()

            node = BinaryExpression(
                left=node,
                operator=operator,
                right=right,
            )

        return node

    def parse_term(self):

        node = self.parse_factor()

        while self.current.token_type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):

            operator = self.current.token_type

            self.advance()

            right = self.parse_factor()

            node = BinaryExpression(
                left=node,
                operator=operator,
                right=right,
            )

        return node

    def parse_factor(self):

        token = self.current

        if self.current.token_type == TokenType.MINUS:
            operator = self.current
            self.advance()
            operand = self.parse_factor()
            return UnaryExpression(
                operator,
                operand
            )

        if token.token_type == TokenType.INTEGER:

            self.advance()

            return IntegerLiteral(
                value=int(token.value)
            )

        if token.token_type == TokenType.STRING:

            self.advance()

            return StringLiteral(
                token.value
            )

        if token.token_type == TokenType.IDENTIFIER:

            self.advance()

            return VariableExpression(
                name=token.value
            )

        if token.token_type == TokenType.LPAREN:

            self.advance()

            expression = self.parse_expression()

            self.consume(TokenType.RPAREN)

            return expression
        
        if token.token_type == TokenType.FLOAT:

            self.advance()

            return FloatLiteral(
                float(token.value)
            )

        raise Exception(
            f"Unexpected token {token.token_type.name}"
        )
    
    def parse_print(self):

        self.consume(TokenType.PRINT)

        self.consume(TokenType.LPAREN)

        expression = self.parse_expression()

        self.consume(TokenType.RPAREN)

        self.consume(TokenType.SEMICOLON)

        return PrintStatement(expression)

    
    def parse_if(self):

        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)

        then_body = []

        while self.current.token_type != TokenType.RBRACE:

            if self.current.token_type == TokenType.NEWLINE:
                self.advance()
                continue

            then_body.append(
                self.parse_statement()
            )

        self.consume(TokenType.RBRACE)

        # Skip newline between } and else
        while self.current.token_type == TokenType.NEWLINE:
            self.advance()

        else_body = None

        if self.current.token_type == TokenType.ELSE:
            self.advance()
            self.consume(TokenType.LBRACE)
            else_body = []

            while self.current.token_type != TokenType.RBRACE:

                if self.current.token_type == TokenType.NEWLINE:
                    self.advance()
                    continue

                else_body.append(
                    self.parse_statement()
                )

            self.consume(TokenType.RBRACE)

        return IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body
        )
    
    def parse_variable_declaration(self):

        self.consume(TokenType.LET)

        variable_name = self.consume(TokenType.IDENTIFIER).value

        variable = VariableExpression(
            name=variable_name
        )

        value = None

        if self.current.token_type == TokenType.ASSIGN:

            self.consume(TokenType.ASSIGN)

            value = self.parse_expression()

        self.consume(TokenType.SEMICOLON)

        return VariableDeclaration(
            variable=variable,
            value=value
        )