from typing import Optional

import llvmlite.ir as ir

from src.semantic.node import SemNode


class Object:
    def __init__(self, name):
        self.name = name


class Variable(Object):
    def __init__(self, name, typ):
        super().__init__(name)
        self.type = typ
        self.alloca: Optional[ir.AllocaInstr] = None

    def set_alloca(self, alloca: ir.AllocaInstr):
        self.alloca = alloca


class Function(Object):
    def __init__(self, name, params, return_type, body: list[SemNode]):
        super().__init__(name)
        self.params = params
        self.return_type = return_type
        self.body = body
        self.llvm_func: Optional[ir.Function] = None

    def set_llvm_func(self, llvm_func: ir.Function):
        self.llvm_func = llvm_func


class ObjectManager:
    def __init__(self):
        self.objects: dict[str, list] = {}
        self.defined: list[set[str]] = []

    def add(self, name: str, obj):
        if name in self.defined[-1]:
            raise RuntimeError(f"Duplicate object '{name}'")
        if not name in self.objects:
            self.objects[name] = []
        self.objects[name].append(obj)

    def push(self):
        self.defined.append(set())

    def pop(self):
        for name in self.defined[-1]:
            self.objects[name].pop()
        self.defined.pop()

    def get(self, name: str):
        if name in self.objects:
            return self.objects[name]
        else:
            raise RuntimeError(f"Object '{name}' not defined")
