from semantic.symbol import Symbol
from semantic.errors import SemanticError


class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def declare(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise SemanticError(
                f"Variable '{symbol.name}' already declared."
            )
        self.symbols[symbol.name] = symbol

    def lookup(self, name: str):
        if name not in self.symbols:
            raise SemanticError(
                f"Variable '{name}' not declared."
            )

        return self.symbols[name]

    def exists(self, name: str):
        return name in self.symbols

    def dump(self):

        print("\n===== SYMBOL TABLE =====")
        for symbol in self.symbols.values():
            print(symbol)
        print("========================")