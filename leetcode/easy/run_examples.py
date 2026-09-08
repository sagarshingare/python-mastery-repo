"""CLI runner for LeetCode Easy problems."""

from __future__ import annotations

import argparse
import logging

from leetcode.easy.solutions import (
    ListNode,
    TreeNode,
    problem_1_two_sum,
    problem_20_valid_parentheses,
    problem_53_maximum_subarray,
    problem_70_climbing_stairs,
    problem_121_best_time_buy_sell_stock,
    problem_125_valid_palindrome,
    problem_141_linked_list_cycle,
    problem_155_min_stack,
    problem_198_house_robber,
    problem_206_reverse_linked_list,
    problem_217_contains_duplicate,
    problem_226_invert_binary_tree,
    problem_242_valid_anagram,
    run_tests,
)

logger = logging.getLogger(__name__)


def run_arrays_hashing_examples() -> None:
    logger.info("Running Easy: Arrays & Hashing")
    nums = [2, 7, 11, 15]
    target = 9
    print(f"Two Sum ({nums}, {target}) -> {problem_1_two_sum(nums, target)}")
    print(f"Contains Duplicate [1, 2, 3, 1] -> {problem_217_contains_duplicate([1, 2, 3, 1])}")
    print(f"Valid Anagram ('anagram', 'nagaram') -> {problem_242_valid_anagram('anagram', 'nagaram')}")
    print(f"Max Subarray [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> {problem_53_maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])}")
    print(f"Best Time to Buy/Sell Stock [7, 1, 5, 3, 6, 4] -> {problem_121_best_time_buy_sell_stock([7, 1, 5, 3, 6, 4])}")


def run_strings_examples() -> None:
    logger.info("Running Easy: Strings")
    s = "A man, a plan, a canal: Panama"
    print(f"Valid Palindrome '{s}' -> {problem_125_valid_palindrome(s)}")


def run_linked_list_examples() -> None:
    logger.info("Running Easy: Linked Lists")
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    rev = problem_206_reverse_linked_list(head)
    vals = []
    curr = rev
    while curr:
        vals.append(curr.val)
        curr = curr.next
    print(f"Reversed Linked List [1,2,3,4,5] -> {vals}")
    print(f"Linked List Cycle detection (linear) -> {problem_141_linked_list_cycle(None)}")


def run_trees_examples() -> None:
    logger.info("Running Easy: Trees")
    root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
    inv = problem_226_invert_binary_tree(root)
    print(f"Inverted Tree root value: {inv.val}, left child: {inv.left.val}, right child: {inv.right.val}")


def run_dp_examples() -> None:
    logger.info("Running Easy: Dynamic Programming")
    print(f"Climbing Stairs (5 steps) -> {problem_70_climbing_stairs(5)} distinct ways")
    print(f"House Robber [2, 7, 9, 3, 1] -> max loot: {problem_198_house_robber([2, 7, 9, 3, 1])}")


def run_stack_examples() -> None:
    logger.info("Running Easy: Stack")
    print(f"Valid Parentheses '()[]{{}}' -> {problem_20_valid_parentheses('()[]{}')}")
    ms = problem_155_min_stack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    print(f"MinStack getMin() -> {ms.getMin()}")
    ms.pop()
    print(f"After pop(), top() -> {ms.top()}, getMin() -> {ms.getMin()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LeetCode Easy demonstrations")
    parser.add_argument(
        "--topic",
        choices=["arrays", "strings", "linked_list", "trees", "dp", "stack", "test", "all"],
        default="all",
        help="Topic or action to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "arrays": run_arrays_hashing_examples,
        "strings": run_strings_examples,
        "linked_list": run_linked_list_examples,
        "trees": run_trees_examples,
        "dp": run_dp_examples,
        "stack": run_stack_examples,
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
