"""CLI runner for company-wise curated problem tracks."""

from __future__ import annotations

import argparse
import logging

from leetcode.company_wise.amazon import (
    critical_connections,
    k_closest_points,
    oranges_rotting,
    reorder_log_files,
)
from leetcode.company_wise.google import (
    LoggerRateLimiter,
    eval_rpn,
    find_words,
    total_fruit,
)
from leetcode.company_wise.meta import (
    TreeNode,
    min_remove_to_make_valid,
    subarray_sum,
    valid_palindrome_ii,
    vertical_order,
)
from leetcode.company_wise.microsoft import (
    ListNode,
    generate_matrix,
    reverse_k_group,
    reverse_words,
    sign_of_product,
)

logger = logging.getLogger(__name__)


def run_google_track() -> None:
    logger.info("Running Google Interview Track")
    # 1. Logger Rate Limiter
    logger_limiter = LoggerRateLimiter()
    print(f"Logger t=1 'foo': {logger_limiter.should_print_message(1, 'foo')}")
    print(f"Logger t=2 'bar': {logger_limiter.should_print_message(2, 'bar')}")
    print(f"Logger t=3 'foo' (within 10s): {logger_limiter.should_print_message(3, 'foo')}")
    print(f"Logger t=11 'foo' (after 10s): {logger_limiter.should_print_message(11, 'foo')}")

    # 2. Fruit into baskets
    fruits = [1, 2, 3, 2, 2]
    print(f"total_fruit({fruits}) -> {total_fruit(fruits)}")

    # 3. Word Search II
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    words = ["oath", "pea", "eat", "rain"]
    print(f"find_words on board for {words} -> {find_words(board, words)}")

    # 4. Eval RPN
    tokens = ["2", "1", "+", "3", "*"]
    print(f"eval_rpn({tokens}) -> {eval_rpn(tokens)}")


def run_meta_track() -> None:
    logger.info("Running Meta (Facebook) Interview Track")
    # 1. Valid Palindrome II
    print(f"valid_palindrome_ii('aba') -> {valid_palindrome_ii('aba')}")
    print(f"valid_palindrome_ii('abca') -> {valid_palindrome_ii('abca')}")
    print(f"valid_palindrome_ii('abc') -> {valid_palindrome_ii('abc')}")

    # 2. Min Remove to Make Valid
    expr = "lee(t(c)o)de)"
    print(f"min_remove_to_make_valid('{expr}') -> '{min_remove_to_make_valid(expr)}'")

    # 3. Subarray sum equals k
    nums = [1, 2, 3]
    print(f"subarray_sum({nums}, k=3) -> {subarray_sum(nums, 3)}")

    # 4. Vertical Order Traversal
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(f"vertical_order(root) -> {vertical_order(root)}")


def run_amazon_track() -> None:
    logger.info("Running Amazon Interview Track")
    # 1. Reorder Log Files
    logs = [
        "dig1 8 1 5 1",
        "let1 art can",
        "dig2 3 6",
        "let2 own kit dig",
        "let3 art zero",
    ]
    print(f"reorder_log_files -> {reorder_log_files(logs)}")

    # 2. Rotting Oranges
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    print(f"oranges_rotting(grid) -> {oranges_rotting(grid)} minutes")

    # 3. K Closest Points
    pts = [[1, 3], [-2, 2]]
    print(f"k_closest_points({pts}, k=1) -> {k_closest_points(pts, 1)}")

    # 4. Critical Connections
    conns = [[0, 1], [1, 2], [2, 0], [1, 3]]
    print(f"critical_connections(n=4) -> {critical_connections(4, conns)}")


def run_microsoft_track() -> None:
    logger.info("Running Microsoft Interview Track")
    # 1. Spiral Matrix II
    print(f"generate_matrix(3) ->")
    for row in generate_matrix(3):
        print(f"  {row}")

    # 2. Sign of Product
    nums = [-1, -2, -3, -4, 3, 2, 1]
    print(f"sign_of_product({nums}) -> {sign_of_product(nums)}")

    # 3. Reverse Words
    text = "  the sky   is blue  "
    print(f"reverse_words('{text}') -> '{reverse_words(text)}'")

    # 4. Reverse Nodes in k-Group
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    rev_k = reverse_k_group(head, 2)
    vals = []
    curr = rev_k
    while curr:
        vals.append(curr.val)
        curr = curr.next
    print(f"reverse_k_group([1,2,3,4,5], k=2) -> {vals}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Company-Wise LeetCode problem tracks")
    parser.add_argument(
        "--company",
        choices=["google", "meta", "amazon", "microsoft", "all"],
        default="all",
        help="Target company interview track (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "google": run_google_track,
        "meta": run_meta_track,
        "amazon": run_amazon_track,
        "microsoft": run_microsoft_track,
    }

    if args.company == "all":
        for comp, fn in dispatch.items():
            print(f"\n{'=' * 20} {comp.upper()} INTERVIEW TRACK {'=' * 20}")
            fn()
    else:
        dispatch[args.company]()


if __name__ == "__main__":
    main()
