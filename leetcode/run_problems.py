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
    "66-plus-one": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_66_plus_one,
        "category": "Arrays",
        "description": "Add one to a large integer represented as an array",
    },
    "136-single-number": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_136_single_number,
        "category": "Bit Manipulation",
        "description": "Find the unique number when others appear twice",
    },
    "88-merge-sorted-array": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_88_merge_sorted_array,
        "category": "Arrays",
        "description": "Merge two sorted arrays in-place",
    },
    "26-remove-duplicates-sorted-array": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_26_remove_duplicates_from_sorted_array,
        "category": "Arrays",
        "description": "Remove duplicates from sorted array in-place",
    },
    "27-remove-element": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_27_remove_element,
        "category": "Arrays",
        "description": "Remove specific elements in-place",
    },
    "83-remove-duplicates-sorted-list": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_83_remove_duplicates_sorted_list,
        "category": "Linked Lists",
        "description": "Remove duplicates from sorted linked list",
    },
    "141-linked-list-cycle": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_141_linked_list_cycle,
        "category": "Linked Lists",
        "description": "Detect cycle in linked list",
    },
    "104-max-depth-binary-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_104_max_depth_binary_tree,
        "category": "Trees",
        "description": "Compute maximum depth of a binary tree",
    },
    "234-palindrome-linked-list": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_234_palindrome_linked_list,
        "category": "Linked Lists",
        "description": "Check whether linked list is a palindrome",
    },
    "125-valid-palindrome": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_125_valid_palindrome,
        "category": "Strings",
        "description": "Validate palindrome with alphanumeric filtering",
    },
    "28-first-occurrence": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_28_find_index_first_occurrence_substring,
        "category": "Strings",
        "description": "Find first occurrence of substring",
    },
    "387-first-unique-character": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_387_first_unique_character_in_string,
        "category": "Strings",
        "description": "Find first non-repeating character",
    },
    "14-longest-common-prefix": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_14_longest_common_prefix,
        "category": "Strings",
        "description": "Find longest common prefix among strings",
    },
    "167-two-sum-ii": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_167_two_sum_ii_input_array_sorted,
        "category": "Two Pointers",
        "description": "Two sum in sorted array using two pointers",
    },
    "344-reverse-string": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_344_reverse_string,
        "category": "Two Pointers",
        "description": "Reverse character array in-place",
    },
    "70-climbing-stairs": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_70_climbing_stairs,
        "category": "Dynamic Programming",
        "description": "Count distinct ways to climb stairs",
    },
    "198-house-robber": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_198_house_robber,
        "category": "Dynamic Programming",
        "description": "Maximize robbery profit without adjacent thefts",
    },
    "202-happy-number": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_202_happy_number,
        "category": "Math",
        "description": "Determine if a number is happy",
    },
    "101-symmetric-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_101_symmetric_tree,
        "category": "Trees",
        "description": "Check whether binary tree is symmetric",
    },
    "257-binary-tree-paths": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_257_binary_tree_paths,
        "category": "Trees",
        "description": "List all root-to-leaf binary tree paths",
    },
    # MEDIUM PROBLEMS
    "3-longest-substring": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_3_longest_substring_without_repeating,
        "category": "Strings",
        "description": "Find the longest substring without repeating characters",
    },
    "39-combination-sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_39_combination_sum,
        "category": "Backtracking",
        "description": "Find all unique combinations summing to target",
    },
    "238-product-except-self": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_238_product_of_array_except_self,
        "category": "Arrays",
        "description": "Compute product of all elements except self",
    },
    "46-permutations": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_46_permutations,
        "category": "Backtracking",
        "description": "Generate all permutations of distinct integers",
    },
    "139-word-break": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_139_word_break,
        "category": "Dynamic Programming",
        "description": "Determine if string can be segmented into dictionary words",
    },
    "49-group-anagrams": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_49_group_anagrams,
        "category": "Hashing",
        "description": "Group words that are anagrams",
    },
    "33-search-rotated": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_33_search_in_rotated_sorted_array,
        "category": "Binary Search",
        "description": "Search in a rotated sorted array",
    },
    "15-3sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_15_3sum,
        "category": "Arrays",
        "description": "Find triplets that sum to zero",
    },
    "2-add-two-numbers": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_2_add_two_numbers,
        "category": "Linked Lists",
        "description": "Add two numbers represented as linked lists",
    },
    "19-remove-nth-node-from-end": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_19_remove_nth_node_from_end,
        "category": "Linked Lists",
        "description": "Remove the nth node from the end of list",
    },
    "24-swap-nodes-in-pairs": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_24_swap_nodes_in_pairs,
        "category": "Linked Lists",
        "description": "Swap adjacent linked list nodes in pairs",
    },
    "148-sort-list": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_148_sort_linked_list,
        "category": "Linked Lists",
        "description": "Sort a linked list in O(n log n)",
    },
    "102-binary-tree-level-order": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_102_binary_tree_level_order_traversal,
        "category": "Trees",
        "description": "Perform level-order traversal on a binary tree",
    },
    "105-construct-binary-tree": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_105_construct_binary_tree_from_preorder_inorder,
        "category": "Trees",
        "description": "Construct binary tree from preorder and inorder traversals",
    },
    "200-number-of-islands": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_200_number_of_islands,
        "category": "Graphs",
        "description": "Count islands in a 2D grid",
    },
    "207-course-schedule": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_207_course_schedule,
        "category": "Graphs",
        "description": "Check if course prerequisites allow completion",
    },
    "5-longest-palindrome-substring": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_5_longest_palindromic_substring,
        "category": "Strings",
        "description": "Find the longest palindromic substring",
    },
    "62-unique-paths": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_62_unique_paths,
        "category": "Dynamic Programming",
        "description": "Count unique grid paths",
    },
    "516-longest-palindromic-subsequence": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_516_longest_palindromic_subsequence,
        "category": "Dynamic Programming",
        "description": "Longest palindromic subsequence length",
    },
    "146-lru-cache": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_146_lru_cache,
        "category": "Design",
        "description": "Create an LRU cache object",
    },
    # HARD PROBLEMS
    "4-median-two-arrays": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_4_median_of_two_sorted_arrays,
        "category": "Binary Search",
        "description": "Find median of two sorted arrays",
    },
    "87-scramble-string": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_87_scramble_string,
        "category": "Dynamic Programming",
        "description": "Check if one string is a scramble of another",
    },
    "44-wildcard-matching": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_44_wildcard_matching,
        "category": "Strings",
        "description": "Match wildcard pattern against string",
    },
    "10-regex-matching": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_10_regular_expression_matching,
        "category": "Strings",
        "description": "Regular expression matching with '.' and '*'",
    },
    "37-sudoku-solver": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_37_sudoku_solver,
        "category": "Backtracking",
        "description": "Solve a Sudoku puzzle using backtracking",
    },
    "23-merge-k-sorted-lists": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_23_merge_k_sorted_lists,
        "category": "Heaps",
        "description": "Merge k sorted linked lists into one sorted list",
    },
    "124-binary-tree-max-path-sum": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_124_binary_tree_max_path_sum,
        "category": "Trees",
        "description": "Find maximum path sum in binary tree",
    },
    "212-word-search-ii": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_212_word_search_ii,
        "category": "Trie",
        "description": "Find words from dictionary in a board",
    },
    "42-trapping-water": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_42_trapping_rain_water,
        "category": "Arrays",
        "description": "Calculate trapped rainwater",
    },
    "239-sliding-window-maximum": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_239_sliding_window_maximum,
        "category": "Deque",
        "description": "Maximum value in each sliding window",
    },
    "84-largest-rectangle-histogram": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_84_largest_rectangle_in_histogram,
        "category": "Stacks",
        "description": "Find largest rectangle area in histogram",
    },
    "297-serialize-deserialize-binary-tree": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_297_serialize_deserialize_binary_tree,
        "category": "Trees",
        "description": "Serialize and deserialize a binary tree",
    },
    "32-longest-valid-parentheses": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_32_longest_valid_parentheses,
        "category": "Dynamic Programming",
        "description": "Longest valid parentheses substring",
    },
    "76-minimum-window-substring": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_76_minimum_window_substring,
        "category": "Strings",
        "description": "Find minimum window substring containing all characters",
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
