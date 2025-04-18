from __future__ import annotations
import enum

from . import node
from llvmlite import ir


class TypeNode(node.SemNode):
    def accept(self, visitor):
        return visitor.visit_type(self)

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.llvm_type: ir.Type

    def __str__(self):
        return 'type: ' + self.name


class ClassNode(TypeNode):
    def accept(self, visitor):
        return visitor.visit_class(self)

    def __init__(self, name: str, members: dict[str, node.SemNode]):
        super().__init__(name)
        self.members = members

    def __str__(self):
        return 'class: ' + self.name


class BaseTypeNode(TypeNode):
    class BaseTypeEnum(enum.IntEnum):
        int = enum.auto()
        float = enum.auto()
        double = enum.auto()
        long = enum.auto()
        short = enum.auto()
        char = enum.auto()
        bool = enum.auto()
        void = enum.auto()

    def __init__(self, base_type: BaseTypeEnum | str):
        self.base_type: BaseTypeNode.BaseTypeEnum
        if isinstance(base_type, str):
            super().__init__(base_type)
            try:
                self.base_type = BaseTypeNode.BaseTypeEnum[base_type]
            except KeyError:
                raise ValueError(f'invalid base type \"{base_type}\"')
        elif isinstance(base_type, self.BaseTypeEnum):
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

    @staticmethod
    def get_void():
        return BaseTypeNode(BaseTypeNode.BaseTypeEnum.void)

    def accept(self, visitor):
        return visitor.visit_type(self)
