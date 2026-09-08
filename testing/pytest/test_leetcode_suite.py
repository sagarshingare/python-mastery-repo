"""Comprehensive test suite for LeetCode problem solutions and company tracks."""

from __future__ import annotations

import pytest

# Easy solutions
from leetcode.easy import (
    ListNode as EasyListNode,
    TreeNode as EasyTreeNode,
    problem_1_two_sum,
    problem_20_valid_parentheses,
    problem_53_maximum_subarray,
    problem_70_climbing_stairs,
    problem_121_best_time_buy_sell_stock,
    problem_206_reverse_linked_list,
    problem_217_contains_duplicate,
    problem_226_invert_binary_tree,
    problem_242_valid_anagram,
)

# Medium solutions
from leetcode.medium import (
    ListNode as MedListNode,
    TreeNode as MedTreeNode,
    problem_3_longest_substring_without_repeating,
    problem_5_longest_palindromic_substring,
    problem_11_container_with_most_water,
    problem_15_three_sum,
    problem_54_spiral_matrix,
    problem_139_word_break,
    problem_152_maximum_product_subarray,
    problem_200_number_of_islands,
    problem_300_longest_increasing_subsequence,
)

# Hard solutions
from leetcode.hard import (
    ListNode as HardListNode,
    TreeNode as HardTreeNode,
    problem_4_median_two_sorted_arrays,
    problem_10_regular_expression_matching,
    problem_42_trapping_rain_water,
    problem_72_edit_distance,
    problem_84_largest_rectangle_histogram,
    problem_146_lru_cache,
    problem_295_find_median_data_stream,
    problem_312_burst_balloons,
)

# Company-Wise tracks
from leetcode.company_wise.google import (
    LoggerRateLimiter,
    eval_rpn,
    find_words,
    total_fruit,
)
from leetcode.company_wise.meta import (
    TreeNode as MetaTreeNode,
    min_remove_to_make_valid,
    subarray_sum,
    valid_palindrome_ii,
    vertical_order,
)
from leetcode.company_wise.amazon import (
    critical_connections,
    k_closest_points,
    oranges_rotting,
    reorder_log_files,
)
from leetcode.company_wise.microsoft import (
    ListNode as MsListNode,
    generate_matrix,
    reverse_k_group,
    reverse_words,
    sign_of_product,
)


# ============================================================================
# EASY PROBLEMS TESTS
# ============================================================================

def test_easy_arrays_and_hashing() -> None:
    assert problem_1_two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert problem_1_two_sum([3, 2, 4], 6) == [1, 2]
    assert problem_217_contains_duplicate([1, 2, 3, 1]) is True
    assert problem_217_contains_duplicate([1, 2, 3, 4]) is False
    assert problem_242_valid_anagram("anagram", "nagaram") is True
    assert problem_242_valid_anagram("rat", "car") is False


def test_easy_dp_and_stack() -> None:
    assert problem_53_maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert problem_121_best_time_buy_sell_stock([7, 1, 5, 3, 6, 4]) == 5
    assert problem_121_best_time_buy_sell_stock([7, 6, 4, 3, 1]) == 0
    assert problem_70_climbing_stairs(2) == 2
    assert problem_70_climbing_stairs(3) == 3
    assert problem_20_valid_parentheses("()[]{}") is True
    assert problem_20_valid_parentheses("(]") is False


def test_easy_linked_list_and_trees() -> None:
    # Reverse Linked List
    head = EasyListNode(1, EasyListNode(2, EasyListNode(3)))
    rev = problem_206_reverse_linked_list(head)
    assert rev is not None and rev.val == 3
    assert rev.next is not None and rev.next.val == 2

    # Invert Binary Tree
    root = EasyTreeNode(4, EasyTreeNode(2), EasyTreeNode(7))
    inverted = problem_226_invert_binary_tree(root)
    assert inverted is not None
    assert inverted.left.val == 7
    assert inverted.right.val == 2


# ============================================================================
# MEDIUM PROBLEMS TESTS
# ============================================================================

def test_medium_arrays_and_two_pointers() -> None:
    res = problem_15_three_sum([-1, 0, 1, 2, -1, -4])
    assert [-1, -1, 2] in res and [-1, 0, 1] in res
    assert problem_11_container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert problem_54_spiral_matrix(matrix) == [1, 2, 3, 6, 9, 8, 7, 4, 5]


def test_medium_strings_and_graphs() -> None:
    assert problem_3_longest_substring_without_repeating("abcabcbb") == 3
    assert problem_3_longest_substring_without_repeating("bbbbb") == 1
    assert problem_5_longest_palindromic_substring("babad") in ("bab", "aba")
    
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert problem_200_number_of_islands(grid) == 3


def test_medium_dynamic_programming() -> None:
    assert problem_139_word_break("leetcode", ["leet", "code"]) is True
    assert problem_139_word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert problem_300_longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert problem_152_maximum_product_subarray([2, 3, -2, 4]) == 6


# ============================================================================
# HARD PROBLEMS TESTS
# ============================================================================

def test_hard_arrays_and_stacks() -> None:
    assert problem_4_median_two_sorted_arrays([1, 3], [2]) == 2.0
    assert problem_4_median_two_sorted_arrays([1, 2], [3, 4]) == 2.5
    assert problem_42_trapping_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert problem_84_largest_rectangle_histogram([2, 1, 5, 6, 2, 3]) == 10


def test_hard_strings_and_dp() -> None:
    assert problem_10_regular_expression_matching("aa", "a*") is True
    assert problem_10_regular_expression_matching("ab", ".*") is True
    assert problem_10_regular_expression_matching("mississippi", "mis*is*p*.") is False
    assert problem_72_edit_distance("horse", "ros") == 3
    assert problem_312_burst_balloons([3, 1, 5, 8]) == 167


def test_hard_design_data_structures() -> None:
    # LRUCache
    lru_cls = problem_146_lru_cache()
    cache = lru_cls(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(3) == 3

    # MedianFinder
    mf = problem_295_find_median_data_stream()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0


# ============================================================================
# COMPANY-WISE TRACKS TESTS
# ============================================================================

def test_company_google_track() -> None:
    limiter = LoggerRateLimiter()
    assert limiter.should_print_message(1, "foo") is True
    assert limiter.should_print_message(2, "bar") is True
    assert limiter.should_print_message(3, "foo") is False
    assert limiter.should_print_message(11, "foo") is True

    assert total_fruit([1, 2, 1]) == 3
    assert total_fruit([0, 1, 2, 2]) == 3
    assert total_fruit([1, 2, 3, 2, 2]) == 4

    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    found = find_words(board, ["oath", "pea", "eat", "rain"])
    assert sorted(found) == ["eat", "oath"]

    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6


def test_company_meta_track() -> None:
    assert valid_palindrome_ii("aba") is True
    assert valid_palindrome_ii("abca") is True
    assert valid_palindrome_ii("abc") is False

    assert min_remove_to_make_valid("lee(t(c)o)de)") in (
        "lee(t(c)o)de",
        "lee(t(co)de)",
        "lee(t(c)ode)",
    )
    assert min_remove_to_make_valid("a)b(c)d") == "ab(c)d"
    assert min_remove_to_make_valid("))((") == ""

    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2

    # Vertical order traversal
    root = MetaTreeNode(3, MetaTreeNode(9), MetaTreeNode(20, MetaTreeNode(15), MetaTreeNode(7)))
    assert vertical_order(root) == [[9], [3, 15], [20], [7]]


def test_company_amazon_track() -> None:
    logs = ["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"]
    expected = [
        "let1 art can",
        "let3 art zero",
        "let2 own kit dig",
        "dig1 8 1 5 1",
        "dig2 3 6",
    ]
    assert reorder_log_files(logs) == expected

    grid1 = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    assert oranges_rotting(grid1) == 4
    grid2 = [[0, 2]]
    assert oranges_rotting(grid2) == 0

    points = [[1, 3], [-2, 2]]
    closest = k_closest_points(points, 1)
    assert closest == [[-2, 2]]

    n = 4
    connections = [[0, 1], [1, 2], [2, 0], [1, 3]]
    assert critical_connections(n, connections) == [[1, 3]]


def test_company_microsoft_track() -> None:
    assert generate_matrix(3) == [
        [1, 2, 3],
        [8, 9, 4],
        [7, 6, 5],
    ]
    assert generate_matrix(1) == [[1]]

    assert sign_of_product([-1, -2, -3, -4, 3, 2, 1]) == 1
    assert sign_of_product([1, 5, 0, 2, -3]) == 0
    assert sign_of_product([-1, 1, -1, 1, -1]) == -1

    assert reverse_words("the sky is blue") == "blue is sky the"
    assert reverse_words("  hello world  ") == "world hello"

    head = MsListNode(1, MsListNode(2, MsListNode(3, MsListNode(4, MsListNode(5)))))
    rev = reverse_k_group(head, 2)
    vals = []
    curr = rev
    while curr:
        vals.append(curr.val)
        curr = curr.next
    assert vals == [2, 1, 4, 3, 5]
