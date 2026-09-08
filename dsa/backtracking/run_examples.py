"""Run Backtracking algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.backtracking.backtracking_examples import (
    generate_parentheses,
    solve_n_queens,
    solve_sudoku,
    subset_sum,
    word_search,
)

logger = logging.getLogger(__name__)


def run_n_queens_examples() -> None:
    logger.info("Running N-Queens backtracking solver")
    solutions_4 = solve_n_queens(4)
    print(f"4-Queens found {len(solutions_4)} solutions:")
    for sol in solutions_4:
        for row in sol:
            print(f"  {row}")
        print()


def run_sudoku_examples() -> None:
    logger.info("Running 9x9 Sudoku solver")
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    solved = solve_sudoku(board)
    print(f"Sudoku solved successfully: {solved}")
    for row in board:
        print(f"  {row}")


def run_combinatorial_backtracking_examples() -> None:
    logger.info("Running subset sum, parentheses generation, and 2D word search")
    nums = [10, 1, 2, 7, 6, 1, 5]
    target = 8
    subsets = subset_sum(nums, target)
    print(f"subset_sum({nums}, target={target}) -> {subsets}")

    parens = generate_parentheses(3)
    print(f"generate_parentheses(3) -> {parens}")

    grid = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    print(f"word_search('ABCCED') in grid: {word_search(grid, 'ABCCED')}")
    print(f"word_search('SEE') in grid: {word_search(grid, 'SEE')}")
    print(f"word_search('ABCB') in grid: {word_search(grid, 'ABCB')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Backtracking examples")
    parser.add_argument(
        "--module",
        choices=["queens", "sudoku", "combinatorial", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "queens":
        run_n_queens_examples()
    elif args.module == "sudoku":
        run_sudoku_examples()
    elif args.module == "combinatorial":
        run_combinatorial_backtracking_examples()
    else:
        run_n_queens_examples()
        run_sudoku_examples()
        run_combinatorial_backtracking_examples()


if __name__ == "__main__":
    main()
