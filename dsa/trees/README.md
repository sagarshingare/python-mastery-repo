# Trees

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.8: Trees**

Binary Search Tree (BST) implementations, tree metrics, and recursive/iterative traversals.

## Key Data Structures & Functions

- **`TreeNode`**: Binary node structure with left/right pointers.
- **`BinarySearchTree`**: Ordered binary tree with insert, search ($O(h)$), and delete operations.
- **Traversals**: `inorder`, `preorder`, `postorder`, `level_order` (BFS breadth-first search).
- **Metrics**: `height()`, `is_balanced()` (AVL height balance check in $O(n)$).

## Quick Start

```python
from dsa.trees import BinarySearchTree, inorder

bst = BinarySearchTree()
for val in [50, 30, 70, 20, 40]:
    bst.insert(val)

assert inorder(bst.root) == [20, 30, 40, 50, 70]
assert bst.search(30) is True
```
