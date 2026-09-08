"""Run Dynamic Programming algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.dynamic_programming.dp_examples import (
    coin_change,
    edit_distance,
    fibonacci_memo,
    fibonacci_tabulation,
    knapsack_01,
    longest_common_subsequence,
    longest_increasing_subsequence,
    max_subarray_sum,
)

logger = logging.getLogger(__name__)


def run_fibonacci_examples() -> None:
    logger.info("Running Fibonacci memoization vs tabulation")
    n = 15
    print(f"fibonacci_memo({n}) = {fibonacci_memo(n)}")
    print(f"fibonacci_tabulation({n}) = {fibonacci_tabulation(n)}")


def run_sequence_dp_examples() -> None:
    logger.info("Running LCS, LIS, and Edit Distance")
    s1, s2 = "abcde", "ace"
    print(f"longest_common_subsequence('{s1}', '{s2}') -> {longest_common_subsequence(s1, s2)}")

    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"longest_increasing_subsequence({nums}) -> {longest_increasing_subsequence(nums)}")

    w1, w2 = "horse", "ros"
    print(f"edit_distance('{w1}', '{w2}') -> {edit_distance(w1, w2)}")


def run_knapsack_and_coin_examples() -> None:
    logger.info("Running 0/1 Knapsack, Coin Change, and Kadane's Max Subarray")
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    max_val = knapsack_01(weights, values, capacity)
    print(f"knapsack_01(weights={weights}, values={values}, cap={capacity}) -> {max_val}")

    coins = [1, 2, 5]
    amount = 11
    min_coins = coin_change(coins, amount)
    print(f"coin_change(coins={coins}, amount={amount}) -> {min_coins} coins")

    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"max_subarray_sum({arr}) -> {max_subarray_sum(arr)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Dynamic Programming examples")
    parser.add_argument(
        "--module",
        choices=["fibonacci", "sequence", "optimization", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "fibonacci":
        run_fibonacci_examples()
    elif args.module == "sequence":
        run_sequence_dp_examples()
    elif args.module == "optimization":
        run_knapsack_and_coin_examples()
    else:
        run_fibonacci_examples()
        run_sequence_dp_examples()
        run_knapsack_and_coin_examples()


if __name__ == "__main__":
    main()
