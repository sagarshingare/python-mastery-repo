"""CLI runner for LeetCode Hard problems."""

from __future__ import annotations

import argparse
import logging

from leetcode.hard.solutions import (
    ListNode,
    TreeNode,
    problem_4_median_two_sorted_arrays,
    problem_10_regular_expression_matching,
    problem_23_merge_k_sorted_lists,
    problem_25_reverse_nodes_k_group,
    problem_42_trapping_rain_water,
    problem_72_edit_distance,
    problem_84_largest_rectangle_histogram,
    problem_123_best_time_buy_sell_stock_iii,
    problem_124_binary_tree_max_path_sum,
    problem_146_lru_cache,
    problem_212_word_search_ii,
    problem_295_find_median_data_stream,
    problem_312_burst_balloons,
    run_tests,
)

logger = logging.getLogger(__name__)


def run_arrays_binary_search_examples() -> None:
    logger.info("Running Hard: Arrays & Binary Search")
    nums1, nums2 = [1, 3], [2]
    print(f"Median of Two Sorted Arrays ({nums1}, {nums2}) -> {problem_4_median_two_sorted_arrays(nums1, nums2)}")

    heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Trapping Rain Water {heights} -> {problem_42_trapping_rain_water(heights)} units")

    hist = [2, 1, 5, 6, 2, 3]
    print(f"Largest Rectangle in Histogram {hist} -> max area: {problem_84_largest_rectangle_histogram(hist)}")


def run_strings_backtracking_examples() -> None:
    logger.info("Running Hard: Strings & Backtracking")
    s, p = "aa", "a*"
    print(f"Regex Matching ('{s}', '{p}') -> {problem_10_regular_expression_matching(s, p)}")

    w1, w2 = "horse", "ros"
    print(f"Edit Distance ('{w1}', '{w2}') -> {problem_72_edit_distance(w1, w2)} operations")

    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    words = ["oath", "pea", "eat", "rain"]
    print(f"Word Search II -> found words: {problem_212_word_search_ii(board, words)}")


def run_lists_trees_examples() -> None:
    logger.info("Running Hard: Linked Lists & Trees")
    # Tree max path sum
    root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(f"Binary Tree Max Path Sum -> {problem_124_binary_tree_max_path_sum(root)}")

    # Merge k sorted lists
    l1 = ListNode(1, ListNode(4, ListNode(5)))
    l2 = ListNode(1, ListNode(3, ListNode(4)))
    l3 = ListNode(2, ListNode(6))
    merged = problem_23_merge_k_sorted_lists([l1, l2, l3])
    vals = []
    curr = merged
    while curr:
        vals.append(curr.val)
        curr = curr.next
    print(f"Merge 3 Sorted Lists -> {vals}")

    # Reverse in k-group
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    rev_k = problem_25_reverse_nodes_k_group(head, 2)
    k_vals = []
    curr = rev_k
    while curr:
        k_vals.append(curr.val)
        curr = curr.next
    print(f"Reverse Nodes in k=2 group -> {k_vals}")


def run_dp_design_examples() -> None:
    logger.info("Running Hard: Advanced DP & Data Structure Design")
    prices = [3, 3, 5, 0, 0, 3, 1, 4]
    print(f"Best Time to Buy/Sell Stock III {prices} -> max profit: {problem_123_best_time_buy_sell_stock_iii(prices)}")

    balloons = [3, 1, 5, 8]
    print(f"Burst Balloons {balloons} -> max coins: {problem_312_burst_balloons(balloons)}")

    # MedianFinder
    mf = problem_295_find_median_data_stream()
    mf.addNum(1)
    mf.addNum(2)
    print(f"MedianFinder after adding [1, 2] -> median: {mf.findMedian()}")
    mf.addNum(3)
    print(f"MedianFinder after adding 3 -> median: {mf.findMedian()}")

    # LRU Cache
    lru_cls = problem_146_lru_cache()
    cache = lru_cls(2)
    cache.put(1, 1)
    cache.put(2, 2)
    g1 = cache.get(1)
    cache.put(3, 3)
    g2 = cache.get(2)
    print(f"LRU Cache capacity=2 -> get(1): {g1}, get(2) (evicted): {g2}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LeetCode Hard demonstrations")
    parser.add_argument(
        "--topic",
        choices=["arrays", "strings", "lists_trees", "dp_design", "test", "all"],
        default="all",
        help="Topic or action to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "arrays": run_arrays_binary_search_examples,
        "strings": run_strings_backtracking_examples,
        "lists_trees": run_lists_trees_examples,
        "dp_design": run_dp_design_examples,
    }

    if args.topic == "test":
        run_tests()
    elif args.topic == "all":
        for fn in dispatch.values():
            fn()
        print("\n--- Running Built-in Quick Validation ---")
        run_tests()
    else:
        dispatch[args.topic]()


if __name__ == "__main__":
    main()
