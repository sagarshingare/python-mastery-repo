"""Run Binary Tree and BST algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.trees.binary_tree import (
    BinarySearchTree,
    TreeNode,
    height,
    inorder,
    invert_tree,
    is_balanced,
    is_valid_bst,
    level_order,
    lowest_common_ancestor,
    postorder,
    preorder,
)

logger = logging.getLogger(__name__)


def run_bst_examples() -> None:
    logger.info("Running BinarySearchTree demonstrations")
    bst = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)

    print(f"Inorder (sorted): {bst.inorder()}")
    print(f"Level order: {bst.level_order()}")
    print(f"Contains 40: {bst.search(40)}, Contains 99: {bst.search(99)}")
    print(f"Min: {bst.find_min()}, Max: {bst.find_max()}")

    bst.delete(30)
    print(f"After delete(30), inorder: {bst.inorder()}")


def run_traversals_examples() -> None:
    logger.info("Running tree traversals (preorder, inorder, postorder, level_order)")
    # Construct tree:
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(f"Preorder:    {preorder(root)}")
    print(f"Inorder:     {inorder(root)}")
    print(f"Postorder:   {postorder(root)}")
    print(f"Level-order: {level_order(root)}")
    print(f"Tree height: {height(root)}, Is balanced: {is_balanced(root)}")


def run_lca_and_validation_examples() -> None:
    logger.info("Running LCA, BST validation, and Tree Inversion")
    # Tree:
    #        3
    #       / \
    #      5   1
    #     / \
    #    6   2
    root = TreeNode(
        3,
        TreeNode(5, TreeNode(6), TreeNode(2)),
        TreeNode(1),
    )
    lca_node = lowest_common_ancestor(root, 6, 2)
    print(f"LCA of 6 and 2: {lca_node.value if lca_node else None}")

    lca_node2 = lowest_common_ancestor(root, 6, 1)
    print(f"LCA of 6 and 1: {lca_node2.value if lca_node2 else None}")

    # BST validation
    bst_root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6))
    non_bst = TreeNode(4, TreeNode(5), TreeNode(6))
    print(f"Is valid BST (bst_root): {is_valid_bst(bst_root)}")
    print(f"Is valid BST (non_bst): {is_valid_bst(non_bst)}")

    # Invert tree
    print(f"Original level-order: {level_order(bst_root)}")
    invert_tree(bst_root)
    print(f"Inverted level-order: {level_order(bst_root)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Tree examples")
    parser.add_argument(
        "--module",
        choices=["bst", "traversals", "advanced", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "bst":
        run_bst_examples()
    elif args.module == "traversals":
        run_traversals_examples()
    elif args.module == "advanced":
        run_lca_and_validation_examples()
    else:
        run_bst_examples()
        run_traversals_examples()
        run_lca_and_validation_examples()


if __name__ == "__main__":
    main()
