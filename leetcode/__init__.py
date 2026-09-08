"""LeetCode Practice and Interview Preparation Mastery Package.

Organized into progressive tiers:
- easy: 60+ foundational problems (Arrays, Two Pointers, Linked Lists, Trees, DP)
- medium: 80+ core interview patterns (Sliding Window, BST, Graphs, Multi-state DP)
- hard: 50+ advanced problems (Median of Two Arrays, Rain Water, Burst Balloons, Monotonic Stacks)
- company_wise: High-frequency interview tracks (Google, Meta, Amazon, Microsoft)
"""

from . import company_wise
from . import easy
from . import hard
from . import medium
from . import run_problems

__all__ = [
    "company_wise",
    "easy",
    "hard",
    "medium",
    "run_problems",
]
