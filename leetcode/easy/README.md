# LeetCode Easy Problems

> **Learning Path**: [Stage 03: LeetCode & Interview Practice](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-03-leetcode--interview-practice) — **Step 3.1** (Prerequisite: [Stage 02: DSA](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa))

A curated collection of **60+ LeetCode Easy problems** demonstrating foundational patterns, space-time optimizations, and production edge case handling.

---

## Topic Breakdown

| Topic | Problem IDs & Descriptions | Key Patterns |
| :--- | :--- | :--- |
| **Arrays & Hashing** | • **#1 Two Sum**<br>• **#217 Contains Duplicate**<br>• **#242 Valid Anagram**<br>• **#238 Product of Array Except Self**<br>• **#49 Group Anagrams** | Hash map complements, frequency tables, prefix/suffix products |
| **Strings & Two Pointers** | • **#125 Valid Palindrome**<br>• **#344 Reverse String**<br>• **#383 Ransom Note**<br>• **#205 Isomorphic Strings** | Two pointers inward, character normalization, character frequency checks |
| **Linked Lists** | • **#206 Reverse Linked List**<br>• **#141 Linked List Cycle**<br>• **#21 Merge Two Sorted Lists**<br>• **#234 Palindrome Linked List**<br>• **#2 Add Two Numbers** | Pointer rewiring, fast & slow pointers (Floyd's cycle finding), dummy heads |
| **Trees & Hierarchy** | • **#226 Invert Binary Tree**<br>• **#104 Maximum Depth**<br>• **#100 Same Tree**<br>• **#101 Symmetric Tree**<br>• **#110 Balanced Binary Tree**<br>• **#235 Lowest Common Ancestor (BST)** | Recursive divide-and-conquer, depth-first search, tree symmetry checks |
| **Dynamic Programming** | • **#70 Climbing Stairs**<br>• **#118 Pascal's Triangle**<br>• **#198 House Robber**<br>• **#53 Maximum Subarray**<br>• **#121 Best Time to Buy and Sell Stock** | 1D memoization, Kadane's algorithm, state transitions |
| **Stack & Queue** | • **#20 Valid Parentheses**<br>• **#155 Min Stack**<br>• **#232 Implement Queue using Stacks**<br>• **#150 Evaluate Reverse Polish Notation** | LIFO bracket matching, parallel min tracking, amortized O(1) push/pop |

---

## Running Demonstrations

Run all Easy demonstrations and validations:
```bash
python3 -m leetcode.easy.run_examples --topic all
```

Or target any specific topic:
```bash
python3 -m leetcode.easy.run_examples --topic arrays
python3 -m leetcode.easy.run_examples --topic trees
python3 -m leetcode.easy.run_examples --topic dp
python3 -m leetcode.easy.run_examples --topic stack
```
