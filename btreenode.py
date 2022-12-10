from __future__ import annotations
from typing import Any, Callable, Sequence


class BTreeNode:
    def __init__(self, is_leaf: bool = False):
        self._keys: list[Any] = []
        self._children: list[BTreeNode] = []
        self._is_leaf: bool = is_leaf

    @property
    def keys(self):
        return self._keys

    @property
    def children(self):
        return self._children

    def is_leaf(self):
        return self._is_leaf

    def insert(self, value: Any):
        if value is None:
            raise ValueError("Parameter 'value' must not be None")

    def in_order(self, f: Callable, *args, **kwargs):
        """Traverses the tree in order, applying f to the keys.

        Args:
            f (function): function applyed to each key in order
            *args: unnamed arguments passed to f on each call
            **kwargs: keyword arguments passed to f on each call
        """

        for i, value in enumerate(self.keys):
            if not self.is_leaf():
                self.children[i].in_order(f, *args, **kwargs)
            f(value, *args, **kwargs)

        if not self.is_leaf():
            self.children[-1].in_order(f, *args, **kwargs)


class BTree:
    def __init__(self, t: int = 2, rootVal: Any = None) -> None:
        self._t = t
        self._root = BTreeNode()

        if rootVal is not None:
            self.root.keys.append(rootVal)

    @property
    def t(self):
        return self._t

    @property
    def root(self):
        return self._root
    
    @property
    def min_keys(self):
        return self._t - 1

    @property
    def max_keys(self):
        return 2 * self.t - 1

    @property
    def max_children(self):
        return 2 * self.t

    def search(self, key: Any) -> tuple[BTreeNode, int] | None:
        return self._search(key, self.root)

    def _search(self, key: Any, node: BTreeNode) -> tuple[BTreeNode, int] | None:
        if key is None or node is None:
            param = "key" if key is None else "node"
            raise ValueError(f"'{param}' parameter must not be None!!!")

        # encontrar nó que pode ter a chave desejada ou ter um filho que tenha
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # se i estiver dentro do limite da lista e o nó tiver a chave desejada,
        # retornar o nó e o índice da chave na lista
        if i < len(node.keys) and key == node.keys[i]:
            return node, i

        # se keys[i-1] < key < keys[i] (ou key > max(keys)) e 'node' for folha,
        # a chave não existe
        if node.is_leaf():
            return None

        # em último caso, procurar pela chave no filho entre as chaves keys[i-1]
        # e keys[i] (ou o último filho, caso i tenha passado o limite da lista
        # de chaves)
        return self._search(key, node.children[i])

    def print(self, sep: str = " ") -> None:
        """Prints tree keys in order with given separator.

        Args:
            sep (str, optional): Inserted after each key. Defaults to " ".
        """

        self.root.in_order(print, end=sep)
        print()


def middle(iter: Sequence) -> Any:
    """Returns the element in the middle of the given iterable."""
    l = len(iter)
    return iter[l // 2]
