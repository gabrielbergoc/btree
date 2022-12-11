import pytest
import re
from btree import BTree

from btreenode import BTreeNode

# examples:
#
# def foo():
#     return 1
#
# def test_foo():
#     assert foo() == 1
#
#
# def bar():
#     raise SystemExit[1]
#
# def test_bar():
#     with pytest.raises(SystemExit):
#         bar()
#

class TestBTree:

    @pytest.mark.parametrize("input_value,expected", [
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (20, 20),
        (23, 23),
        (0, None),
        (1, None),
        (-1, None),
        (100, None),
        (8.000001, None),
        (7.999999, None),
        (11.000001, None),
        (10.999999, None),
        (15.000001, None),
        (14.999999, None),
        (23.000001, None),
        (22.999999, None),
    ])
    def test_search(self, capsys, input_value, expected):
        # ----------------------------------------------------------------------
        # -------- ARRANGE --------- #

        # mount tree manually to not depend on insert method
        #
        #          11
        #      /        \
        #     9       16  18
        #   /  \    /   |    \
        #  8   10  15  17  20 23
        #
        
        tree = BTree(2, 11)

        leftChild = BTreeNode()
        leftChild._keys.extend([9])

        rightChild = BTreeNode()
        rightChild._keys.extend((16, 18))

        tree._root._children.extend((leftChild, rightChild))
        tree._root._is_leaf = False

        lleftChild = BTreeNode()
        lleftChild._is_leaf = True
        lleftChild._keys.extend([8])

        lrightChild = BTreeNode()
        lrightChild._is_leaf = True
        lrightChild._keys.extend([10])

        leftChild._children.extend((lleftChild, lrightChild))

        rleftChild = BTreeNode()
        rleftChild._is_leaf = True
        rleftChild._keys.extend([15])

        middleChild = BTreeNode()
        middleChild._is_leaf = True
        middleChild._keys.extend([17])
        
        rrightChild = BTreeNode()
        rrightChild._is_leaf = True
        rrightChild._keys.extend((20, 23))

        rightChild._children.extend((rleftChild, middleChild, rrightChild))

        # assert that tree is correctly constructed
        tree.print()
        
        out, err = capsys.readouterr()
        
        # this is the current default behavior of BTree.print method and could
        # potentially change in the future
        expected_out = "8 9 10 11 15 16 17 18 20 23 \n"

        assert out == expected_out
        
        # ----------------------------------------------------------------------
        # -------- ACT --------- #
        
        result = tree.search(input_value)
        
        # ----------------------------------------------------------------------
        # -------- ASSERT --------- #
        
        # for valid parameters
        if result is not None:
            node, i = result
            assert node.keys[i] == expected
        
        # for invalid parameters (search for elements not belonging in tree)
        # make sure the input isn't in the tree
        else:
            assert re.search(f" {str(input_value)} ", expected_out) is None
    
    def test_insert(self):
        tree = BTree(2)
        
        elements = [8, 9, 10, 11, 15, 16, 17, 18, 20, 23]
        
        for element in elements:
            tree.insert(element)
            
        # now this tree should be like this:
        #
        #          11
        #      /        \
        #     9       16  18
        #   /  \    /   |    \
        #  8   10  15  17  20 23
        #
        
        assert tree.root.keys[0] == 11
        
        lchild = tree.root.children[0]
        rchild = tree.root.children[1]
        
        assert lchild.keys[0] == 9
        assert rchild.keys[0] == 16
        assert rchild.keys[1] == 18
        
        llchild = lchild.children[0]
        lrchild = lchild.children[1]
        
        assert llchild.keys[0] == 8
        assert lrchild.keys[0] == 10
        
        rlchild = rchild.children[0]
        rmchild = rchild.children[1]
        rrchild = rchild.children[2]
        
        assert rlchild.keys[0] == 15
        assert rrchild.keys[0] == 20
        assert rrchild.keys[1] == 23
        
        # important flags!!!
        assert tree.root.is_leaf == False
        assert lchild.is_leaf == False
        assert rchild.is_leaf == False
        assert llchild.is_leaf == True
        assert lrchild.is_leaf == True
        assert rlchild.is_leaf == True
        assert rmchild.is_leaf == True
        assert rrchild.is_leaf == True
