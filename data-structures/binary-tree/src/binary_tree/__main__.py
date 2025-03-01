# MIT License
# Copyright (c) 2025 dbjwhs

"""Runnable module for binary tree."""

import logging
import sys

from .binary_tree import BinaryTree

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Demonstrate the BinaryTree functionality.
    
    Returns:
        0 for success, non-zero for failure
    """
    logger.info("Binary Tree Implementation Demo")
    logger.info("==============================")
    
    # Create an integer tree
    tree: BinaryTree[int] = BinaryTree()
    
    # Add some values
    for value in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(value)
        
    logger.info(f"Tree size: {len(tree)}")
    logger.info(f"Tree max depth: {tree.max_depth()}")
    logger.info(f"Is valid BST: {tree.is_valid_bst()}")
    
    # Traversals
    results: list[int] = []
    
    logger.info("\nIn-order traversal (should be sorted):")
    tree.in_order_traversal(lambda x: results.append(x))
    logger.info(" ".join(str(x) for x in results))
    results.clear()
    
    logger.info("\nPre-order traversal:")
    tree.pre_order_traversal(lambda x: results.append(x))
    logger.info(" ".join(str(x) for x in results))
    results.clear()
    
    logger.info("\nPost-order traversal:")
    tree.post_order_traversal(lambda x: results.append(x))
    logger.info(" ".join(str(x) for x in results))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())