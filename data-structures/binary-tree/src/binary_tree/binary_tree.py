# MIT License
# Copyright (c) 2025 dbjwhs

"""
Binary search tree implementation.

Key properties:
- Works with any comparable type
- Maintains BST invariants for arbitrary comparable types
- Provides O(log n) search efficiency when balanced
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

# Type variable for generic implementation
T = TypeVar('T')

# Configure logger
logger = logging.getLogger(__name__)


class BinaryTree(Generic[T]):
    """
    Binary Search Tree implementation.

    A binary search tree is a hierarchical data structure where each node has at most
    two children, and all values in the left subtree are less than the node's value,
    while all values in the right subtree are greater than the node's value.
    
    This implementation uses strong typing and supports any comparable type.
    """

    @dataclass
    class Node(Generic[T]):
        """Internal node structure for the binary tree."""
        
        data: T
        left: BinaryTree.Node[T] | None = None
        right: BinaryTree.Node[T] | None = None

    def __init__(self) -> None:
        """Initialize an empty binary tree."""
        self._root: BinaryTree.Node[T] | None = None
        self._size: int = 0

    def __len__(self) -> int:
        """Return the number of nodes in the tree."""
        return self._size

    def empty(self) -> bool:
        """Check if the tree is empty."""
        return self._size == 0

    def insert(self, value: T) -> None:
        """
        Insert a value into the binary search tree.
        
        If the value already exists, it will not be inserted again.
        
        Args:
            value: The value to insert
        """
        # Only insert if the value doesn't exist
        if not self.search(value):
            self._root = self._insert_helper(self._root, value)
            self._size += 1

    def _insert_helper(
        self, node: BinaryTree.Node[T] | None, value: T
    ) -> BinaryTree.Node[T]:
        """
        Helper function for BST insertion.
        
        Maintains BST property by recursively finding the correct position.
        
        Args:
            node: The current node being processed
            value: The value to insert
            
        Returns:
            The updated node after insertion
        """
        if node is None:
            return BinaryTree.Node(value)
        
        if value < node.data:
            node.left = self._insert_helper(node.left, value)
        elif node.data < value:  # Using < operator for consistency
            node.right = self._insert_helper(node.right, value)
            
        return node

    def search(self, value: T) -> bool:
        """
        Search for a value in the binary search tree.
        
        Time complexity: O(log n) when balanced, O(n) worst case.
        
        Args:
            value: The value to search for
            
        Returns:
            True if the value exists in the tree, False otherwise
        """
        return self._search_helper(self._root, value)
    
    def _search_helper(self, node: BinaryTree.Node[T] | None, value: T) -> bool:
        """
        Helper function for BST search.
        
        Uses BST property for O(log n) search.
        
        Args:
            node: The current node being processed
            value: The value to search for
            
        Returns:
            True if the value exists in the subtree, False otherwise
        """
        if node is None:
            return False
        
        # Equivalent to ==, handles custom types without requiring __eq__
        if not (node.data < value) and not (value < node.data):
            return True
        
        if value < node.data:
            return self._search_helper(node.left, value)
        
        return self._search_helper(node.right, value)

    def find_min_value(self) -> T:
        """
        Find the minimum value in the tree.
        
        Raises:
            RuntimeError: If the tree is empty
            
        Returns:
            The minimum value in the tree
        """
        min_node = self._find_min(self._root)
        if min_node is None:
            raise RuntimeError("Tree is empty")
        return min_node.data
    
    def _find_min(self, node: BinaryTree.Node[T] | None) -> BinaryTree.Node[T] | None:
        """
        Helper to find minimum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the minimum value, or None if the subtree is empty
        """
        if node is None:
            return None
        
        current = node
        while current.left is not None:
            current = current.left
            
        return current

    def find_max_value(self) -> T:
        """
        Find the maximum value in the tree.
        
        Raises:
            RuntimeError: If the tree is empty
            
        Returns:
            The maximum value in the tree
        """
        max_node = self._find_max(self._root)
        if max_node is None:
            raise RuntimeError("Tree is empty")
        return max_node.data
    
    def _find_max(self, node: BinaryTree.Node[T] | None) -> BinaryTree.Node[T] | None:
        """
        Helper to find maximum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the maximum value, or None if the subtree is empty
        """
        if node is None:
            return None
        
        current = node
        while current.right is not None:
            current = current.right
            
        return current

    def in_order_traversal(self, visit_func: Callable[[T], None]) -> None:
        """
        Perform an in-order traversal of the tree.
        
        In-order traversal visits nodes in ascending order for a BST.
        
        Algorithm:
        1. Create stack to track nodes during traversal
        2. Traverse left subtree to its leftmost node, pushing each node to stack
        3. When leftmost reached, pop and process node, then traverse its right child
        4. Continue until all nodes processed
        
        Time complexity: O(n) where n is number of nodes
        Space complexity: O(h) where h is height of tree
        
        Args:
            visit_func: Function to call for each node value
        """
        if self._root is None:
            return
        
        stack = []
        current = self._root
        
        while current is not None or stack:
            # Traverse to the leftmost node
            while current is not None:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            visit_func(current.data)
            
            # Traverse right subtree
            current = current.right

    def pre_order_traversal(self, visit_func: Callable[[T], None]) -> None:
        """
        Perform a pre-order traversal of the tree.
        
        Pre-order traversal visits root before children (root-left-right).
        
        Algorithm:
        1. Create stack and push root
        2. While stack not empty:
           - Pop and process current node
           - Push right child (if exists)
           - Push left child (if exists)
        3. Continue until stack empty
        
        Time complexity: O(n) where n is number of nodes
        Space complexity: O(h) where h is height of tree
        
        Args:
            visit_func: Function to call for each node value
        """
        if self._root is None:
            return
        
        stack = [self._root]
        
        while stack:
            current = stack.pop()
            
            # Process current node
            visit_func(current.data)
            
            # Push right then left (so left is processed first)
            if current.right is not None:
                stack.append(current.right)
            if current.left is not None:
                stack.append(current.left)

    def post_order_traversal(self, visit_func: Callable[[T], None]) -> None:
        """
        Perform a post-order traversal of the tree.
        
        Post-order traversal visits nodes after their children (left-right-root).
        
        Algorithm:
        1. Use two stacks: s1 for processing, s2 for final order
        2. Push root to s1
        3. While s1 not empty:
           - Pop node from s1 and push to s2
           - Push left child to s1 (if exists)
           - Push right child to s1 (if exists)
        4. Process s2 to get post-order traversal
        
        Time complexity: O(n) where n is number of nodes
        Space complexity: O(n) where n is number of nodes
        
        Args:
            visit_func: Function to call for each node value
        """
        if self._root is None:
            return
        
        s1 = [self._root]
        s2 = []
        
        while s1:
            current = s1.pop()
            s2.append(current)
            
            if current.left is not None:
                s1.append(current.left)
            if current.right is not None:
                s1.append(current.right)
        
        while s2:
            visit_func(s2.pop().data)

    def is_valid_bst(self) -> bool:
        """
        Validate that the tree follows binary search tree properties.
        
        BST invariants:
        - For any node n, all nodes in n's left subtree have values < n
        - For any node n, all nodes in n's right subtree have values > n
        - No duplicate values allowed
        
        Time complexity: O(n) where n is number of nodes
        Space complexity: O(h) where h is height of tree
        
        Returns:
            True if the tree is a valid BST, False otherwise
        """
        return self._is_valid_bst_helper(self._root)
    
    def _is_valid_bst_helper(
        self, 
        node: BinaryTree.Node[T] | None, 
        min_value: T | None = None, 
        max_value: T | None = None
    ) -> bool:
        """
        Helper function to validate BST property.
        
        Uses optional bounds to work with any comparable type.
        
        Args:
            node: The current node being processed
            min_value: The minimum allowed value for the subtree
            max_value: The maximum allowed value for the subtree
            
        Returns:
            True if the subtree is a valid BST, False otherwise
        """
        if node is None:
            return True
        
        # Check bounds if they exist
        if (min_value is not None and not (min_value < node.data)) or \
           (max_value is not None and not (node.data < max_value)):
            return False
        
        return (self._is_valid_bst_helper(node.left, min_value, node.data) and
                self._is_valid_bst_helper(node.right, node.data, max_value))

    def max_depth(self) -> int:
        """
        Find the maximum depth of the tree.
        
        The maximum depth is the number of nodes along the longest path from the
        root node down to the farthest leaf node.
        
        Returns:
            The maximum depth of the tree
        """
        return self._max_depth_helper(self._root)
    
    def _max_depth_helper(self, node: BinaryTree.Node[T] | None) -> int:
        """
        Helper function to find maximum depth.
        
        Args:
            node: The current node being processed
            
        Returns:
            The maximum depth of the subtree
        """
        if node is None:
            return 0
        
        return 1 + max(
            self._max_depth_helper(node.left),
            self._max_depth_helper(node.right)
        )
    
    def copy(self) -> BinaryTree[T]:
        """
        Create a deep copy of the tree.
        
        Returns:
            A new tree with the same structure and values
        """
        new_tree = BinaryTree[T]()
        new_tree._root = self._copy_tree(self._root)
        new_tree._size = self._size
        return new_tree
    
    def _copy_tree(self, node: BinaryTree.Node[T] | None) -> BinaryTree.Node[T] | None:
        """
        Helper function to copy all nodes recursively.
        
        Args:
            node: The current node being processed
            
        Returns:
            A copy of the subtree
        """
        if node is None:
            return None
        
        new_node = BinaryTree.Node(node.data)
        new_node.left = self._copy_tree(node.left)
        new_node.right = self._copy_tree(node.right)
        return new_node
        
    # Python-specific methods
    def __eq__(self, other: object) -> bool:
        """
        Check if two trees are equal.
        
        Two trees are equal if they have the same structure and the same values.
        
        Args:
            other: The other tree to compare with
            
        Returns:
            True if the trees are equal, False otherwise
        """
        if not isinstance(other, BinaryTree):
            return False
        
        # Quick size check before deep comparison
        if self._size != other._size:
            return False
        
        # Both empty trees are equal
        if self.empty() and other.empty():
            return True
        
        # Collect values in-order for comparison
        self_values: list[T] = []
        other_values: list[T] = []
        
        self.in_order_traversal(lambda x: self_values.append(x))
        other.in_order_traversal(lambda x: other_values.append(x))
        
        return self_values == other_values