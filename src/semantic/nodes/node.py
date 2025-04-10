import abc

class SemNode:
    def __init__(self):
        pass

    @abc.abstractmethod
    def accept(self, visitor):
        return visitor.visit(self)


class PackageNode(SemNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return 'package: ' + self.name

    def accept(self, visitor):
        return visitor.visit_package(self)