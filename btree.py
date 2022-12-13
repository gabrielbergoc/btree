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

        # variável privada para auxiliar o método print_tree
        self.__levels: list[list[object]] = []

    @property
    def t(self) -> int:
        """Minimum degree of this tree (of each node). Same as `min_children`.

        Returns:
            int: Minimum degree of this tree.
        """
        return self._t

    @property
    def root(self) -> BTreeNode | None:
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
        if self._root is None:
            return None
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

        # se raiz estiver cheia, realizar split preventivo
        if self.is_full(self._root):
            new_root = BTreeNode()
            new_root.insert_child(self._root)
            self._root = new_root

            self._split_child(new_root, 0)          # split da raiz antiga
            self._insert_non_full(new_root, key)    # insere nova chave
            return

        self._insert_non_full(self._root, key)

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Helper method to insert a key in a non-full node.

        Args:
            node (BTreeNode): Node in which to insert new key.
            key (Any): The new key.
        """
        # do fim para o começo, procurar o índice adequado de inserção da nova
        # chave
        i = node.n_keys
        while i >= 0 and node.get_key(i - 1) > key:
            i -= 1

        # base da recursão: inserir nova chave na folha, no índice adequado
        if node.is_leaf:
            node.insert_key(key, i)
            return

        # se o nó atual não for folha, verificar se o filho onde será inserida
        # a nova chave está cheio. se estiver, fazer split do filho
        if self.is_full(node.get_child(i)):
            self._split_child(node, i)

            # corrigir índice de inserção
            if node.get_key(i) < key:
                i += 1

        # inserir recursivamente nova chave no filho correto
        self._insert_non_full(node.get_child(i), key)

    def _split_child(self, node: BTreeNode, i: int) -> None:
        """Split given node's i-th child and move its middle value up to given
        node.

        Args:
            node (BTreeNode): The node whose child to split, and which will
            receive the child's middle value.
            i (int): The index at which is found the child to split.
        """
        child = node.get_child(i)                       # nó que será dividido
        new_child = BTreeNode(is_leaf=child.is_leaf)    # novo nó resultado da divisão
        node.insert_child(new_child, i + 1)             # inserir novo nó à direita do original
        node.insert_key(child.get_key(self._t - 1), i)  # passar a chave mediana um nível acima
        new_child._keys = child._keys[self._t:]         # transferir chaves maiores para o novo nó
        child._keys = child._keys[:self._t - 1]         # manter as chaves menores no original

        if not child.is_leaf:
            new_child._children = child._children[self._t:]     # transferir filhos maiores para o novo nó
            child._children = child._children[:self._t]         # manter filhos menores no original

    def print_inorder(self, sep: str = " ") -> None:
        """Prints tree keys in order with given separator.

        Args:
            sep (str, optional): Inserted after each key. Defaults to " ".
        """
        if self._root is None:
            print(None)
            return

        self._root.keys_inorder(print, end=sep)
        print()

    def visualize_tree(self) -> None:
        """Method to output the tree in a human-friendly format. It is
        recommended to redirect the output to a text file if the tree is too
        large.
        """
        if self._root is None:
            print(None)
            return

        self.__save_tree_info()

        buffer = ""

        for level in self.__levels:
            prev_end = 0

            for node in level:
                total = node["end"] - node["pos"]
                slack = total - len(str(node["keys"]))
                pad = node["pos"] - prev_end

                buffer += " " * (pad + slack // 2)
                buffer += str(node["keys"])
                buffer += " " * (slack - slack // 2)

                prev_end += pad + total

            buffer += "\n\n"

        print(buffer)

    def __save_tree_info(self) -> None:
        """Auxiliary method to save nodes' metadata to pretty-print tree in
        `visualize_tree`
        """
        if self._root is None:
            return

        self.__levels = []
        self.__save_node_info(self._root)

    def __save_node_info(self, node: BTreeNode, level: int = 0, i: int = 0) -> None:
        if node is None:
            raise ValueError("'node' parameter must not be None!!!")

        if level > len(self.__levels):
            raise ValueError("You shouldn't be accessing this level yet. Didn't you skip a level?")

        if level == len(self.__levels):
            self.__levels.append([])

        this_level = self.__levels[level]
        this_info = {"keys": str(node.keys), "pos": 0}

        if len(this_level) > 0:
            this_info.update({"pos": this_level[-1]["end"] + 2 if i == 0 else 1})

        if node.is_leaf:
            this_info.update({"end": this_info["pos"] + len(this_info["keys"])})
        else:
            for i, child in enumerate(node.children):
                self.__save_node_info(child, level + 1, i)

            this_info.update({"end": self.__levels[level + 1][-1]["end"]})

        this_level.append(this_info)


if __name__ == "__main__":
    tree = BTree(2)

    elements = [8, 9, 10, 11, 15, 16, 17, 18, 20, 23]

    for element in elements:
        tree.insert(element)

    tree.visualize_tree()
