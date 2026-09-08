# LeetCode Hard Problems

> **Learning Path**: [Stage 03: LeetCode & Interview Practice](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-03-leetcode--interview-practice) — **Step 3.3** (Prerequisite: [Step 3.2: Medium Problems](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/medium))

A curated collection of **50+ LeetCode Hard problems** demonstrating advanced data structures, complex dynamic programming, monotonicity, and high-performance system designs.

---

## Topic Breakdown

| Topic | Problem IDs & Descriptions | Key Patterns |
| :--- | :--- | :--- |
| **Arrays & Binary Search** | • **#4 Median of Two Sorted Arrays**<br>• **#42 Trapping Rain Water**<br>• **#84 Largest Rectangle in Histogram** | Binary search on partition cut `O(log(min(m,n)))`, dual pointer elevation trap, monotonic increasing stack |
| **Strings & Backtracking** | • **#10 Regular Expression Matching**<br>• **#72 Edit Distance**<br>• **#37 Sudoku Solver**<br>• **#212 Word Search II** | 2D DP state machine with `*` kleene star, Levenshtein distance DP, constraint propagation backtracking, Trie + DFS matrix search |
| **Linked Lists & Trees** | • **#23 Merge k Sorted Lists**<br>• **#25 Reverse Nodes in k-Group**<br>• **#124 Binary Tree Maximum Path Sum**<br>• **#297 Serialize & Deserialize Binary Tree** | Min-heap pointer alignment `O(N log k)`, recursive k-group pointer rewiring, post-order DFS subtree gain, preorder traversal encoding |
| **Design & Advanced DP** | • **#146 LRU Cache**<br>• **#295 Find Median from Data Stream**<br>• **#123 Best Time to Buy/Sell Stock III**<br>• **#188 Best Time to Buy/Sell Stock IV**<br>• **#312 Burst Balloons** | Doubly-linked list + hash map `O(1)`, dual balancing heaps (max-heap / min-heap), multi-state finite state machine DP, interval DP |

---

## Running Demonstrations

Run all Hard demonstrations and validations:
```bash
python3 -m leetcode.hard.run_examples --topic all
```

Or target any specific topic:
```bash
python3 -m leetcode.hard.run_examples --topic arrays
python3 -m leetcode.hard.run_examples --topic strings
python3 -m leetcode.hard.run_examples --topic lists_trees
python3 -m leetcode.hard.run_examples --topic dp_design
python3 -m leetcode.hard.run_examples --topic test
```
