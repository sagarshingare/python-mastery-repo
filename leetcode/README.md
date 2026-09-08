# LeetCode Solutions - Python

> **Learning Path**: [Stage 03: LeetCode & Interview Practice](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-03-leetcode--interview-practice) (Prerequisites: [Stage 01: Core Python](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python), [Stage 02: DSA](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa))

A comprehensive, production-hardened suite of **300+ LeetCode problems** and **FAANG/Tier-1 Company Interview Tracks** with detailed algorithmic explanations, asymptotic complexity analysis, and modular CLI runners.

---

## 📊 Problem & Track Statistics

| Module / Track | Path | Count | Key Focus Areas |
|:---|:---|:---|:---|
| **Step 3.1: Easy** | [`leetcode/easy/`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/easy) | 60+ problems | Two Pointers, In-place reversal, BFS/DFS basics, 1D DP, MinStack |
| **Step 3.2: Medium** | [`leetcode/medium/`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/medium) | 80+ problems | Sliding Window, BST validation, Flood fill, 2D DP, Backtracking |
| **Step 3.3: Hard** | [`leetcode/hard/`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/hard) | 50+ problems | Partition binary search, Monotonic stacks, LRU cache, Interval DP |
| **Step 3.4: Company-Wise** | [`leetcode/company_wise/`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/company_wise) | 16 core tracks | High-frequency problems for Google, Meta, Amazon, Microsoft |

---

## 🏢 Step 3.4: Company-Wise Interview Tracks

Targeted interview tracks focusing on algorithmic patterns frequently tested at top technology firms:

- **Google Track** ([`company_wise/google.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/company_wise/google.py)):
  - **#359 Logger Rate Limiter**: Stream sliding window deduplication and timestamp caching
  - **#904 Fruit Into Baskets**: At-most-2 distinct elements sliding window
  - **#212 Word Search II**: Prefix Trie paired with recursive backtracking on 2D grids
  - **#150 Evaluate Reverse Polish Notation**: Stack-based operand evaluation with truncation toward zero

- **Meta Track** ([`company_wise/meta.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/company_wise/meta.py)):
  - **#680 Valid Palindrome II**: Two-pointer fault-tolerant mismatch skipping
  - **#1249 Minimum Remove to Make Valid Parentheses**: Dual-pass index set filtering
  - **#560 Subarray Sum Equals K**: Cumulative prefix sum frequency hash map `O(N)`
  - **#314 Binary Tree Vertical Order Traversal**: BFS column-coordinate tracking with left-to-right determinism

- **Amazon Track** ([`company_wise/amazon.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/company_wise/amazon.py)):
  - **#937 Reorder Data in Log Files**: Multi-key tuple sorting with stable fallback
  - **#994 Rotting Oranges**: Multi-source BFS queue with elapsed step counting
  - **#973 K Closest Points to Origin**: Max-heap bounding `O(N log K)` vs. QuickSelect
  - **#1192 Critical Connections in a Network**: Tarjan's Bridge Finding with discovery/low-link timestamps

- **Microsoft Track** ([`company_wise/microsoft.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode/company_wise/microsoft.py)):
  - **#59 Spiral Matrix II**: Boundary contraction matrix population
  - **#1822 Sign of the Product of an Array**: Zero-check parity accumulation `O(1)` space
  - **#151 Reverse Words in a String**: In-place sentence tokenization and word flipping
  - **#25 Reverse Nodes in k-Group**: Pointer group reversal with dummy sentinel

---

## 🏭 Production Use Cases

Algorithms and data structure optimizations are mirrored in production software engineering:

- **Arrays & Hashing**: In-memory caching, real-time rate limiting, event stream deduplication, and fast lookup tables.
- **Strings & Parsing**: Query parsing, tokenization, serialization/deserialization protocols, and AST evaluation.
- **Linked Lists**: Streaming buffer queues, LRU/LFU cache evictions, and low-latency packet sequencing.
- **Trees & Graphs**: Dependency resolution, hierarchical RBAC trees, service mesh topology routing, and distributed cycle detection.
- **Dynamic Programming**: Resource allocation, cost optimization, query execution plan costing, and network flow management.

---

## 🚀 Execution & CLI Guide

### 1. Unified LeetCode Showcase
Run representative problems across all tiers and company tracks:
```bash
python3 -m leetcode.examples
```

### 2. Interactive Problem Runner CLI
Explore, inspect, run, and test individual problems:
```bash
# List problems by difficulty or category
python3 -m leetcode.run_problems list --difficulty easy
python3 -m leetcode.run_problems list --category "Dynamic Programming"

# View problem statistics
python3 -m leetcode.run_problems stats

# Show problem description and solution approach
python3 -m leetcode.run_problems show 1-two-sum

# Run unit tests across a difficulty tier
python3 -m leetcode.run_problems test easy
python3 -m leetcode.run_problems test medium
python3 -m leetcode.run_problems test hard
```

### 3. Submodule Runners
Run topic-specific or company-specific demonstrations directly:
```bash
# Easy problems
python3 -m leetcode.easy.run_examples --topic arrays
python3 -m leetcode.easy.run_examples --topic all

# Medium problems
python3 -m leetcode.medium.run_examples --topic dp
python3 -m leetcode.medium.run_examples --topic all

# Hard problems
python3 -m leetcode.hard.run_examples --topic dp_design
python3 -m leetcode.hard.run_examples --topic all

# Company-Wise tracks
python3 -m leetcode.company_wise.run_examples --company google
python3 -m leetcode.company_wise.run_examples --company meta
python3 -m leetcode.company_wise.run_examples --company amazon
python3 -m leetcode.company_wise.run_examples --company microsoft
python3 -m leetcode.company_wise.run_examples --company all
```
