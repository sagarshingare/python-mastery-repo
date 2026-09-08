"""Run Heap data structure and streaming algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.heaps.heap import (
    MaxHeap,
    MinHeap,
    find_median_stream,
    heapsort,
    k_smallest_elements,
    merge_k_sorted_lists,
    top_k_elements,
)

logger = logging.getLogger(__name__)


def run_min_max_heap_examples() -> None:
    logger.info("Running MinHeap & MaxHeap demonstrations")
    min_h = MinHeap()
    for val in [30, 10, 50, 20, 40]:
        min_h.push(val)
    print(f"MinHeap peek: {min_h.peek()}, size: {len(min_h)}")
    print(f"Popped min: {min_h.pop()}, new min: {min_h.peek()}")

    max_h = MaxHeap()
    for val in [30, 10, 50, 20, 40]:
        max_h.push(val)
    print(f"MaxHeap peek: {max_h.peek()}, size: {len(max_h)}")
    print(f"Popped max: {max_h.pop()}, new max: {max_h.peek()}")


def run_heapsort_and_topk_examples() -> None:
    logger.info("Running heapsort and top/smallest k demonstrations")
    nums = [12, 11, 13, 5, 6, 7]
    sorted_nums = heapsort(nums)
    print(f"Heapsort of {nums} -> {sorted_nums}")

    top3 = top_k_elements(nums, 3)
    smallest3 = k_smallest_elements(nums, 3)
    print(f"Top 3 elements: {top3}")
    print(f"Smallest 3 elements: {smallest3}")


def run_merge_and_median_examples() -> None:
    logger.info("Running merge K sorted lists and median stream")
    lists = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    merged = merge_k_sorted_lists(lists)
    print(f"merge_k_sorted_lists({lists}) -> {merged}")

    stream = [5, 15, 1, 3]
    medians = find_median_stream(stream)
    print(f"Running medians for stream {stream}: {medians}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Heap examples")
    parser.add_argument(
        "--module",
        choices=["heaps", "sort_topk", "streaming", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "heaps":
        run_min_max_heap_examples()
    elif args.module == "sort_topk":
        run_heapsort_and_topk_examples()
    elif args.module == "streaming":
        run_merge_and_median_examples()
    else:
        run_min_max_heap_examples()
        run_heapsort_and_topk_examples()
        run_merge_and_median_examples()


if __name__ == "__main__":
    main()
