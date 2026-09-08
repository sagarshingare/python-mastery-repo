"""Run Array and Search algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.arrays.array_utils import (
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

logger = logging.getLogger(__name__)


def run_dynamic_array_examples() -> None:
    logger.info("Running DynamicArray demonstrations")
    arr: DynamicArray[int] = DynamicArray()
    for x in [10, 20, 30, 40, 50]:
        arr.append(x)
    print(f"DynamicArray after appends: {arr}, size: {len(arr)}, capacity: {arr.capacity}")
    popped = arr.pop()
    print(f"Popped value: {popped}, remaining: {arr}")
    arr.insert(1, 15)
    print(f"After insert(1, 15): {arr}")


def run_search_examples() -> None:
    logger.info("Running search algorithm demonstrations")
    data = [11, 22, 33, 44, 55, 66, 77, 88]
    print(f"Dataset: {data}")
    lin_idx = linear_search(data, 44)
    print(f"Linear search for 44: index {lin_idx}")
    bin_idx = binary_search(data, 77)
    print(f"Binary search for 77: index {bin_idx}")


def run_two_pointer_examples() -> None:
    logger.info("Running two-pointer technique demonstrations")
    sorted_nums = [2, 7, 11, 15]
    target = 9
    pair = two_sum_sorted(sorted_nums, target)
    print(f"two_sum_sorted({sorted_nums}, {target}) -> indices: {pair}")

    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    water = container_with_most_water(heights)
    print(f"container_with_most_water({heights}) -> max area: {water}")

    dups = [1, 1, 2, 2, 3, 4, 4]
    new_len = remove_duplicates_inplace(dups)
    print(f"remove_duplicates_inplace -> length {new_len}, unique prefix: {dups[:new_len]}")


def run_prefix_sum_and_subarray_examples() -> None:
    logger.info("Running prefix sum and subarray demonstrations")
    nums = [1, 2, 3, 4, 5]
    ps = PrefixSum(nums)
    range_sum = ps.query(1, 3)  # nums[1] + nums[2] + nums[3] = 2 + 3 + 4 = 9
    print(f"PrefixSum({nums}).query(1, 3) -> {range_sum}")

    k_nums = [1, 1, 1]
    count = subarray_sum_equals_k(k_nums, 2)
    print(f"subarray_sum_equals_k({k_nums}, 2) -> {count}")

    kadane_nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    max_sum = max_subarray_sum(kadane_nums)
    print(f"Kadane's max subarray sum: {max_sum}")


def run_partition_and_interval_examples() -> None:
    logger.info("Running Dutch National Flag, Intervals, and Rotation")
    colors = [2, 0, 2, 1, 1, 0]
    sort_colors(colors)
    print(f"Dutch National Flag sort_colors -> {colors}")

    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    merged = merge_intervals(intervals)
    print(f"merge_intervals -> {merged}")

    rot_nums = [1, 2, 3, 4, 5, 6, 7]
    rotate_array_inplace(rot_nums, 3)
    print(f"rotate_array_inplace by 3 -> {rot_nums}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Array & Search examples")
    parser.add_argument(
        "--module",
        choices=["dynamic", "search", "two_pointer", "subarray", "intervals", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "dynamic": run_dynamic_array_examples,
        "search": run_search_examples,
        "two_pointer": run_two_pointer_examples,
        "subarray": run_prefix_sum_and_subarray_examples,
        "intervals": run_partition_and_interval_examples,
    }

    if args.module == "all":
        for fn in dispatch.values():
            fn()
    else:
        dispatch[args.module]()


if __name__ == "__main__":
    main()
