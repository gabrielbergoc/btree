from __future__ import annotations
from typing import Any, Callable, Sequence


class BTreeNode:
    def __init__(self, *args: Any, is_leaf: bool = False):
        """If *args is given, initialize keys with its values.

        Args:
            *args (Any, optional): Initial keys.
            is_leaf (bool, optional): Flag to indicate if node is a leaf. Defaults to False.
        """
        self._keys: list[Any] = list(args)
        self._children: list[BTreeNode] = []
        self._is_leaf: bool = is_leaf

    @property
    def keys(self) -> list[Any]:
        """Getter for keys.

        Returns:
            list[Any]: A shallow copy of the node's keys list.
        """
        return self._keys[:]

    @property
    def children(self) -> list[BTreeNode]:
        """Getter for children

        Returns:
            list[BTreeNode]: A shallow copy of the node's children list.
        """
        return self._children[:]

    @property
    def n_keys(self) -> int:
        """Getter for current number of keys.

        Returns:
            int: Current number of keys in this node.
        """
        return len(self._keys)

    @property
    def n_children(self) -> int:
        """Getter for current number of children.

        Returns:
            int: Current number of children in this node.
        """
        return len(self._children)

    def is_leaf(self) -> bool:
        return self._is_leaf
    
    def get_key(self, i: int) -> Any:
        """Get key at index 'i'.

        Args:
            i (int): Index of the key to retrieve.

        Returns:
            Any: The key at given index.
            
        Raises: 
            IndexError: If index is out of range.
        """
        return self._keys[i]
    
    def get_child(self, i: int) -> BTreeNode:
        """Get child at index 'i'.

        Args:
            i (int): Index of the child to retrieve.

        Returns:
            Any: The child at given index.
            
        Raises: 
            IndexError: If index is out of range.
        """
        return self._children[i]
    
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
            self._keys.insert(i, key)
        else:
            self._keys.append(key)
        
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
            self._children.insert(i, child)
        else:
            self._children.append(child)

    def in_order(self, f: Callable, *args: tuple[Any], **kwargs: dict) -> None:
        """Traverses the tree in order, applying f to the keys.

        Args:
            f (function): function applyed to each key in order.
            *args: unnamed arguments passed to f on each call.
            **kwargs: keyword arguments passed to f on each call.
        """
        for i, value in enumerate(self._keys):
            if not self.is_leaf():
                self._children[i].in_order(f, *args, **kwargs)
            f(value, *args, **kwargs)

        if not self.is_leaf():
            self._children[-1].in_order(f, *args, **kwargs)
            
    def __str__(self):
        return f"{{ keys: {self._keys}, children: {self._children}, is_leaf: {self._is_leaf} }}"

    def __repr__(self) -> str:
        return self.__str__()

class BTree:
    def __init__(self, t: int = 2, rootVal: Any = None) -> None:
        """B-tree of minimum degree t, maximum degree 2*t, (minimum number of
        keys: t-1; maximum number of keys: 2*t-1). If 'rootVal' is given,
        initialize root with this value; else, root is None.

        Args:
            t (int, optional): Minimum node degree. Defaults to 2.
            rootVal (Any, optional): Value with which to initialize root. If
            None, root is None. Defaults to None.
        """
        self._t = t

        if rootVal is None:
            self._root = None
        else:
            self._root = BTreeNode(rootVal, is_leaf=True)

    @property
    def t(self) -> int:
        """Minimum degree of this tree (of each node).

        Returns:
            int: Minimum degree.
        """
        return self._t

    @property
    def root(self) -> BTreeNode:
        return self._root

    @property
    def min_keys(self) -> int:
        return self._t - 1

    @property
    def max_keys(self) -> int:
        return 2 * self.t - 1
    
    @property
    def min_children(self) -> int:
        return self._t

    @property
    def max_children(self) -> int:
        return 2 * self.t

    def is_full(self, node: BTreeNode) -> bool:
        """To check if given node is full (reached maximum number of keys/children).

        Args:
            node (BTreeNode): The node on which to perform the check.

        Returns:
            bool: True if node is full, False otherwise.
        """
        return node.n_keys == self.max_keys

    def search(self, key: Any) -> tuple[BTreeNode, int] | None:
        """Search for given key in this tree. If found, returns a tuple with
        both the node that contains the key and the index at which it is found
        in the node's keys list, None otherwise.

        Args:
            key (Any): The search key.

        Returns:
            tuple[BTreeNode, int] | None: Tuple with the node that contains the
            search key and the index at which it is found in the node's key
            list, or None if the key isn't found.
        """
        return self._search(key, self._root)

    def _search(self, key: Any, node: BTreeNode) -> tuple[BTreeNode, int] | None:
        """Recursively search for given key starting at given node.

        Args:
            key (Any): The search key.
            node (BTreeNode): The node on which to perform the search.

        Raises:
            ValueError: If either parameter is None.

        Returns:
            tuple[BTreeNode, int] | None: Tuple with the node that contains the
            search key and the index at which it is found in the node's key
            list, or None if the key isn't found.
        """
        if key is None or node is None:
            param = "key" if key is None else "node"
            raise ValueError(f"'{param}' parameter must not be None!!!")

        # encontrar nó que pode ter a chave desejada ou ter um filho que tenha
        i = 0
        while i < node.n_keys and key > node.get_key(i):
            i += 1

        # se i estiver dentro do limite da lista e o nó tiver a chave desejada,
        # retornar o nó e o índice da chave na lista
        if i < node.n_keys and key == node.get_key(i):
            return node, i

        # se keys[i-1] < key < keys[i] (ou key > max(keys)) e 'node' for folha,
        # a chave não existe
        if node.is_leaf():
            return None

        # em último caso, procurar pela chave no filho entre as chaves keys[i-1]
        # e keys[i] (ou o último filho, caso i tenha passado o limite da lista
        # de chaves)
        return self._search(key, node.get_child(i))

    def insert(self, key: Any) -> None:
        """Insert given key in this tree.

        Args:
            key (Any): The new key to insert.
        """
        if self._root is None:
            self._root = BTreeNode(key, is_leaf=True)
            return

        root = self._root

        if self.is_full(root):
            temp = BTreeNode()

            self._root = temp
            temp.insert_child(root)
            self._split_child(temp, 0)

            i = 0 if key < temp.get_key(0) else 1

            self._insert_non_full(temp.get_child(i), key)
            return

        self._insert_non_full(root, key)

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Helper method to insert a key in a non-full node.

        Args:
            node (BTreeNode): Node in which to insert new key.
            key (Any): The new key.
        """
        i = node.n_keys - 1
        while i >= 0 and node.get_key(i) > key:
            i -= 1

        if node.is_leaf():
            node.insert_key(key, i + 1)
            return

        if self.is_full(node.get_child(i + 1)):
            self._split_child(node, i + 1)
            if node.get_key(i + 1) < key:
                i += 1
                
        self._insert_non_full(node.get_child(i + 1), key)
        
    def _split_child(self, node: BTreeNode, i: int) -> None:
        """Split given node's i-th child and move its middle value up to given
        node.

        Args:
            node (BTreeNode): The node whose child to split, and which will
            receive the child's middle value.
            i (int): The index at which is found the child to split.
        """
        child = node.get_child(i)
        new = BTreeNode(is_leaf=child.is_leaf())
        
        for j in range(self.min_keys, self.max_keys + 1):
            new.insert_key(child.get_key(j))
            
        if not child.is_leaf():
            for j in range(self.min_children, self.max_children + 1):
                new.insert_child(child.get_child(j))
                
        child.insert_child(new, i + 1)
        child.insert_key(node.get_key(self._t - 1), i)

    def print(self, sep: str = " ") -> None:
        """Prints tree keys in order with given separator.

        Args:
            sep (str, optional): Inserted after each key. Defaults to " ".
        """
        self._root.in_order(print, end=sep)
        print()


def middle(sequence: Sequence) -> Any:
    """Returns the element in the middle of the given sequence."""
    l = len(sequence)
    return sequence[l // 2]
