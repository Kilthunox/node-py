

class Node:
    _parent = None
    _view: list = []
    _kwargs: dict = None
    _index: int = 0

    def __init__(self, name, *children: list, **kwargs: dict):
        self._name = name
        self._kwargs = kwargs
        self._view = [node._name for node in children]
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        for node in children:
            node._parent = self
            setattr(self, node._name, node)

    def __call__(self, name: str, *children, **kwargs):
        self._name = name
        self._kwargs.update(kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        for node in children:
            self.add_child(node)

    def __iter__(self):
        for node_name in self.get_view():
            yield self.getattr(node_name)

    def __getitem__(self, pointer: str):
        if pointer is None:
            return

        if pointer[0] == "/":
            attr = self.get_root()
            pointer = pointer[1:]
        else:
            attr = self

        for attr_name in pointer.split("/"):
            if not attr_name or attr_name == ".":
                continue
            elif attr_name == "..":
                attr = attr.get_parent()
            else:
                attr = attr.getattr(attr_name)
        return attr

    def __setitem__(self, pointer: str, value: any):
        if pointer is None:
            return

        if pointer[0] == "/":
            attr = self.get_root()
            pointer = pointer[1:]
        else:
            attr = self

        pointer_split = pointer.split("/")
        final_attr = pointer_split[-1]

        for attr_name in pointer_split[:-1]:
            if not attr_name or attr_name == ".":
                continue
            elif attr_name == "..":
                attr = attr.get_parent()
            else:
                attr = attr.getattr(attr_name)

        attr.setattr(final_attr, value)

    def __repr__(self):
        return f"<{self.get_pointer()}>"

    def show(self):
        if self.get_parent():
            if self._name not in self.get_parent().get_view():
                self.get_parent()._view.append(self._name)

    def hide(self):
        if self.get_parent():
            if self._name in self.get_parent().get_view():
                self.get_parent()._view.remove(self._name)

    def check_pointer(self, pointer: str) -> bool:
        if pointer is None:
            False

        if pointer[0] == "/":
            attr = self.get_root()
            pointer = pointer[1:]
        else:
            attr = self

        for attr_name in pointer.split("/"):
            if not attr_name or attr_name == ".":
                continue
            elif attr_name == "..":
                attr = attr.get_parent()
            else:
                if not hasattr(attr, attr_name):
                    return False
                else:
                    attr = attr.getattr(attr_name)
        return True

    @property
    def in_view(self) -> bool:
        node = self
        while node.get_parent() is not None:
            if node._name not in node.get_parent().get_view():
                return False
            node = node.get_parent()
        return True

    def initattr(self, attr: str, value: any):
        if not hasattr(self, attr):
            setattr(self, attr, value)
        elif self[attr] is None:
            setattr(self, attr, value)

    def setattr(self, attr: str, value: any):
        setattr(self, attr, value)

    def getattr(self, attr: str) -> any:
        try:
            return getattr(self, attr)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__}:{self.get_pointer()} has no attribute '{attr}'")

    def cascade(self, *signals):
        for signal in signals:
            self.get_root()[signal](self)
        for child in self:
            child.cascade(*signals)

    def set_parent(self, node):
        self._parent = node

    def sort_view(self):
        self.set_view([node._name for node in sorted(self.get_children(), key=lambda node: node._index)])

    def set_index(self, value: int):
        self._index = value

    def get_index(self) -> int:
        return self._index

    def get_children(self, key=lambda node: True):
        return list(filter(key, self))

    def add_child(self, child, index=None):
        if index is None:
            index = len(self.get_view())
        child.set_parent(self)
        self[child._name] = child
        self.view.insert(index, child._name)
        for setup_method in ("startup", "build", "fit"):
            child[setup_method]()
        self.sort_view()

    def clear_children(self, key=lambda node: True):
        for node in list(filter(key, self)):
            delattr(self, node._name)
            if node._name in self.get_view():
                self._view.remove(node._name)

    def remove_child(self, child_name):
        self._view.remove(child_name)
        delattr(self, child_name)

    def get_parent(self):
        return self._parent

    def get_root(self):
        if self.get_parent() is None:
            return self

        root = None
        next_node = self.get_parent()
        while root is None:
            if next_node.get_parent() is None:
                root = next_node
            else:
                next_node = next_node.get_parent()

        return root

    def get_pointer(self) -> str:
        next_node = self.get_parent()
        pointer_string = ""
        while next_node:
            if next_node.get_parent():
                pointer_string = f"/{next_node._name}{pointer_string}"
            next_node = next_node.get_parent()
        pointer_string += f"/{self._name}"

        return pointer_string

    def set_view(self, new_view: list):
        self._view = new_view

    def get_view(self) -> list:
        return self._view

    def build(self):
        for node in self:
            node.build()

    def run(self):
        for node in self:
            node.run()

