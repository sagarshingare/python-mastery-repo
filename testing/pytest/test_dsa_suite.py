"""Comprehensive test suite for the Data Structures & Algorithms (DSA) module."""

from __future__ import annotations

import pytest

# Arrays
from dsa.arrays import (
    DynamicArray,
    PrefixSum,
    binary_search,
    container_with_most_water,
    linear_search,
    max_subarray_sum,
    merge_intervals,
    remove_duplicates_inplace,
    rotate_array_inplace,
    sort_colors,
    subarray_sum_equals_k,
    two_sum_sorted,
)

# Linked List
from dsa.linked_list import DoublyLinkedList, SinglyLinkedList

# Stack
from dsa.stack import MinStack, Stack, evaluate_postfix, is_balanced, next_greater_element

# Queue
from dsa.queue import CircularQueue, Deque, PriorityQueue, Queue

# Trees
from dsa.trees import (
    BinarySearchTree,
    TreeNode,
    height,
    inorder,
    invert_tree,
    is_balanced as is_tree_balanced,
    is_valid_bst,
    level_order,
    lowest_common_ancestor,
    postorder,
    preorder,
)

# Graphs
from dsa.graphs import DisjointSetUnion, Graph

# Heaps
from dsa.heaps import (
    MaxHeap,
    MinHeap,
    find_median_stream,
    heapsort,
    k_smallest_elements,
    merge_k_sorted_lists,
    top_k_elements,
)

# Strings
from dsa.strings import (
    are_anagrams,
    first_unique_char,
    is_palindrome,
    kmp_search,
    longest_common_prefix,
    longest_common_substring,
    longest_substring_without_repeats,
    reverse_words,
)

# Recursion
from dsa.recursion import (
    factorial,
    fibonacci,
    flatten_nested,
    flood_fill,
    permutations,
    power,
    power_set,
    tower_of_hanoi,
)

# Sliding Window
from dsa.sliding_window import (
    count_anagram_substrings,
    longest_substring_k_distinct,
    max_consecutive_ones,
    max_sum_subarray,
    min_window_substring,
)

# Backtracking
from dsa.backtracking import (
    generate_parentheses,
    solve_n_queens,
    solve_sudoku,
    subset_sum,
    word_search,
)

# Dynamic Programming
from dsa.dynamic_programming import (
    coin_change,
    edit_distance,
    fibonacci_memo,
    fibonacci_tabulation,
    knapsack_01,
    longest_common_subsequence,
    longest_increasing_subsequence,
)

# System Design
from dsa.system_design import BloomFilter, LFUCache, LRUCache, Trie


# ---------------------------------------------------------------------------
# 1. Arrays Tests
# ---------------------------------------------------------------------------

def test_dynamic_array_operations() -> None:
    arr: DynamicArray[int] = DynamicArray()
    assert len(arr) == 0
    for x in range(10):
        arr.append(x)
    assert len(arr) == 10
    assert arr[0] == 0
    assert arr[9] == 9
    arr[0] = 99
    assert arr[0] == 99
    assert arr.pop() == 9
    arr.insert(1, 42)
    assert arr[1] == 42
    with pytest.raises(IndexError):
        _ = arr[100]


def test_search_algorithms() -> None:
    data = [10, 20, 30, 40, 50]
    assert linear_search(data, 30) == 2
    assert linear_search(data, 99) == -1
    assert binary_search(data, 40) == 3
    assert binary_search(data, 99) == -1


def test_two_pointer_techniques() -> None:
    # two_sum_sorted
    assert two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum_sorted([1, 2, 3], 10) is None

    # container_with_most_water
    assert container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    # remove_duplicates_inplace
    nums = [1, 1, 2, 2, 3]
    length = remove_duplicates_inplace(nums)
    assert length == 3
    assert nums[:length] == [1, 2, 3]


def test_prefix_sum_and_kadane() -> None:
    # PrefixSum
    ps = PrefixSum([1, 2, 3, 4, 5])
    assert ps.query(0, 2) == 6
    assert ps.query(2, 4) == 12

    # subarray_sum_equals_k
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2
    assert subarray_sum_equals_k([1, 2, 3], 3) == 2  # [1,2] and [3]

    # Kadane's max_subarray_sum
    max_sum = max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert max_sum == 6


def test_partition_intervals_rotation() -> None:
    # Dutch National Flag
    colors = [2, 0, 2, 1, 1, 0]
    sort_colors(colors)
    assert colors == [0, 0, 1, 1, 2, 2]

    # merge_intervals
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    assert merge_intervals(intervals) == [[1, 6], [8, 10], [15, 18]]

    # rotate_array_inplace
    arr = [1, 2, 3, 4, 5, 6, 7]
    rotate_array_inplace(arr, 3)
    assert arr == [5, 6, 7, 1, 2, 3, 4]


# ---------------------------------------------------------------------------
# 2. Linked List Tests
# ---------------------------------------------------------------------------

def test_singly_linked_list_features() -> None:
    sll: SinglyLinkedList[int] = SinglyLinkedList()
    sll.append(10)
    sll.append(20)
    sll.prepend(5)
    assert sll.to_list() == [5, 10, 20]
    assert sll.middle_node() == 10
    assert sll.has_cycle() is False
    sll.reverse()
    assert sll.to_list() == [20, 10, 5]
    assert sll.find(10) is not None
    assert sll.find(99) is None


def test_doubly_linked_list_features() -> None:
    dll: DoublyLinkedList[str] = DoublyLinkedList()
    dll.append("B")
    dll.prepend("A")
    dll.append("C")
    assert dll.to_list() == ["A", "B", "C"]
    assert dll.to_list_reversed() == ["C", "B", "A"]
    assert dll.delete("B") is True
    assert dll.to_list() == ["A", "C"]


# ---------------------------------------------------------------------------
# 3. Stack Tests
# ---------------------------------------------------------------------------

def test_stack_utilities() -> None:
    st: Stack[int] = Stack()
    assert st.is_empty is True
    st.push(10)
    st.push(20)
    assert st.peek() == 20
    assert len(st) == 2
    assert st.pop() == 20

    # MinStack
    ms: MinStack[int] = MinStack()
    ms.push(3)
    ms.push(5)
    assert ms.get_min() == 3
    ms.push(2)
    assert ms.get_min() == 2
    ms.pop()
    assert ms.get_min() == 3

    # evaluate_postfix
    assert evaluate_postfix("2 3 + 4 *") == 20

    # next_greater_element
    assert next_greater_element([4, 5, 2, 10, 8]) == [5, 10, 10, -1, -1]


# ---------------------------------------------------------------------------
# 4. Queue Tests
# ---------------------------------------------------------------------------

def test_queue_structures() -> None:
    # FIFO Queue
    q: Queue[int] = Queue()
    q.enqueue(1)
    q.enqueue(2)
    assert q.peek() == 1
    assert q.dequeue() == 1

    # CircularQueue
    cq = CircularQueue(capacity=2)
    cq.enqueue(10)
    cq.enqueue(20)
    assert cq.is_full is True
    with pytest.raises(OverflowError):
        cq.enqueue(30)
    assert cq.dequeue() == 10
    cq.enqueue(30)
    assert cq.dequeue() == 20
    assert cq.dequeue() == 30

    # PriorityQueue
    pq: PriorityQueue[str] = PriorityQueue()
    pq.enqueue("low", priority=10)
    pq.enqueue("high", priority=1)
    assert pq.dequeue() == "high"

    # Deque
    dq: Deque[int] = Deque()
    dq.append_right(1)
    dq.append_left(2)
    assert dq.pop_left() == 2
    assert dq.pop_right() == 1


# ---------------------------------------------------------------------------
# 5. Trees Tests
# ---------------------------------------------------------------------------

def test_tree_algorithms() -> None:
    # BST
    bst = BinarySearchTree()
    for v in [5, 3, 7, 2, 4, 6, 8]:
        bst.insert(v)
    assert bst.inorder() == [2, 3, 4, 5, 6, 7, 8]
    assert bst.find_min() == 2
    assert bst.find_max() == 8

    # Traversals on arbitrary tree
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert preorder(root) == [1, 2, 3]
    assert inorder(root) == [2, 1, 3]
    assert postorder(root) == [2, 3, 1]
    assert level_order(root) == [[1], [2, 3]]
    assert height(root) == 1
    assert is_tree_balanced(root) is True

    # LCA
    #       4
    #      / \
    #     2   6
    #    / \
    #   1   3
    tree = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6))
    assert lowest_common_ancestor(tree, 1, 3).value == 2
    assert lowest_common_ancestor(tree, 1, 6).value == 4

    # is_valid_bst
    assert is_valid_bst(tree) is True
    invalid_tree = TreeNode(5, TreeNode(6), TreeNode(7))
    assert is_valid_bst(invalid_tree) is False

    # invert_tree
    inv = invert_tree(TreeNode(1, TreeNode(2), TreeNode(3)))
    assert inv.left.value == 3
    assert inv.right.value == 2


# ---------------------------------------------------------------------------
# 6. Graph Tests
# ---------------------------------------------------------------------------

def test_graph_and_dijkstra_dsu() -> None:
    # Directed Graph & Topo sort
    dag = Graph(directed=True)
    dag.add_edge("A", "B")
    dag.add_edge("B", "C")
    assert dag.topological_sort() == ["A", "B", "C"]
    assert dag.has_cycle() is False

    # Cycle in directed graph
    cyclic = Graph(directed=True)
    cyclic.add_edge("A", "B")
    cyclic.add_edge("B", "A")
    assert cyclic.has_cycle() is True
    with pytest.raises(ValueError):
        cyclic.topological_sort()

    # Dijkstra
    wg = Graph(directed=True)
    wg.add_edge("A", "B", weight=1.0)
    wg.add_edge("B", "C", weight=2.0)
    wg.add_edge("A", "C", weight=4.0)
    cost, path = wg.dijkstra_shortest_path("A", "C")
    assert cost == 3.0
    assert path == ["A", "B", "C"]

    # DSU
    dsu = DisjointSetUnion(["A", "B", "C", "D"])
    assert dsu.count == 4
    assert dsu.union("A", "B") is True
    assert dsu.union("B", "C") is True
    assert dsu.connected("A", "C") is True
    assert dsu.connected("A", "D") is False
    assert dsu.count == 2
    assert dsu.union("A", "C") is False  # already connected


# ---------------------------------------------------------------------------
# 7. Heaps Tests
# ---------------------------------------------------------------------------

def test_heaps_and_streaming() -> None:
    # MinHeap and MaxHeap
    min_h = MinHeap()
    for x in [5, 1, 3]:
        min_h.push(x)
    assert min_h.peek() == 1
    assert min_h.pop() == 1

    max_h = MaxHeap()
    for x in [5, 1, 8]:
        max_h.push(x)
    assert max_h.peek() == 8
    assert max_h.pop() == 8

    # heapsort
    nums = [9, 3, 1, 5, 13, 2]
    assert heapsort(nums) == [1, 2, 3, 5, 9, 13]
    assert top_k_elements(nums, 2) == [13, 9]
    assert k_smallest_elements(nums, 2) == [1, 2]

    # merge_k_sorted_lists
    assert merge_k_sorted_lists([[1, 4], [2, 5], [3, 6]]) == [1, 2, 3, 4, 5, 6]

    # find_median_stream
    assert find_median_stream([5, 15, 1, 3]) == [5.0, 10.0, 5.0, 4.0]


# ---------------------------------------------------------------------------
# 8. Strings Tests
# ---------------------------------------------------------------------------

def test_string_algorithms() -> None:
    assert is_palindrome("Racecar") is True
    assert are_anagrams("anagram", "nagaram") is True
    assert longest_common_prefix(["interspecies", "interstellar", "interstate"]) == "inters"
    assert kmp_search("AABAACAADAABAABA", "AABA") == [0, 9, 12]
    sub = longest_substring_without_repeats("pwwkew")
    assert sub == "wke"
    assert len(sub) == 3
    assert longest_common_substring("abcde", "abfde") == "ab"
    assert reverse_words("  the sky is  blue ") == "blue is sky the"
    assert first_unique_char("leetcode") == 0


# ---------------------------------------------------------------------------
# 9. Recursion Tests
# ---------------------------------------------------------------------------

def test_recursion_algorithms() -> None:
    assert factorial(5) == 120
    assert fibonacci(7) == 13
    assert power(2, 8) == 256
    assert len(power_set([1, 2, 3])) == 8
    assert len(permutations([1, 2, 3])) == 6
    assert len(tower_of_hanoi(3, "A", "C", "B")) == 7

    grid = [[1, 1], [1, 0]]
    flood_fill(grid, 0, 0, 2)
    assert grid == [[2, 2], [2, 0]]

    assert flatten_nested([1, [2, [3, 4], 5]]) == [1, 2, 3, 4, 5]


# ---------------------------------------------------------------------------
# 10. Sliding Window Tests
# ---------------------------------------------------------------------------

def test_sliding_window_algorithms() -> None:
    assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9
    assert longest_substring_k_distinct("araaci", 2) == "araa"
    assert min_window_substring("ADOBECODEBANC", "ABC") == "BANC"
    assert max_consecutive_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert count_anagram_substrings("cbaebabacd", "abc") == 2


# ---------------------------------------------------------------------------
# 11. Backtracking Tests
# ---------------------------------------------------------------------------

def test_backtracking_algorithms() -> None:
    assert len(solve_n_queens(4)) == 2
    assert len(generate_parentheses(3)) == 5
    assert subset_sum([2, 3, 6, 7], 7) == [[7]]

    grid = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert word_search(grid, "ABCCED") is True
    assert word_search(grid, "ABCB") is False


# ---------------------------------------------------------------------------
# 12. Dynamic Programming Tests
# ---------------------------------------------------------------------------

def test_dynamic_programming_algorithms() -> None:
    assert fibonacci_memo(10) == 55
    assert fibonacci_tabulation(10) == 55
    assert knapsack_01([1, 2, 3], [10, 15, 40], 6) == 65
    assert longest_common_subsequence("abcde", "ace") == "ace"
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert coin_change([1, 2, 5], 11) == 3
    assert edit_distance("kitten", "sitting") == 3


# ---------------------------------------------------------------------------
# 13. System Design Tests
# ---------------------------------------------------------------------------

def test_system_design_structures() -> None:
    # LRUCache
    lru = LRUCache(capacity=2)
    lru.put(1, 10)
    lru.put(2, 20)
    assert lru.get(1) == 10
    lru.put(3, 30)  # evicts 2
    assert lru.get(2) is None
    assert lru.get(3) == 30

    # LFUCache
    lfu = LFUCache(capacity=2)
    lfu.put(1, 10)
    lfu.put(2, 20)
    assert lfu.get(1) == 10  # freq of 1 is now 2
    lfu.put(3, 30)  # key 2 has freq 1, key 1 has freq 2 -> evicts 2
    assert lfu.get(2) is None
    assert lfu.get(3) == 30
    assert lfu.get(1) == 10

    # Trie
    trie = Trie()
    trie.insert("python")
    trie.insert("pytorch")
    assert trie.search("python") is True
    assert trie.search("py") is False
    assert trie.starts_with("py") is True
    assert trie.autocomplete("py") == ["python", "pytorch"]

    # BloomFilter
    bf = BloomFilter(expected_items=100, fp_rate=0.01)
    bf.add("data_structures")
    assert "data_structures" in bf
    assert "random_non_existent_key_123" not in bf
