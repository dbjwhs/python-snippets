# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the BinaryTree class."""

from typing import TypeVar

import pytest

from binary_tree import BinaryTree

T = TypeVar('T')


def test_empty_tree() -> None:
    """Test operations on an empty tree."""
    tree: BinaryTree[int] = BinaryTree()
    
    assert tree.empty()
    assert len(tree) == 0
    assert tree.max_depth() == 0
    assert tree.is_valid_bst()


def test_basic_operations() -> None:
    """Test basic BST operations like insert and search."""
    tree: BinaryTree[int] = BinaryTree()
    
    # Insert values
    tree.insert(5)  # root
    tree.insert(3)  # left of 5
    tree.insert(7)  # right of 5
    tree.insert(2)  # left of 3
    tree.insert(4)  # right of 3
    tree.insert(6)  # left of 7
    tree.insert(8)  # right of 7
    
    # Verify BST property
    assert tree.is_valid_bst()
    
    # Test search functionality
    assert tree.search(5)  # root
    assert tree.search(2)  # leaf
    assert tree.search(7)  # internal node
    assert not tree.search(1)  # non-existent value
    assert not tree.search(9)  # non-existent value


def test_duplicate_insertion() -> None:
    """Test that duplicates are not inserted into the tree."""
    tree: BinaryTree[int] = BinaryTree()
    
    tree.insert(5)
    size_before = len(tree)
    
    # Try to insert duplicate
    tree.insert(5)
    
    # Size should not change
    assert len(tree) == size_before


def test_min_max_functions() -> None:
    """Test min and max value functions."""
    tree: BinaryTree[int] = BinaryTree()
    
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    tree.insert(2)
    tree.insert(4)
    tree.insert(6)
    tree.insert(8)
    
    assert tree.find_min_value() == 2
    assert tree.find_max_value() == 8


def test_min_max_empty_tree() -> None:
    """Test min and max functions on empty tree should raise."""
    tree: BinaryTree[int] = BinaryTree()
    
    with pytest.raises(RuntimeError):
        tree.find_min_value()
        
    with pytest.raises(RuntimeError):
        tree.find_max_value()


def test_traversals() -> None:
    """Test all tree traversal methods."""
    tree: BinaryTree[int] = BinaryTree()
    
    # Create a BST
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    tree.insert(2)
    tree.insert(4)
    tree.insert(6)
    tree.insert(8)
    
    # Capture traversal results
    inorder_result: list[int] = []
    preorder_result: list[int] = []
    postorder_result: list[int] = []
    
    # Perform traversals
    tree.in_order_traversal(lambda x: inorder_result.append(x))
    tree.pre_order_traversal(lambda x: preorder_result.append(x))
    tree.post_order_traversal(lambda x: postorder_result.append(x))
    
    # Verify results
    assert inorder_result == [2, 3, 4, 5, 6, 7, 8]
    assert preorder_result == [5, 3, 2, 4, 7, 6, 8]
    assert postorder_result == [2, 4, 3, 6, 8, 7, 5]


def test_empty_traversals() -> None:
    """Test traversals on an empty tree."""
    empty_tree: BinaryTree[int] = BinaryTree()
    empty_result: list[int] = []
    
    # Traversals on empty tree should not add any values
    empty_tree.in_order_traversal(lambda x: empty_result.append(x))
    assert len(empty_result) == 0
    
    empty_tree.pre_order_traversal(lambda x: empty_result.append(x))
    assert len(empty_result) == 0
    
    empty_tree.post_order_traversal(lambda x: empty_result.append(x))
    assert len(empty_result) == 0


def test_single_node_traversals() -> None:
    """Test traversals on a tree with a single node."""
    single_node_tree: BinaryTree[int] = BinaryTree()
    single_node_tree.insert(1)
    
    # Results for all traversals should be the same for a single node
    inorder_result: list[int] = []
    preorder_result: list[int] = []
    postorder_result: list[int] = []
    
    single_node_tree.in_order_traversal(lambda x: inorder_result.append(x))
    assert inorder_result == [1]
    
    single_node_tree.pre_order_traversal(lambda x: preorder_result.append(x))
    assert preorder_result == [1]
    
    single_node_tree.post_order_traversal(lambda x: postorder_result.append(x))
    assert postorder_result == [1]


def test_copy_constructor() -> None:
    """Test the copy method creates a deep copy."""
    tree1: BinaryTree[int] = BinaryTree()
    
    for value in [5, 3, 7, 2, 4, 6, 8]:
        tree1.insert(value)
    
    # Create a copy
    tree2 = tree1.copy()
    
    # Check equality
    assert tree2.is_valid_bst()
    assert len(tree2) == len(tree1)
    assert tree2.find_min_value() == tree1.find_min_value()
    assert tree2.find_max_value() == tree1.find_max_value()
    
    # Check that it's a deep copy (modifying tree1 doesn't affect tree2)
    tree1.insert(1)
    assert len(tree1) != len(tree2)
    assert tree1.find_min_value() != tree2.find_min_value()


def test_equality() -> None:
    """Test tree equality."""
    tree1: BinaryTree[int] = BinaryTree()
    tree2: BinaryTree[int] = BinaryTree()
    
    # Empty trees should be equal
    assert tree1 == tree2
    
    # Same trees should be equal
    for value in [5, 3, 7, 2, 4, 6, 8]:
        tree1.insert(value)
        tree2.insert(value)
    
    assert tree1 == tree2
    
    # Different trees should not be equal
    tree3: BinaryTree[int] = BinaryTree()
    for value in [5, 3, 7, 2, 4, 6, 9]:  # Different from tree1
        tree3.insert(value)
    
    assert tree1 != tree3


def test_string_tree() -> None:
    """Test tree with string values."""
    string_tree: BinaryTree[str] = BinaryTree()
    
    # Basic string tests
    assert string_tree.empty()
    
    string_tree.insert("hello")
    string_tree.insert("abc")
    string_tree.insert("xyz")
    
    assert string_tree.is_valid_bst()
    assert string_tree.find_min_value() == "abc"
    assert string_tree.find_max_value() == "xyz"
    
    # Test string traversal
    inorder_string_result: list[str] = []
    string_tree.in_order_traversal(lambda x: inorder_string_result.append(x))
    
    assert inorder_string_result == ["abc", "hello", "xyz"]