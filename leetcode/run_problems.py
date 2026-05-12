"""
LeetCode Problems CLI Runner

Interactive CLI for exploring, searching, and running LeetCode problems across
different difficulty levels (Easy, Medium, Hard).

Features:
  - Browse problems by difficulty and topic
  - Run test cases for specific problems
  - Display problem explanations and solutions
  - Performance analysis (time/space complexity)
"""

import argparse
import sys
from typing import Dict, List, Callable
from enum import Enum

# Import solution modules
from leetcode.easy import solutions as easy_solutions
from leetcode.medium import solutions as medium_solutions
from leetcode.hard import solutions as hard_solutions


class Difficulty(Enum):
    """Problem difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# Problem registry mapping problem names to functions
PROBLEM_REGISTRY: Dict[str, Dict] = {
    # EASY PROBLEMS
    "1-two-sum": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_1_two_sum,
        "category": "Arrays & Hashing",
        "description": "Find two numbers that add up to target",
    },
    "217-contains-duplicate": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_217_contains_duplicate,
        "category": "Arrays & Hashing",
        "description": "Check if array contains duplicates",
    },
    "242-valid-anagram": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_242_valid_anagram,
        "category": "Strings",
        "description": "Check if two strings are anagrams",
    },
    "121-best-time-buy-sell-stock": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_121_best_time_to_buy_sell_stock,
        "category": "Arrays",
        "description": "Find max profit buying and selling stock",
    },
    "125-valid-palindrome": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_125_valid_palindrome,
        "category": "Strings",
        "description": "Check if string is valid palindrome",
    },
    "20-valid-parentheses": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_20_valid_parentheses,
        "category": "Stack",
        "description": "Validate parentheses/brackets",
    },
    "70-climbing-stairs": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_70_climbing_stairs,
        "category": "Dynamic Programming",
        "description": "Count ways to climb n stairs",
    },
    "198-house-robber": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_198_house_robber,
        "category": "Dynamic Programming",
        "description": "Max money from robbing non-adjacent houses",
    },
    # MEDIUM PROBLEMS
    "3-longest-substring": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_3_longest_substring_without_repeating,
        "category": "Strings",
        "description": "Find longest substring without repeating characters",
    },
    "39-combination-sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_39_combination_sum,
        "category": "Backtracking",
        "description": "Find all combinations summing to target",
    },
    "49-group-anagrams": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_49_group_anagrams,
        "category": "Hashing",
        "description": "Group anagrams from list of strings",
    },
    "33-search-rotated": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_33_search_in_rotated_sorted_array,
        "category": "Binary Search",
        "description": "Search in rotated sorted array",
    },
    "15-3sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_15_3sum,
        "category": "Arrays",
        "description": "Find all triplets that sum to zero",
    },
    "5-longest-palindrome": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_5_longest_palindromic_substring,
        "category": "Strings",
        "description": "Find longest palindromic substring",
    },
    "62-unique-paths": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_62_unique_paths,
        "category": "Dynamic Programming",
        "description": "Count unique paths in grid",
    },
    "200-number-of-islands": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_200_number_of_islands,
        "category": "Graphs",
        "description": "Count number of islands in grid",
    },
    # HARD PROBLEMS
    "4-median-two-arrays": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_4_median_of_two_sorted_arrays,
        "category": "Binary Search",
        "description": "Find median of two sorted arrays",
    },
    "44-wildcard-matching": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_44_wildcard_matching,
        "category": "Strings",
        "description": "Wildcard pattern matching",
    },
    "10-regex-matching": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_10_regular_expression_matching,
        "category": "Strings",
        "description": "Regular expression matching",
    },
    "42-trapping-water": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_42_trapping_rain_water,
        "category": "Arrays",
        "description": "Calculate trapped rain water",
    },
    "76-min-window-substring": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_76_minimum_window_substring,
        "category": "Strings",
        "description": "Find minimum window substring",
    },
    "32-valid-parentheses": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_32_longest_valid_parentheses,
        "category": "Dynamic Programming",
        "description": "Longest valid parentheses substring",
    },
}


def print_header(title: str) -> None:
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title:^76}  ")
    print("=" * 80)


def print_section(title: str) -> None:
    """Print formatted section"""
    print(f"\n{title}")
    print("-" * 80)


def list_problems(difficulty: str = None, category: str = None) -> None:
    """List all problems, optionally filtered by difficulty or category"""
    print_header("LeetCode Problems Browser")
    
    # Group problems by difficulty
    by_difficulty = {}
    for problem_id, info in PROBLEM_REGISTRY.items():
        diff = info["difficulty"].value
        if difficulty and diff != difficulty:
            continue
        
        if diff not in by_difficulty:
            by_difficulty[diff] = {}
        
        cat = info["category"]
        if category and cat != category:
            continue
        
        if cat not in by_difficulty[diff]:
            by_difficulty[diff][cat] = []
        
        by_difficulty[diff][cat].append((problem_id, info["description"]))
    
    # Display problems
    for diff in ["easy", "medium", "hard"]:
        if diff in by_difficulty:
            print_section(f"{diff.upper()} Problems ({len([p for cat in by_difficulty[diff].values() for p in cat])} total)")
            
            for category_name in sorted(by_difficulty[diff].keys()):
                problems = by_difficulty[diff][category_name]
                print(f"\n  {category_name}:")
                for problem_id, description in sorted(problems):
                    print(f"    • {problem_id:30} - {description}")


def show_problem_details(problem_id: str) -> None:
    """Show detailed information about a problem"""
    if problem_id not in PROBLEM_REGISTRY:
        print(f"❌ Problem '{problem_id}' not found")
        return
    
    info = PROBLEM_REGISTRY[problem_id]
    print_header(f"Problem: {problem_id}")
    
    print(f"\nDifficulty: {info['difficulty'].value.upper()}")
    print(f"Category:   {info['category']}")
    print(f"Description: {info['description']}")
    print(f"\nFunction:   {info['function'].__name__}")
    
    # Print docstring
    if info['function'].__doc__:
        print_section("Documentation")
        print(info['function'].__doc__)


def run_problem(problem_id: str, *args) -> None:
    """Run a specific problem with given arguments"""
    if problem_id not in PROBLEM_REGISTRY:
        print(f"❌ Problem '{problem_id}' not found")
        return
    
    info = PROBLEM_REGISTRY[problem_id]
    func = info['function']
    
    print_header(f"Running: {problem_id}")
    
    try:
        # Try to parse arguments as Python literals
        parsed_args = []
        for arg in args:
            try:
                parsed_args.append(eval(arg))
            except:
                parsed_args.append(arg)
        
        result = func(*parsed_args)
        
        print(f"\n✅ Result: {result}")
        print(f"\nInput: {parsed_args}")
    except Exception as e:
        print(f"❌ Error running problem: {e}")


def run_all_tests(difficulty: str = None) -> None:
    """Run all test cases for a difficulty level"""
    print_header("Running All Tests")
    
    if difficulty == "easy":
        print("\n[EASY PROBLEMS]")
        easy_solutions.run_tests()
    elif difficulty == "medium":
        print("\n[MEDIUM PROBLEMS]")
        medium_solutions.run_tests()
    elif difficulty == "hard":
        print("\n[HARD PROBLEMS]")
        hard_solutions.run_tests()
    else:
        print("\n[EASY PROBLEMS]")
        easy_solutions.run_tests()
        print("\n[MEDIUM PROBLEMS]")
        medium_solutions.run_tests()
        print("\n[HARD PROBLEMS]")
        hard_solutions.run_tests()


def get_statistics() -> None:
    """Print statistics about problems"""
    print_header("LeetCode Problems Statistics")
    
    by_difficulty = {"easy": 0, "medium": 0, "hard": 0}
    by_category = {}
    
    for problem_id, info in PROBLEM_REGISTRY.items():
        diff = info["difficulty"].value
        by_difficulty[diff] += 1
        
        cat = info["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    
    print("\n📊 By Difficulty:")
    for diff in ["easy", "medium", "hard"]:
        print(f"  {diff.upper():10} : {by_difficulty[diff]:3} problems")
    
    print(f"\n  TOTAL     : {sum(by_difficulty.values()):3} problems")
    
    print("\n📚 By Category:")
    for category in sorted(by_category.keys()):
        print(f"  {category:30} : {by_category[category]:3} problems")


def main() -> None:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="LeetCode Problems CLI Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m leetcode.run_problems list                           # List all problems
  python -m leetcode.run_problems list --difficulty easy         # List easy problems
  python -m leetcode.run_problems show 1-two-sum                 # Show problem details
  python -m leetcode.run_problems run 1-two-sum [2,7,11,15] 9   # Run specific problem
  python -m leetcode.run_problems test easy                      # Run all easy tests
  python -m leetcode.run_problems stats                          # Show statistics
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List problems")
    list_parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], help="Filter by difficulty")
    list_parser.add_argument("--category", help="Filter by category")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show problem details")
    show_parser.add_argument("problem", help="Problem ID (e.g., 1-two-sum)")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a problem")
    run_parser.add_argument("problem", help="Problem ID")
    run_parser.add_argument("args", nargs="*", help="Problem arguments")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run all tests")
    test_parser.add_argument("difficulty", nargs="?", choices=["easy", "medium", "hard"], help="Difficulty level")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "list":
        list_problems(args.difficulty, args.category)
    elif args.command == "show":
        show_problem_details(args.problem)
    elif args.command == "run":
        run_problem(args.problem, *args.args)
    elif args.command == "test":
        run_all_tests(args.difficulty)
    elif args.command == "stats":
        get_statistics()


if __name__ == "__main__":
    main()
