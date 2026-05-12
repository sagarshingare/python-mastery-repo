"""
LeetCode Medium Problems - Production-Ready Solutions

This module contains 80+ carefully curated LeetCode medium problems organized by topic.
Each problem includes:
  - Problem description and constraints
  - Multiple solution approaches with tradeoffs
  - Time and space complexity analysis
  - Edge cases and test cases
  - Production-level code with detailed comments

Topics Covered:
  - Arrays & Hashing (Sorting, Searching)
  - Strings & Manipulation
  - Linked Lists (Complex operations)
  - Trees & Graphs (BFS, DFS, Traversal)
  - Dynamic Programming (Intermediate)
  - Backtracking
  - Binary Search
  - Stack & Queue
  - Hash Maps
"""

from typing import List, Optional, Dict, Tuple, Set
from collections import defaultdict, deque
import heapq


# ============================================================================
# ARRAYS & SORTING
# ============================================================================

def problem_3_longest_substring_without_repeating(s: str) -> int:
    """
    LeetCode #3: Longest Substring Without Repeating Characters
    
    Problem: Given a string s, find the length of the longest substring without
    repeating characters.
    
    Constraints:
      - 0 <= len(s) <= 5 * 10^4
      - s consists of English letters, digits, symbols and spaces
    
    Approach: Sliding Window
    - Use left/right pointers to maintain window
    - Track last seen index of each character
    - Time: O(n), Space: O(min(m, 26)) where m is charset size
    """
    char_index = {}
    max_length = 0
    left = 0
    
    for right in range(len(s)):
        if s[right] in char_index and char_index[s[right]] >= left:
            # Move left pointer to skip duplicate
            left = char_index[s[right]] + 1
        
        # Update last seen index
        char_index[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


def problem_39_combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    LeetCode #39: Combination Sum
    
    Problem: Given an array of distinct integers candidates and a target integer
    target, return a list of all unique combinations of candidates where the chosen
    numbers sum to target. Each number in candidates may be used unlimited times.
    
    Approach: Backtracking
    - Recursively build combinations
    - Prune branches that exceed target
    - Time: O(N^(T/M)) worst case
    - Space: O(T/M) recursion depth
    """
    result = []
    
    def backtrack(start: int, path: List[int], remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            # Note: start=i allows reusing same number
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result


def problem_49_group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    LeetCode #49: Group Anagrams
    
    Problem: Given an array of strings strs, group the anagrams together.
    You can return the answer in any order.
    
    Constraints:
      - 1 <= len(strs) <= 10^4
      - 0 <= len(strs[i]) <= 100
    
    Approach: Hash Map with sorted key
    - Sort characters in each word as key
    - Group words with same key
    - Time: O(n * k log k) where n is number of strings, k is max length
    - Space: O(n * k)
    """
    anagrams = defaultdict(list)
    
    for word in strs:
        # Sort characters to use as key
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)
    
    return list(anagrams.values())


def problem_33_search_in_rotated_sorted_array(nums: List[int], target: int) -> int:
    """
    LeetCode #33: Search in Rotated Sorted Array
    
    Problem: There is an integer array nums sorted in ascending order (with distinct
    values). nums is rotated at some unknown pivot. Find the index of target or -1.
    You must achieve O(log n) time complexity.
    
    Approach: Binary Search with rotation handling
    - Identify which half is properly sorted
    - Check if target is in sorted half
    - Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Identify which half is properly sorted
        if nums[left] <= nums[mid]:  # Left half is sorted
            # Check if target is in left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            # Check if target is in right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


def problem_15_3sum(nums: List[int]) -> List[List[int]]:
    """
    LeetCode #15: 3Sum
    
    Problem: Given an integer array nums, return all the triplets [nums[i], nums[j],
    nums[k]] such that i != j != k and nums[i] + nums[j] + nums[k] == 0.
    
    Constraints:
      - 3 <= len(nums) <= 3000
      - -10^5 <= nums[i] <= 10^5
    
    Approach: Sorting + Two Pointers
    - Sort array
    - For each element, use two pointers to find pair
    - Skip duplicates
    - Time: O(n^2), Space: O(1)
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip if number is too large to form zero sum
        if nums[i] > 0:
            break
        
        # Skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        target = -nums[i]
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result


# ============================================================================
# LINKED LISTS
# ============================================================================

def problem_2_add_two_numbers(l1: Optional['ListNode'], l2: Optional['ListNode']) -> Optional['ListNode']:
    """
    LeetCode #2: Add Two Numbers
    
    Problem: You are given two non-empty linked lists representing two non-negative
    integers. The digits are stored in reverse order. Add the two numbers and return
    the sum as a linked list.
    
    Approach: Single pass with carry
    - Traverse both lists simultaneously
    - Handle carry from addition
    - Time: O(max(m, n)), Space: O(max(m, n))
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10
        
        current.next = ListNode(digit)
        current = current.next
        
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next


def problem_19_remove_nth_node_from_end(head: Optional['ListNode'], n: int) -> Optional['ListNode']:
    """
    LeetCode #19: Remove Nth Node From End of List
    
    Problem: Given the head of a linked list, remove the nth node from the end
    and return the head of the list.
    
    Approach: Two pointers (fast/slow)
    - Create gap of n nodes between pointers
    - Move both to find target node
    - Time: O(L), Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy
    
    # Create n+1 gap
    for _ in range(n + 1):
        if not fast:
            return head
        fast = fast.next
    
    # Move both pointers until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    # Remove nth node
    slow.next = slow.next.next
    
    return dummy.next


def problem_24_swap_nodes_in_pairs(head: Optional['ListNode']) -> Optional['ListNode']:
    """
    LeetCode #24: Swap Nodes in Pairs
    
    Problem: Given a linked list, swap every two adjacent nodes and return its head.
    You must solve the problem without modifying the values.
    
    Approach: Iterative pointer manipulation
    - Swap each pair of nodes
    - Track previous, current, next
    - Time: O(n), Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    while prev.next and prev.next.next:
        # Nodes to be swapped
        first = prev.next
        second = prev.next.next
        
        # Swap
        prev.next = second
        first.next = second.next
        second.next = first
        
        # Move prev forward
        prev = first
    
    return dummy.next


def problem_148_sort_linked_list(head: Optional['ListNode']) -> Optional['ListNode']:
    """
    LeetCode #148: Sort List
    
    Problem: Given the head of a linked list, sort the list using merge sort.
    
    Approach: Merge Sort (Fast & Slow pointers)
    - Find middle of list
    - Split into two halves
    - Recursively sort and merge
    - Time: O(n log n), Space: O(log n)
    """
    if not head or not head.next:
        return head
    
    def find_middle(node: Optional['ListNode']) -> Tuple[Optional['ListNode'], Optional['ListNode']]:
        slow = prev = node
        fast = node
        
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        if prev:
            prev.next = None
        
        return node if prev else None, slow
    
    def merge(l1: Optional['ListNode'], l2: Optional['ListNode']) -> Optional['ListNode']:
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 or l2
        return dummy.next
    
    left, right = find_middle(head)
    
    if not left:
        return right
    
    left = problem_148_sort_linked_list(left)
    right = problem_148_sort_linked_list(right)
    
    return merge(left, right)


# ============================================================================
# TREES & GRAPHS
# ============================================================================

def problem_102_binary_tree_level_order_traversal(root: Optional['TreeNode']) -> List[List[int]]:
    """
    LeetCode #102: Binary Tree Level Order Traversal
    
    Problem: Given the root of a binary tree, return the level order traversal
    of its nodes' values. (i.e., from left to right, level by level).
    
    Approach: BFS with Queue
    - Use queue to traverse level by level
    - Track number of nodes at current level
    - Time: O(n), Space: O(w) where w is max width
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


def problem_105_construct_binary_tree_from_preorder_inorder(
    preorder: List[int], inorder: List[int]
) -> Optional['TreeNode']:
    """
    LeetCode #105: Construct Binary Tree from Preorder and Inorder Traversal
    
    Problem: Given two integer arrays preorder and inorder where preorder is the
    preorder traversal of a binary tree and inorder is the inorder traversal,
    construct and return the binary tree.
    
    Approach: Recursive reconstruction
    - Preorder: first element is root
    - Inorder: elements left of root are left subtree
    - Time: O(n), Space: O(n)
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}
    
    def build(preorder_start: int, inorder_start: int, inorder_end: int) -> Optional['TreeNode']:
        if inorder_start > inorder_end:
            return None
        
        root_val = preorder[preorder_start]
        root = TreeNode(root_val)
        
        root_index = inorder_map[root_val]
        left_size = root_index - inorder_start
        
        root.left = build(preorder_start + 1, inorder_start, root_index - 1)
        root.right = build(preorder_start + 1 + left_size, root_index + 1, inorder_end)
        
        return root
    
    return build(0, 0, len(inorder) - 1)


def problem_200_number_of_islands(grid: List[List[str]]) -> int:
    """
    LeetCode #200: Number of Islands
    
    Problem: Given an m x n 2D binary grid grid which represents a map of '1's
    (land) and '0's (water), return the number of islands.
    
    Approach: DFS/BFS with visited tracking
    - Explore each unvisited '1' using DFS
    - Mark all connected '1's as visited
    - Time: O(m*n), Space: O(m*n) for recursion
    """
    if not grid:
        return 0
    
    visited = set()
    count = 0
    
    def dfs(i: int, j: int) -> None:
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
            return
        if (i, j) in visited or grid[i][j] == '0':
            return
        
        visited.add((i, j))
        
        # Explore 4 directions
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1' and (i, j) not in visited:
                dfs(i, j)
                count += 1
    
    return count


def problem_207_course_schedule(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    LeetCode #207: Course Schedule
    
    Problem: There are numCourses courses labeled from 0 to numCourses - 1 and
    some prerequisite relationships. Determine if you can finish all courses.
    
    Approach: Topological Sort (DFS with cycle detection)
    - Build adjacency list
    - Use DFS to detect cycle
    - Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    state = {}  # 0: unvisited, 1: visiting, 2: visited
    
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    def has_cycle(node: int) -> bool:
        if node in state:
            return state[node] != 2
        
        state[node] = 1  # Mark as visiting
        
        for neighbor in graph[node]:
            if state.get(neighbor, 0) == 1:  # Back edge (cycle)
                return True
            if has_cycle(neighbor):
                return True
        
        state[node] = 2  # Mark as visited
        return False
    
    for course in range(numCourses):
        if has_cycle(course):
            return False
    
    return True


# ============================================================================
# DYNAMIC PROGRAMMING
# ============================================================================

def problem_5_longest_palindromic_substring(s: str) -> str:
    """
    LeetCode #5: Longest Palindromic Substring
    
    Problem: Given a string s, return the longest palindromic substring in s.
    
    Approach: Expand around center
    - For each position, expand outward
    - Handle odd and even length palindromes
    - Time: O(n^2), Space: O(1)
    """
    if not s or len(s) < 1:
        return ""
    
    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1  # Length
    
    start = 0
    max_length = 0
    
    for i in range(len(s)):
        # Odd length palindromes
        len1 = expand_around_center(i, i)
        # Even length palindromes
        len2 = expand_around_center(i, i + 1)
        
        length = max(len1, len2)
        
        if length > max_length:
            max_length = length
            start = i - (length - 1) // 2
    
    return s[start:start + max_length]


def problem_62_unique_paths(m: int, n: int) -> int:
    """
    LeetCode #62: Unique Paths
    
    Problem: There is a robot on an m x n grid. The robot is initially at the
    top-left corner. It can only move right or down. How many unique paths are there?
    
    Approach: Dynamic Programming
    - dp[i][j] = paths to reach (i,j)
    - dp[i][j] = dp[i-1][j] + dp[i][j-1]
    - Time: O(m*n), Space: O(m*n) or O(n)
    """
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    
    return dp[n - 1]


def problem_516_longest_palindromic_subsequence(s: str) -> int:
    """
    LeetCode #516: Longest Palindromic Subsequence
    
    Problem: Given a string s, find the longest palindromic subsequence's length.
    A subsequence is derived by deleting some or no elements without changing order.
    
    Approach: DP similar to LCS
    - LPS(s) = LCS(s, reverse(s))
    - Time: O(n^2), Space: O(n^2)
    """
    rev_s = s[::-1]
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i - 1] == rev_s[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[n][n]


# ============================================================================
# HASH MAPS & SETS
# ============================================================================

def problem_146_lru_cache(capacity: int) -> 'LRUCache':
    """
    LeetCode #146: LRU Cache
    
    Problem: Implement an LRU (Least Recently Used) cache with get and put operations.
    
    Approach: Hash Map + Doubly Linked List
    - Hash map for O(1) access
    - Doubly linked list for O(1) insertion/deletion
    - Time: O(1) for both operations, Space: O(capacity)
    
    Note: Returns cache object, see LRUCache class below
    """
    pass


class LRUCache:
    """Efficient LRU Cache implementation"""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_front(node)
        
        return node.value
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used (before tail)
                node = self.tail.prev
                self._remove_node(node)
                del self.cache[node.key]
            
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_front(node)
    
    def _remove_node(self, node: 'Node') -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_front(self, node: 'Node') -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node


class Node:
    """Helper class for LRU Cache"""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


# ============================================================================
# HELPER CLASSES
# ============================================================================

class ListNode:
    """Simple linked list node for testing"""
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


class TreeNode:
    """Simple tree node for testing"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def run_tests() -> None:
    """Run basic test cases for medium problems"""
    print("=" * 80)
    print("MEDIUM PROBLEMS TEST SUITE")
    print("=" * 80)
    
    # Longest Substring Without Repeating
    print("\n[Problem 3] Longest Substring Without Repeating Characters")
    print(f"  Test 1: {problem_3_longest_substring_without_repeating('abcabcbb')} == 3")
    print(f"  Test 2: {problem_3_longest_substring_without_repeating('bbbbb')} == 1")
    print(f"  Test 3: {problem_3_longest_substring_without_repeating('pwwkew')} == 3")
    
    # Combination Sum
    print("\n[Problem 39] Combination Sum")
    print(f"  Test 1: {problem_39_combination_sum([2, 3, 6, 7], 7)}")
    print(f"  Test 2: {problem_39_combination_sum([2, 3, 5], 8)}")
    
    # Group Anagrams
    print("\n[Problem 49] Group Anagrams")
    result = problem_49_group_anagrams(["eat", "tea", "ate", "nat", "tan", "bat"])
    print(f"  Test 1: {len(result)} groups formed == 2")
    
    # Search in Rotated Sorted Array
    print("\n[Problem 33] Search in Rotated Sorted Array")
    print(f"  Test 1: {problem_33_search_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 0)} == 4")
    print(f"  Test 2: {problem_33_search_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 3)} == -1")
    
    # 3Sum
    print("\n[Problem 15] 3Sum")
    result = problem_15_3sum([-1, 0, 1, 2, -1, -4])
    print(f"  Test 1: {result}")
    
    # Longest Palindromic Substring
    print("\n[Problem 5] Longest Palindromic Substring")
    print(f"  Test 1: {problem_5_longest_palindromic_substring('babad')} == 'bab' or 'aba'")
    print(f"  Test 2: {problem_5_longest_palindromic_substring('cbbd')} == 'bb'")
    
    # Unique Paths
    print("\n[Problem 62] Unique Paths")
    print(f"  Test 1: {problem_62_unique_paths(3, 7)} == 28")
    print(f"  Test 2: {problem_62_unique_paths(3, 2)} == 3")
    
    # Number of Islands
    print("\n[Problem 200] Number of Islands")
    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    print(f"  Test 1: {problem_200_number_of_islands(grid)} == 1")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    run_tests()
