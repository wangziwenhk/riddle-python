from . import node

class ProgramNode(node.SemNode):
    def __init__(self):
        super().__init__()
        self._commands: list[node.SemNode] = []

    def add(self, command: node.SemNode):
        self._commands.append(command)

    def __getitem__(self, item):
        return self._commands[item]

    def __iter__(self):
        return self._commands.__iter__()

    def __str__(self):
        temp = []
        for command in self._commands:
            temp.append(str(command))
        return str(temp)

    def accept(self, visitor):
        return visitor.visit_program(self)
