"""Run Recursion and Divide & Conquer demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.recursion.recursion_examples import (
    factorial,
    fibonacci,
    flatten_nested,
    flood_fill,
    permutations,
    power,
    power_set,
    tower_of_hanoi,
)

logger = logging.getLogger(__name__)


def run_math_recursion_examples() -> None:
    logger.info("Running fundamental math recursion (factorial, fibonacci, power)")
    print(f"factorial(5) = {factorial(5)}")
    print(f"fibonacci(8) = {fibonacci(8)}")
    print(f"power(2, 10) = {power(2, 10)} (fast modular/exponentiation)")


def run_combinatorics_examples() -> None:
    logger.info("Running combinatorial recursion (power set, permutations)")
    items = [1, 2, 3]
    pset = power_set(items)
    print(f"power_set({items}) -> {pset} (count: {len(pset)})")

    perms = permutations(items)
    print(f"permutations({items}) -> {perms} (count: {len(perms)})")


def run_divide_and_conquer_examples() -> None:
    logger.info("Running Tower of Hanoi, Flood Fill, and Tree/Nested Flattening")
    hanoi_steps = tower_of_hanoi(3, "A", "C", "B")
    print(f"Tower of Hanoi (3 discs) moves count: {len(hanoi_steps)}")
    for move in hanoi_steps:
        print(f"  {move}")

    image = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]
    print("Original grid for flood fill:")
    for row in image:
        print(f"  {row}")
    flood_fill(image, row=1, col=1, new_color=2)
    print("After flood_fill at (1, 1) with color 2:")
    for row in image:
        print(f"  {row}")

    nested = [1, [2, [3, 4], 5], [[6]], 7]
    flat = flatten_nested(nested)
    print(f"flatten_nested({nested}) -> {flat}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Recursion examples")
    parser.add_argument(
        "--module",
        choices=["math", "combinatorics", "divide_conquer", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "math":
        run_math_recursion_examples()
    elif args.module == "combinatorics":
        run_combinatorics_examples()
    elif args.module == "divide_conquer":
        run_divide_and_conquer_examples()
    else:
        run_math_recursion_examples()
        run_combinatorics_examples()
        run_divide_and_conquer_examples()


if __name__ == "__main__":
    main()
