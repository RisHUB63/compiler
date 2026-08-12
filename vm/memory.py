class Memory:
    def __init__(self):
        self.variables = {}

    def store(self, name, value):
        self.variables[name] = value

    def load(self, name):
        if name not in self.variables:
            raise Exception(
                f"Variable '{name}' not found"
            )
        return self.variables[name]