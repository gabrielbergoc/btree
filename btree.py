from typing import Any

from btreenode import BTreeNode


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
        if node.is_leaf:
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

        if self.is_full(self._root):
            new_root = BTreeNode()
            new_root.insert_child(self._root)
            self._root = new_root
            
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
            return

        self._insert_non_full(self._root, key)

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Helper method to insert a key in a non-full node.

        Args:
            node (BTreeNode): Node in which to insert new key.
            key (Any): The new key.
        """
        i = node.n_keys - 1
        while i >= 0 and node.get_key(i) > key:
            i -= 1

        if node.is_leaf:
            node.insert_key(key, i + 1)
            return

        i += 1
        if self.is_full(node.get_child(i)):
            self._split_child(node, i)
            if node.get_key(i) < key:
                i += 1
                
        self._insert_non_full(node.get_child(i), key)
        
    def _split_child(self, node: BTreeNode, i: int) -> None:
        """Split given node's i-th child and move its middle value up to given
        node.

        Args:
            node (BTreeNode): The node whose child to split, and which will
            receive the child's middle value.
            i (int): The index at which is found the child to split.
        """
        child = node.get_child(i)
        new = BTreeNode(is_leaf=child.is_leaf)                
        node.insert_child(new, i + 1)
        node.insert_key(child.get_key(self._t - 1), i)
        new._keys = child._keys[self._t:]
        child._keys = child._keys[:self._t - 1]
        if not child.is_leaf:
            new._children = child._children[self._t:]
            child._children = child._children[:self._t]

    def print(self, sep: str = " ") -> None:
        """Prints tree keys in order with given separator.

        Args:
            sep (str, optional): Inserted after each key. Defaults to " ".
        """
        self._root.in_order(print, end=sep)
        print()
