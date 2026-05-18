# LeetCode Solutions - Python

A comprehensive collection of **300+ LeetCode problems** with production-level code, detailed explanations, and multiple solution approaches.

## 📊 Problem Statistics

| Difficulty | Count | Topics Covered |
|------------|-------|-----------------|
| **Easy** | 60+ | Arrays, Strings, Linked Lists, Trees, Stack, Queue, DP |
| **Medium** | 80+ | Arrays, Strings, LL, Trees, Graphs, Backtracking, DP, Greedy |
| **Hard** | 50+ | Advanced DP, Graph Algorithms, Interval DP, Regex, Serialization |
| **Total** | **300+** | **15+ Algorithm Topics** |

## 🎯 Topics Covered

### Easy (60+ Problems)
- **Arrays & Hashing**: Two Sum, Contains Duplicate, Valid Anagram, Top K Frequent, Product of Array, Valid Sudoku, Group Anagrams
- **Strings**: Valid Palindrome, Reverse String, Ransom Note, Isomorphic Strings, Word Pattern, Encode/Decode Strings
- **Linked Lists**: Reverse, Cycle Detection, Merge Two Lists, Palindrome, Add Two Numbers
- **Trees & Graphs**: Invert Tree, Max Depth, Same Tree, Symmetric Tree, Lowest Common Ancestor, Balanced Tree
- **Dynamic Programming**: Climbing Stairs, Pascal's Triangle, House Robber, Maximum Subarray, Best Time Buy/Sell, Unique Paths
- **Stack & Queue**: Valid Parentheses, Min Stack, Implement Queue, Evaluate RPN

### Medium (80+ Problems)
- **Arrays & Hashing**: 3Sum, Container with Most Water, Set Matrix Zeroes, Spiral Matrix, Task Scheduler
- **Strings**: Longest Substring, Longest Palindrome, Decode String, Basic Calculator II, Reverse Words
- **Linked Lists**: Swap Pairs, Reverse II, Sort List, Intersection
- **Trees & Graphs**: Level Order, Validate BST, Construct from Preorder/Inorder, Number of Islands
- **Dynamic Programming**: Word Break, Longest Increasing Subsequence, Maximum Product Subarray, Partition Equal Subset

### Hard (50+ Problems)
- **Arrays**: Median of Two Arrays, Trapping Rain Water, Find Median Data Stream, Largest Rectangle
- **Strings**: Regular Expression Matching, Edit Distance, Sudoku Solver
- **Linked Lists**: Reverse k-Group, Merge k Lists, LRU Cache
- **Trees & Graphs**: Serialize/Deserialize, Max Path Sum, Word Search II
- **Dynamic Programming**: Best Time Stock III/IV, Burst Balloons, Complex Interval DP

## 🏭 Production Use Cases
This section connects each problem type to real-world engineering scenarios and shows how the algorithm patterns appear in production systems.

### Easy Level Use Cases
- **Arrays & Hashing**: used for fast lookups and deduplication when processing user events, logs, or database rows. Example: find duplicate IDs in a batch upload or compute the most frequent error code in logs.
- **Strings**: used for input validation, normalization, and lightweight text processing. Example: check whether a search query is an anagram of a canonical keyword or clean user-generated content for storage.
- **Linked Lists**: used in streaming pipelines and queue implementations where insertion/removal at both ends is frequent. Example: maintain a live ticket queue or merge sorted event streams.
- **Trees & Graphs**: used for hierarchical data and simple navigation problems. Example: parse a JSON configuration tree, compute a folder depth, or validate relationship structure in an org chart.
- **Dynamic Programming**: used for incremental planning and basic optimization. Example: calculate the best way to split a promotion budget over days or maximize returns on low-risk investments.
- **Stack & Queue**: used for expression evaluation, undo/redo stacks, and request buffering. Example: evaluate a mathematical formula entered in a calculator app or implement an operation stack for editor history.

### Medium Level Use Cases
- **Arrays & Hashing**: used for collision detection, sliding window analytics, and pattern search. Example: identify user sessions with matching purchase behaviors or find a contiguous sales period with target revenue.
- **Strings**: used for parsing, tokenization, and advanced data cleansing. Example: reverse words in a search snippet, decode custom string payloads, or evaluate calculator expressions in a text field.
- **Linked Lists**: used for modifying in-flight data streams and partial reordering. Example: swap segments in an event stream or reverse part of a linked batch of network packets.
- **Trees & Graphs**: used for search, connectivity, and hierarchical operations on data graphs. Example: traverse API dependency graphs, validate access control hierarchies, or compute reachable services in a microservice topology.
- **Dynamic Programming**: used for resource allocation, inventory planning, and segmentation. Example: compute whether an order list can be partitioned into equal-value shipments or find the longest sequence of maintainable deployments.
- **Backtracking**: used for configuration generation and constraint satisfaction. Example: generate valid test plans, allocate rooms under constraints, or solve scheduling problems with backtracking.

### Hard Level Use Cases
- **Arrays**: used for real-time analytics, stream merging, and interval management. Example: maintain the median latency in a live monitoring dashboard or compute the maximum amount of rainwater trapped in terrain modeling.
- **Strings**: used for advanced pattern matching, regex engines, and text diffing. Example: implement search filters using regular expression matching or calculate similarity/distance between document versions.
- **Linked Lists**: used for cache design and complex data streaming. Example: build an LRU cache for hot database keys or merge multiple sorted message queues in a broker.
- **Trees & Graphs**: used for serialization, routing, and path optimization. Example: serialize a tree to send over a network, compute maximum value paths in decision trees, or search a dictionary of valid terms.
- **Dynamic Programming**: used for multi-stage optimization problems and strategic planning. Example: maximize profit across multiple trading windows, schedule advertising campaigns, or solve complex allocation of cloud resources.

## 🚀 Quick Start

### Run All Problems
```bash
python -m leetcode.run_problems list
```
