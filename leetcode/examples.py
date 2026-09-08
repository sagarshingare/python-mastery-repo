"""Standard entry point alias for the LeetCode module.

Provides unified CLI access to LeetCode Easy, Medium, Hard, and Company-Wise problems.
"""

from __future__ import annotations

import sys
from .run_problems import main


def run_showcase() -> None:
    """Run summary statistics and quick validations across all tiers."""
    from leetcode.easy.run_examples import run_arrays_hashing_examples
    from leetcode.medium.run_examples import run_arrays_two_pointers_examples
    from leetcode.hard.run_examples import run_arrays_binary_search_examples
    from leetcode.company_wise.run_examples import run_google_track

    print("================================================================================")
    print("                      LeetCode Mastery Suite Showcase                           ")
    print("================================================================================\n")
    run_arrays_hashing_examples()
    print()
    run_arrays_two_pointers_examples()
    print()
    run_arrays_binary_search_examples()
    print()
    run_google_track()
    print("\n--- Use 'python3 -m leetcode.run_problems --help' for interactive problem exploration. ---")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_showcase()
    else:
        main()
