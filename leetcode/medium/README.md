# LeetCode Medium Problems

> **Learning Path**: [Stage 03: LeetCode & Interview Practice](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-03-leetcode--interview-practice) — **Step 3.2** (Prerequisite: [Step 3.1: Easy Problems](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/easy))

A curated collection of **80+ LeetCode Medium problems** covering core interview patterns, optimal multi-pass/two-pointer algorithms, tree/graph traversals, and dynamic programming.

---

## Topic Breakdown

| Topic | Problem IDs & Descriptions | Key Patterns |
| :--- | :--- | :--- |
| **Arrays & Two Pointers** | • **#15 3Sum**<br>• **#11 Container With Most Water**<br>• **#73 Set Matrix Zeroes**<br>• **#54 Spiral Matrix**<br>• **#621 Task Scheduler** | Two-pointer shrinking window, in-place matrix marker tracking, greedy frequency counting |
| **Strings & Parsing** | • **#3 Longest Substring Without Repeating**<br>• **#5 Longest Palindromic Substring**<br>• **#394 Decode String**<br>• **#227 Basic Calculator II**<br>• **#151 Reverse Words in a String** | Sliding window with hash sets, expand-around-center, stack-based nested decoding |
| **Linked Lists** | • **#24 Swap Nodes in Pairs**<br>• **#92 Reverse Linked List II**<br>• **#148 Sort List**<br>• **#160 Intersection of Two Linked Lists** | Dummy node sentinel, sublist reversal, merge sort on linked lists, dual pointer alignment |
| **Trees & Graphs** | • **#102 Binary Tree Level Order**<br>• **#98 Validate Binary Search Tree**<br>• **#105 Construct Tree from Pre/Inorder**<br>• **#200 Number of Islands** | BFS queue level order, DFS BST interval validation `(low, high)`, map-accelerated tree building, grid flood-fill DFS/BFS |
| **Dynamic Programming** | • **#139 Word Break**<br>• **#300 Longest Increasing Subsequence**<br>• **#152 Maximum Product Subarray**<br>• **#416 Partition Equal Subset Sum**<br>• **#494 Target Sum** | 1D boolean DP with prefix sets, patience sorting / DP, min/max tracking for negative factors, 0/1 knapsack reduction |

---

## Running Demonstrations

Run all Medium demonstrations and validations:
```bash
python3 -m leetcode.medium.run_examples --topic all
```

Or target any specific topic:
```bash
python3 -m leetcode.medium.run_examples --topic arrays
python3 -m leetcode.medium.run_examples --topic strings
python3 -m leetcode.medium.run_examples --topic trees_graphs
python3 -m leetcode.medium.run_examples --topic dp
python3 -m leetcode.medium.run_examples --topic test
```
