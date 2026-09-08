"""CLI runner for LeetCode Medium problems."""

from __future__ import annotations

import argparse
import logging

from leetcode.medium.solutions import (
    ListNode,
    TreeNode,
    problem_3_longest_substring_without_repeating,
    problem_5_longest_palindromic_substring,
    problem_11_container_with_most_water,
    problem_15_three_sum,
    problem_54_spiral_matrix,
    problem_98_validate_bst,
    problem_102_binary_tree_level_order,
    problem_139_word_break,
    problem_152_maximum_product_subarray,
    problem_200_number_of_islands,
    problem_300_longest_increasing_subsequence,
    run_tests,
)

logger = logging.getLogger(__name__)


def run_arrays_two_pointers_examples() -> None:
    logger.info("Running Medium: Arrays & Two Pointers")
    nums = [-1, 0, 1, 2, -1, -4]
    print(f"3Sum ({nums}) -> {problem_15_three_sum(nums)}")

    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Container With Most Water {heights} -> max area: {problem_11_container_with_most_water(heights)}")

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    print(f"Spiral Matrix -> {problem_54_spiral_matrix(matrix)}")


def run_strings_examples() -> None:
    logger.info("Running Medium: Strings")
    s1 = "abcabcbb"
    print(f"Longest Substring Without Repeating '{s1}' -> length: {problem_3_longest_substring_without_repeating(s1)}")

    s2 = "babad"
    print(f"Longest Palindromic Substring '{s2}' -> '{problem_5_longest_palindromic_substring(s2)}'")


def run_trees_graphs_examples() -> None:
    logger.info("Running Medium: Trees & Graphs")
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(f"Binary Tree Level Order -> {problem_102_binary_tree_level_order(root)}")
    print(f"Validate BST (root) -> {problem_98_validate_bst(root)}")

    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    print(f"Number of Islands in grid -> {problem_200_number_of_islands(grid)}")


def run_dp_examples() -> None:
    logger.info("Running Medium: Dynamic Programming")
    s = "leetcode"
    word_dict = ["leet", "code"]
    print(f"Word Break ('{s}', {word_dict}) -> {problem_139_word_break(s, word_dict)}")

    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Longest Increasing Subsequence {nums} -> length: {problem_300_longest_increasing_subsequence(nums)}")

    prod_nums = [2, 3, -2, 4]
    print(f"Max Product Subarray {prod_nums} -> {problem_152_maximum_product_subarray(prod_nums)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LeetCode Medium demonstrations")
    parser.add_argument(
        "--topic",
        choices=["arrays", "strings", "trees_graphs", "dp", "test", "all"],
        default="all",
        help="Topic or action to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "arrays": run_arrays_two_pointers_examples,
        "strings": run_strings_examples,
        "trees_graphs": run_trees_graphs_examples,
        "dp": run_dp_examples,
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
