"""Unified CLI runner for all Data Structures and Algorithms modules."""

from __future__ import annotations

import argparse
import logging
import sys

from dsa.arrays.run_examples import run_dynamic_array_examples, run_partition_and_interval_examples, run_prefix_sum_and_subarray_examples, run_search_examples, run_two_pointer_examples
from dsa.linked_list.run_examples import run_doubly_linked_list_examples, run_singly_linked_list_examples
from dsa.stack.run_examples import run_min_stack_examples, run_parentheses_examples, run_postfix_and_monotonic_examples, run_stack_basics_examples
from dsa.queue.run_examples import run_circular_queue_examples, run_deque_examples, run_fifo_queue_examples, run_priority_queue_examples
from dsa.trees.run_examples import run_bst_examples, run_lca_and_validation_examples, run_traversals_examples
from dsa.graphs.run_examples import run_dijkstra_examples, run_dsu_examples, run_topological_sort_examples, run_traversal_examples
from dsa.heaps.run_examples import run_heapsort_and_topk_examples, run_merge_and_median_examples, run_min_max_heap_examples
from dsa.strings.run_examples import run_matching_and_prefix_examples, run_palindrome_anagram_examples, run_substring_and_transform_examples
from dsa.recursion.run_examples import run_combinatorics_examples, run_divide_and_conquer_examples, run_math_recursion_examples
from dsa.sliding_window.run_examples import run_dynamic_window_examples, run_fixed_window_examples
from dsa.backtracking.run_examples import run_combinatorial_backtracking_examples, run_n_queens_examples, run_sudoku_examples
from dsa.dynamic_programming.run_examples import run_fibonacci_examples, run_knapsack_and_coin_examples, run_sequence_dp_examples
from dsa.system_design.run_examples import run_bloom_filter_examples, run_lfu_cache_examples, run_lru_cache_examples, run_trie_examples

logger = logging.getLogger(__name__)

MODULE_RUNNERS = {
    "arrays": [
        run_dynamic_array_examples,
        run_search_examples,
        run_two_pointer_examples,
        run_prefix_sum_and_subarray_examples,
        run_partition_and_interval_examples,
    ],
    "linked_list": [
        run_singly_linked_list_examples,
        run_doubly_linked_list_examples,
    ],
    "stack": [
        run_stack_basics_examples,
        run_min_stack_examples,
        run_parentheses_examples,
        run_postfix_and_monotonic_examples,
    ],
    "queue": [
        run_fifo_queue_examples,
        run_circular_queue_examples,
        run_priority_queue_examples,
        run_deque_examples,
    ],
    "trees": [
        run_bst_examples,
        run_traversals_examples,
        run_lca_and_validation_examples,
    ],
    "graphs": [
        run_traversal_examples,
        run_topological_sort_examples,
        run_dijkstra_examples,
        run_dsu_examples,
    ],
    "heaps": [
        run_min_max_heap_examples,
        run_heapsort_and_topk_examples,
        run_merge_and_median_examples,
    ],
    "strings": [
        run_palindrome_anagram_examples,
        run_matching_and_prefix_examples,
        run_substring_and_transform_examples,
    ],
    "recursion": [
        run_math_recursion_examples,
        run_combinatorics_examples,
        run_divide_and_conquer_examples,
    ],
    "sliding_window": [
        run_fixed_window_examples,
        run_dynamic_window_examples,
    ],
    "backtracking": [
        run_n_queens_examples,
        run_sudoku_examples,
        run_combinatorial_backtracking_examples,
    ],
    "dynamic_programming": [
        run_fibonacci_examples,
        run_sequence_dp_examples,
        run_knapsack_and_coin_examples,
    ],
    "system_design": [
        run_lru_cache_examples,
        run_lfu_cache_examples,
        run_trie_examples,
        run_bloom_filter_examples,
    ],
}


def run_submodule(name: str) -> None:
    """Execute all demonstrations for a specific submodule."""
    runners = MODULE_RUNNERS.get(name)
    if not runners:
        print(f"Unknown module: {name}")
        return
    print(f"\n{'=' * 20} Running Module: DSA.{name.upper()} {'=' * 20}")
    for runner in runners:
        runner()


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified CLI runner for DSA demonstrations")
    parser.add_argument(
        "--module",
        choices=list(MODULE_RUNNERS.keys()) + ["all"],
        default="all",
        help="Submodule to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "all":
        for mod in MODULE_RUNNERS:
            run_submodule(mod)
    else:
        run_submodule(args.module)


if __name__ == "__main__":
    main()
