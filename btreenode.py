from __future__ import annotations
from typing import Any, Callable


class BTreeNode:
    def __init__(self, *args: Any, is_leaf: bool = False):
        """If *args is given, initialize keys with its values.

        Args:
            *args (Any, optional): Initial keys.
            is_leaf (bool, optional): Flag to indicate if node is a leaf. Defaults to False.
        """
        self.__keys: list[Any] = list(args)
        self.__children: list[BTreeNode] = []

    @property
    def keys(self) -> list[Any]:
        """Getter for keys.

        Returns:
            list[Any]: A shallow copy of the node's keys list.
        """
        return self.__keys[:]

    @property
    def children(self) -> list[BTreeNode]:
        """Getter for children

        Returns:
            list[BTreeNode]: A shallow copy of the node's children list.
        """
        return self.__children[:]
    
    @property
    def _keys(self) -> list[Any]:
        return self.__keys
    
    # protected getters and setters to facilitate some operations in BTree class
    @_keys.setter
    def _keys(self, keys: list[Any]) -> None:
        self.__keys = keys
        
    @property
    def _children(self) -> list[BTreeNode]:
        return self.__children
    
    @_children.setter
    def _children(self, children: list[BTreeNode]) -> None:
        self.__children = children

    @property
    def n_keys(self) -> int:
        """Getter for current number of keys.

        Returns:
            int: Current number of keys in this node.
        """
        return len(self.__keys)

    @property
    def n_children(self) -> int:
        """Getter for current number of children.

        Returns:
            int: Current number of children in this node.
        """
        return len(self.__children)

    @property
    def is_leaf(self) -> bool:
        return self.n_children == 0
    
    def get_key(self, i: int) -> Any:
        """Get key at index 'i'.

        Args:
            i (int): Index of the key to retrieve.

        Returns:
            Any: The key at given index.
            
        Raises: 
            IndexError: If index is out of range.
        """
        return self.__keys[i]
    
    def get_child(self, i: int) -> BTreeNode:
        """Get child at index 'i'.

        Args:
            i (int): Index of the child to retrieve.

        Returns:
            Any: The child at given index.
            
        Raises: 
            IndexError: If index is out of range.
        """
        return self.__children[i]
    
    def insert_key(self, key: Any, i: int | None = None) -> None:
        """Inserts given key at index i.

        Args:
            key (Any): New key to insert in this node.
            i (int | None): Index at which insert new key. If None, appends at
            the end. Defaults to None.

        Raises:
            TypeError: If 'key' is None.
        """
        if key is None:
            raise TypeError("'key' parameter must not be None")
        
        if i is not None:
            self.__keys.insert(i, key)
        else:
            self.__keys.append(key)
        
    def insert_child(self, child: BTreeNode, i: int | None = None) -> None:
        """Inserts given child at index i.

        Args:
            child (Any): New child to insert in this node.
            i (int | None, optional): Index at which insert new child. If None, appends
            at the end. Defaults to None.

        Raises:
            TypeError: If 'child' is None.
        """        
        if child is None:
            raise TypeError("'child' parameter must not be None")
        
        if i is not None:
            self.__children.insert(i, child)
        else:
            self.__children.append(child)

    def in_order(self, f: Callable, *args: tuple[Any], **kwargs: Any) -> None:
        """Traverses the tree in order, applying f to the keys.

        Args:
            f (function): function applyed to each key in order.
            *args: unnamed arguments passed to f on each call.
            **kwargs: keyword arguments passed to f on each call.
        """
        for i, value in enumerate(self.__keys):
            if not self.is_leaf:
                self.__children[i].in_order(f, *args, **kwargs)
            f(value, *args, **kwargs)

        if not self.is_leaf:
            self.__children[-1].in_order(f, *args, **kwargs)
            
    def __str__(self):
        return f"{{ keys: {self.__keys}, children: {self.__children}, is_leaf: {self._is_leaf} }}"

    def __repr__(self) -> str:
        return self.__str__()
