# Company-Wise Interview Tracks

> **Learning Path**: [Stage 03: LeetCode & Interview Practice](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-03-leetcode--interview-practice) — **Step 3.4** (Prerequisites: [Easy](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/easy), [Medium](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/medium), [Hard](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/hard))

Curated collections of high-frequency interview questions targeted specifically for premier technology companies: **Google**, **Meta (Facebook)**, **Amazon**, and **Microsoft**.

---

## Company Breakdown & Focus Areas

| Company | Key Algorithmic Patterns | High-Frequency Questions |
| :--- | :--- | :--- |
| **Google** | • Trie + Backtracking<br>• Streaming Median & Rate Limiting<br>• Sliding Window with Bounds<br>• Stack Parsers | • Word Search II (#212)<br>• Logger Rate Limiter (#359)<br>• Fruit Into Baskets (#904)<br>• Evaluate RPN (#150) |
| **Meta** | • Two Pointers Tolerance<br>• String Balance & Repairs<br>• Prefix Sum Frequency Hashing<br>• Binary Tree Coordinate Traversal | • Valid Palindrome II (#680)<br>• Minimum Remove Parentheses (#1249)<br>• Subarray Sum Equals K (#560)<br>• Vertical Order Traversal (#314) |
| **Amazon** | • Custom Comparator Sorting<br>• Multi-source BFS Outbreak<br>• Heaps & Spatial Proximity<br>• Graph Bridges (Tarjan's) | • Reorder Data in Log Files (#937)<br>• Rotting Oranges (#994)<br>• K Closest Points to Origin (#973)<br>• Critical Connections (#1192) |
| **Microsoft** | • Matrix Boundary Geometry<br>• Sign & Overflow Management<br>• Token Inversion<br>• Block-Reversal in Linked Lists | • Spiral Matrix II (#59)<br>• Sign of Product (#1822)<br>• Reverse Words (#151)<br>• Reverse Nodes in k-Group (#25) |

---

## Running Company Tracks

Run all company tracks:
```bash
python3 -m leetcode.company_wise.run_examples --company all
```

Or run any specific company track:
```bash
python3 -m leetcode.company_wise.run_examples --company google
python3 -m leetcode.company_wise.run_examples --company meta
python3 -m leetcode.company_wise.run_examples --company amazon
python3 -m leetcode.company_wise.run_examples --company microsoft
```
