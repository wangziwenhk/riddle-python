class ObjectManager:
    def __init__(self):
        self.objects: dict[str, list] = {}
        self.defined: list[set[str]] = []

    def add(self, name: str, obj):
        if name in self.defined[-1]:
            raise RuntimeError(f"Duplicate object '{name}'")
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