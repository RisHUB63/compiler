from semantic.symbol_table import SymbolTable
from semantic.errors import SemanticError


class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        self.table = SymbolTable()
    
    def lookup(self,name):

        if self.table.exists(name):
            return self.table.lookup(name)

        if self.parent:
            return self.parent.lookup(name)

        raise SemanticError(
            f"Variable '{name}' not declared"
        )
    
    def enter_scope(self):
        self.scope = Scope(
            parent=self.scope
        )

    def exit_scope(self):
        self.scope = self.scope.parent