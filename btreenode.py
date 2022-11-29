from __future__ import annotations
from typing import Any


class BTreeNode:
    def __init__(self, t: int = 2, is_leaf: bool = False):
        self._t = t
        self._values: list[Any] = []
        self._children: list[BTreeNode] = []
        self._is_leaf: bool = is_leaf

    @property
    def t(self):
        return self._t
    
    @property
    def max_keys(self):
        return 2 * self.t - 1
    
    @property
    def max_children(self):
        return 2 * self.t
    
    @property
    def values(self):
        return self._values
    
    @property
    def children(self):
        return self._children
    
    def is_leaf(self):
        return self._is_leaf
    
    def insert(self, value: Any):
        if value is None:
            raise ValueError("Parameter 'value' must not be None")
        
    def in_order(self, f: function):
        for i, value in (enumerate(self.values)):
            if not self.is_leaf():
                self.children[i].in_order(f)
            f(value)

        if not self.is_leaf():
            self.children[-1].in_order(f)
