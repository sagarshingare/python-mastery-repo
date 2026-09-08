"""Backtracking algorithms: N-Queens, Sudoku, subset sum, and word search."""

from __future__ import annotations


def solve_n_queens(n: int) -> list[list[str]]:
    """Solve the N-Queens problem and return all valid board configurations.

    Each solution is a list of *n* strings where ``'Q'`` marks a queen
    and ``'.'`` marks an empty cell.
    """
    solutions: list[list[str]] = []
    cols: set[int] = set()
    pos_diag: set[int] = set()   # row + col
    neg_diag: set[int] = set()   # row - col
    board: list[list[str]] = [["." for _ in range(n)] for _ in range(n)]

    def _backtrack(row: int) -> None:
        if row == n:
            solutions.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = "Q"
            _backtrack(row + 1)
            board[row][col] = "."
            cols.discard(col)
            pos_diag.discard(row + col)
            neg_diag.discard(row - col)

    _backtrack(0)
    return solutions


def solve_sudoku(board: list[list[int]]) -> bool:
    """Solve a 9×9 Sudoku puzzle in-place. Empty cells are represented by 0.

    Returns True if solved, False if unsolvable.
    """

    def _is_valid(row: int, col: int, num: int) -> bool:
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def _solve() -> bool:
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if _is_valid(row, col, num):
                            board[row][col] = num
                            if _solve():
                                return True
                            board[row][col] = 0
                    return False
        return True

    return _solve()


def subset_sum(nums: list[int], target: int) -> list[list[int]]:
    """Find all subsets of *nums* that sum to *target*.

    Each combination is used at most once.
    """
    results: list[list[int]] = []
    nums_sorted = sorted(nums)

    def _backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        for i in range(start, len(nums_sorted)):
            if nums_sorted[i] > remaining:
                break
            if i > start and nums_sorted[i] == nums_sorted[i - 1]:
                continue  # skip duplicates
            path.append(nums_sorted[i])
            _backtrack(i + 1, remaining - nums_sorted[i], path)
            path.pop()

    _backtrack(0, target, [])
    return results


def word_search(board: list[list[str]], word: str) -> bool:
    """Check if *word* exists in a 2-D character grid (adjacent cells, no reuse)."""
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])

    def _search(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True
        if (
            row < 0 or row >= rows
            or col < 0 or col >= cols
            or board[row][col] != word[index]
        ):
            return False

        temp = board[row][col]
        board[row][col] = "#"  # mark visited

        found = (
            _search(row + 1, col, index + 1)
            or _search(row - 1, col, index + 1)
            or _search(row, col + 1, index + 1)
            or _search(row, col - 1, index + 1)
        )

        board[row][col] = temp  # restore
        return found

    for r in range(rows):
        for c in range(cols):
            if _search(r, c, 0):
                return True
    return False


def generate_parentheses(n: int) -> list[str]:
    """Generate all valid combinations of *n* pairs of parentheses."""
    results: list[str] = []

    def _backtrack(path: list[str], open_count: int, close_count: int) -> None:
        if len(path) == 2 * n:
            results.append("".join(path))
            return
        if open_count < n:
            path.append("(")
            _backtrack(path, open_count + 1, close_count)
            path.pop()
        if close_count < open_count:
            path.append(")")
            _backtrack(path, open_count, close_count + 1)
            path.pop()

    _backtrack([], 0, 0)
    return results
