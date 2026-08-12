from lexer.token import Token, TokenType


KEYWORDS = {
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "def": TokenType.DEF,
    "return": TokenType.RETURN,
    "print": TokenType.PRINT,
    "let": TokenType.LET
}


class Lexer:

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def advance(self):
        if self.current_char() == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char() in " \t":
            self.advance()

    def read_number(self):
        start = self.position
        has_dot = False

        while (
            self.current_char() is not None
            and (
                self.current_char().isdigit()
                or self.current_char() == "."
            )
        ):

            if self.current_char() == ".":
                if has_dot:
                    break

                has_dot = True

            self.advance()

        value = self.source[start:self.position]

        if has_dot:
            return Token(
                TokenType.FLOAT,
                value,
                self.line,
                start
            )

        return Token(
            TokenType.INTEGER,
            value,
            self.line,
            start
        )

    def read_identifier(self):
        start = self.column
        text = ""

        while (
            self.current_char() is not None
            and (
                self.current_char().isalnum()
                or self.current_char() == "_"
            )
        ):
            text += self.current_char()
            self.advance()

        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        return Token(
            token_type,
            text,
            self.line,
            start,
        )

    def next_token(self):

        while self.current_char() is not None:

            if self.current_char() in " \t":
                self.skip_whitespace()
                continue

            if self.current_char() == "\n":
                token = Token(
                    TokenType.NEWLINE,
                    "\\n",
                    self.line,
                    self.column,
                )
                self.advance()
                return token
            
            if self.current_char() == "{":
                self.advance()
                return Token(
                    TokenType.LBRACE,
                    "{",
                    self.line,
                    self.column - 1
                )
            
            if self.current_char() == "}":
                self.advance()
                return Token(
                    TokenType.RBRACE,
                    "}",
                    self.line,
                    self.column - 1
                )
            
            if self.current_char() == ";":
                self.advance()
                return Token(
                    TokenType.SEMICOLON,
                    ";",
                    self.line,
                    self.column - 1
                )
            if self.current_char() == ">":
                self.advance()
                return Token(
                    TokenType.GREATER,
                    ">",
                    self.line,
                    self.column-1
                )
            
            if self.current_char() == "==":
                self.advance()
                return Token(
                    TokenType.EQUAL_EQUAL,
                    "==",
                    self.line,
                    self.column-1
                )
            
            if self.current_char() == "!=":
                self.advance()
                return Token(
                    TokenType.NOT_EQUAL,
                    "!=",
                    self.line,
                    self.column-1
                )
            
            if self.current_char() == ">=":
                self.advance()
                return Token(
                    TokenType.GREATER_EQUAL,
                    ">=",
                    self.line,
                    self.column-1
                )
            
            if self.current_char() == "<=":
                self.advance()
                return Token(
                    TokenType.LESS_EQUAL,
                    "<=",
                    self.line,
                    self.column-1
                )
            


            if self.current_char().isdigit():
                return self.read_number()

            if self.current_char().isalpha() or self.current_char() == "_":
                return self.read_identifier()
            
            if self.current_char() == '"':
                return self.read_string()

            ch = self.current_char()

            if ch == "+":
                self.advance()
                return Token(TokenType.PLUS, "+", self.line, self.column - 1)

            if ch == "-":
                self.advance()
                return Token(TokenType.MINUS, "-", self.line, self.column - 1)

            if ch == "*":
                self.advance()
                return Token(TokenType.STAR, "*", self.line, self.column - 1)

            if ch == "/":
                self.advance()
                return Token(TokenType.SLASH, "/", self.line, self.column - 1)

            if ch == "=":
                self.advance()
                return Token(TokenType.ASSIGN, "=", self.line, self.column - 1)

            if ch == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(", self.line, self.column - 1)

            if ch == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")", self.line, self.column - 1)

            if ch == ":":
                self.advance()
                return Token(TokenType.COLON, ":", self.line, self.column - 1)

            if ch == ",":
                self.advance()
                return Token(TokenType.COMMA, ",", self.line, self.column - 1)

            raise Exception(
                f"Unexpected character '{ch}' "
                f"at line {self.line}, column {self.column}"
            )

        return Token(
            TokenType.EOF,
            "",
            self.line,
            self.column,
        )
    
    def tokenize(self):
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.token_type == TokenType.EOF:
                break
        return tokens
    
    def read_string(self):

        self.advance()  # skip opening "

        value = ""

        while (
            self.current_char() is not None
            and self.current_char() != '"'
        ):
            value += self.current_char()
            self.advance()

        if self.current_char() == '"':
            self.advance()

        return Token(
            TokenType.STRING,
            value,
            self.line,
            self.column
        )
