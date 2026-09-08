"""Binary tree and binary search tree implementations."""

from __future__ import annotations

from collections import deque
from typing import Any, Generator


class TreeNode:
    """Node for a binary tree."""

    __slots__ = ("value", "left", "right")

    def __init__(
        self,
        value: Any,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.value!r})"


# ---------------------------------------------------------------------------
# Traversals
# ---------------------------------------------------------------------------

def inorder(root: TreeNode | None) -> list[Any]:
    """Inorder traversal (left → root → right). O(n)."""
    result: list[Any] = []

    def _walk(node: TreeNode | None) -> None:
        if node is None:
            return
        _walk(node.left)
        result.append(node.value)
        _walk(node.right)

    _walk(root)
    return result


def preorder(root: TreeNode | None) -> list[Any]:
    """Preorder traversal (root → left → right). O(n)."""
    result: list[Any] = []

    def _walk(node: TreeNode | None) -> None:
        if node is None:
            return
        result.append(node.value)
        _walk(node.left)
        _walk(node.right)

    _walk(root)
    return result


def postorder(root: TreeNode | None) -> list[Any]:
    """Postorder traversal (left → right → root). O(n)."""
    result: list[Any] = []

    def _walk(node: TreeNode | None) -> None:
        if node is None:
            return
        _walk(node.left)
        _walk(node.right)
        result.append(node.value)

    _walk(root)
    return result


def level_order(root: TreeNode | None) -> list[list[Any]]:
    """Level-order (BFS) traversal returning values grouped by level."""
    if root is None:
        return []
    result: list[list[Any]] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level_size = len(queue)
        level: list[Any] = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)
    return result


# ---------------------------------------------------------------------------
# Tree properties
# ---------------------------------------------------------------------------

def height(root: TreeNode | None) -> int:
    """Return the height of the tree (-1 for empty, 0 for single node)."""
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))


def is_balanced(root: TreeNode | None) -> bool:
    """Check whether the tree is height-balanced."""

    def _check(node: TreeNode | None) -> int:
        if node is None:
            return 0
        left_h = _check(node.left)
        right_h = _check(node.right)
        if left_h == -1 or right_h == -1 or abs(left_h - right_h) > 1:
            return -1
        return 1 + max(left_h, right_h)

    return _check(root) != -1


def lowest_common_ancestor(
    root: TreeNode | None,
    p: Any,
    q: Any,
) -> TreeNode | None:
    """Find the Lowest Common Ancestor (LCA) of two node values in a binary tree.

    Time Complexity: O(N), Space Complexity: O(H).
    """
    if root is None or root.value == p or root.value == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left is not None and right is not None:
        return root
    return left if left is not None else right


def is_valid_bst(
    root: TreeNode | None,
    min_val: float = float("-inf"),
    max_val: float = float("inf"),
) -> bool:
    """Validate whether a binary tree satisfies the Binary Search Tree invariant (strictly min < node < max).

    Time Complexity: O(N), Space Complexity: O(H).
    """
    if root is None:
        return True
    if not (min_val < root.value < max_val):
        return False
    return is_valid_bst(root.left, min_val, root.value) and is_valid_bst(
        root.right, root.value, max_val
    )


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """Invert (mirror) a binary tree in-place and return the root.

    Time Complexity: O(N), Space Complexity: O(H).
    """
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# ---------------------------------------------------------------------------
# Binary Search Tree
# ---------------------------------------------------------------------------

class BinarySearchTree:
    """A binary search tree supporting insert, search, delete, and traversal.

    Duplicate values are placed in the right subtree.
    """

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, value: Any) -> None:
        """Insert a value into the BST. O(h)."""
        self.root = self._insert(self.root, value)

    def _insert(self, node: TreeNode | None, value: Any) -> TreeNode:
        if node is None:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value: Any) -> bool:
        """Return True if *value* exists in the BST. O(h)."""
        return self._search(self.root, value)

    def _search(self, node: TreeNode | None, value: Any) -> bool:
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def delete(self, value: Any) -> None:
        """Delete a value from the BST. O(h)."""
        self.root = self._delete(self.root, value)

    def _delete(self, node: TreeNode | None, value: Any) -> TreeNode | None:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Node to delete found
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Two children: replace with inorder successor
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    @staticmethod
    def _find_min(node: TreeNode) -> TreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_min(self) -> Any:
        """Return the minimum value in the BST."""
        if self.root is None:
            raise ValueError("BST is empty")
        return self._find_min(self.root).value

    def find_max(self) -> Any:
        """Return the maximum value in the BST."""
        if self.root is None:
            raise ValueError("BST is empty")
        current = self.root
        while current.right is not None:
            current = current.right
        return current.value

    def inorder(self) -> list[Any]:
        """Return an inorder traversal of the BST (sorted order)."""
        return inorder(self.root)

    def level_order(self) -> list[list[Any]]:
        """Return a level-order traversal of the BST."""
        return level_order(self.root)
