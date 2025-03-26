import enum

from . import node
from llvmlite import ir


class TypeNode(node.SemNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.llvm_type: ir.Type


class ClassNode(TypeNode):
    def __init__(self, name: str, members: dict[str, node.SemNode]):
        super().__init__(name)
        self.members = members


class BaseTypeNode(TypeNode):
    class BaseTypeEnum(enum.IntEnum):
        int = enum.auto()
        float = enum.auto()
        double = enum.auto()
        long = enum.auto()
        short = enum.auto()
        char = enum.auto()
        bool = enum.auto()

    def __init__(self, base_type: BaseTypeEnum):
        super().__init__(base_type.name)
        self.base_type = base_type

    @staticmethod
    def get_int():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.int)

    @staticmethod
    def get_float():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.float)

    @staticmethod
    def get_double():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.double)

    @staticmethod
    def get_long():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.long)

    @staticmethod
    def get_short():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.short)

    @staticmethod
    def get_char():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.char)

    @staticmethod
    def get_bool():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.bool)