# Data Structures & Algorithms (DSA)

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) (Prerequisite: [Stage 01: Core Python](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python))

Structured implementations of algorithms, data structures, and system design structures in modern Python.

---

## Step-by-Step Learning Sequence

| Step | Subfolder | Key Concepts Covered |
|:---|:---|:---|
| **Step 2.1** | [`arrays/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/arrays) | Array operations, two pointers, prefix sums, two-sum variations |
| **Step 2.2** | [`strings/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/strings) | Palindromes, anagrams, KMP pattern matching, longest common prefix |
| **Step 2.3** | [`linked_list/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/linked_list) | `SinglyLinkedList`, `DoublyLinkedList`, reversal, cycle detection |
| **Step 2.4** | [`stack/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/stack) | `Stack`, `MinStack` (O(1)), balanced parentheses, postfix evaluation |
| **Step 2.5** | [`queue/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/queue) | `Queue`, `CircularQueue` (ring buffer), `PriorityQueue`, `Deque` |
| **Step 2.6** | [`recursion/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/recursion) | Divide-and-conquer, power sets, permutations, Tower of Hanoi, flood fill |
| **Step 2.7** | [`sliding_window/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/sliding_window) | Max sum subarray, k-distinct characters, minimum window substring |
| **Step 2.8** | [`trees/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/trees) | `BinarySearchTree`, traversals, LCA, BST validation, tree inversion |
| **Step 2.9** | [`heaps/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/heaps) | `MinHeap`, `MaxHeap`, heapsort, top-K elements, stream median finder |
| **Step 2.10** | [`graphs/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/graphs) | BFS, DFS, Kahn's topological sort, Dijkstra's algorithm, Disjoint Set Union (DSU) |
| **Step 2.11** | [`backtracking/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/backtracking) | N-Queens, Sudoku solver, subset sum, word search, parentheses |
| **Step 2.12** | [`dynamic_programming/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/dynamic_programming) | Memoization, tabulation, 0/1 knapsack, LCS, edit distance, coin change |
| **Step 2.13** | [`system_design/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa/system_design) | `LRUCache`, `LFUCache`, `Trie` with autocomplete prefix lookup, `BloomFilter` |

---

## Running Demonstrations

Run all DSA examples unified:
```bash
python3 -m dsa.run_examples --module all
```

Or run any specific submodule CLI:
```bash
python3 -m dsa.run_examples --module arrays
python3 -m dsa.run_examples --module trees
python3 -m dsa.run_examples --module graphs
python3 -m dsa.run_examples --module system_design
```

Or execute directly within any subfolder:
```bash
python3 -m dsa.arrays.run_examples --module all
```
