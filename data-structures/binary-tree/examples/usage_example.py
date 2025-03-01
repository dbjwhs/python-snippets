# MIT License
# Copyright (c) 2025 dbjwhs

"""Example usage of the BinaryTree class."""

import logging

from binary_tree import BinaryTree

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main() -> None:
    """Demonstrate basic usage of the BinaryTree class."""
    # Example with integers
    logger.info("Creating a tree of integers...")
    int_tree: BinaryTree[int] = BinaryTree()

    # Insert values to create the tree structure
    #        5
    #      /   \
    #     3     7
    #    / \   / \
    #   2   4 6   8
    int_tree.insert(5)
    int_tree.insert(3)
    int_tree.insert(7)
    int_tree.insert(2)
    int_tree.insert(4)
    int_tree.insert(6)
    int_tree.insert(8)

    # Test search operations
    logger.info("Search operations:")
    logger.info(f"Search for 5: {int_tree.search(5)}")
    logger.info(f"Search for 9: {int_tree.search(9)}")

    # Find min and max values
    logger.info(f"Minimum value: {int_tree.find_min_value()}")
    logger.info(f"Maximum value: {int_tree.find_max_value()}")

    # Test traversals
    logger.info("\nTraversals:")
    
    # In-order traversal (sorted order for BST)
    logger.info("In-order traversal:")
    in_order_results: list[int] = []
    int_tree.in_order_traversal(lambda x: in_order_results.append(x))
    logger.info(" ".join(str(x) for x in in_order_results))
    
    # Pre-order traversal
    logger.info("Pre-order traversal:")
    pre_order_results: list[int] = []
    int_tree.pre_order_traversal(lambda x: pre_order_results.append(x))
    logger.info(" ".join(str(x) for x in pre_order_results))
    
    # Post-order traversal
    logger.info("Post-order traversal:")
    post_order_results: list[int] = []
    int_tree.post_order_traversal(lambda x: post_order_results.append(x))
    logger.info(" ".join(str(x) for x in post_order_results))
    
    # Example with strings
    logger.info("\nCreating a tree of strings...")
    string_tree: BinaryTree[str] = BinaryTree()
    
    string_tree.insert("hello")
    string_tree.insert("abc")
    string_tree.insert("xyz")
    
    logger.info(f"Minimum string: {string_tree.find_min_value()}")
    logger.info(f"Maximum string: {string_tree.find_max_value()}")
    
    # String traversal
    logger.info("In-order traversal of string tree:")
    string_results: list[str] = []
    string_tree.in_order_traversal(lambda x: string_results.append(x))
    logger.info(" ".join(string_results))


if __name__ == "__main__":
    main()