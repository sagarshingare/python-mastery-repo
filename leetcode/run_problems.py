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
# Built dynamically from actual available functions
PROBLEM_REGISTRY: Dict[str, Dict] = {
    # EASY PROBLEMS
    "1-two-sum": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_1_two_sum,
        "category": "Arrays & Hashing",
        "description": "Find two numbers that add up to target",
    },
    "2-add-two-numbers": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_2_add_two_numbers,
        "category": "Linked Lists",
        "description": "Add two numbers represented as linked lists",
    },
    "20-valid-parentheses": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_20_valid_parentheses,
        "category": "Stack",
        "description": "Validate parentheses are correctly matched",
    },
    "21-merge-two-sorted-lists": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_21_merge_two_sorted_lists,
        "category": "Linked Lists",
        "description": "Merge two sorted linked lists",
    },
    "36-valid-sudoku": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_36_valid_sudoku,
        "category": "Hashing",
        "description": "Validate a partially filled sudoku board",
    },
    "49-group-anagrams": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_49_group_anagrams,
        "category": "Arrays & Hashing",
        "description": "Group words that are anagrams",
    },
    "53-maximum-subarray": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_53_maximum_subarray,
        "category": "Dynamic Programming",
        "description": "Find the contiguous subarray with largest sum",
    },
    "62-unique-paths": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_62_unique_paths,
        "category": "Dynamic Programming",
        "description": "Count unique grid paths from top-left to bottom-right",
    },
    "70-climbing-stairs": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_70_climbing_stairs,
        "category": "Dynamic Programming",
        "description": "Count distinct ways to climb stairs",
    },
    "100-same-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_100_same_tree,
        "category": "Trees",
        "description": "Check if two binary trees are identical",
    },
    "101-symmetric-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_101_symmetric_tree,
        "category": "Trees",
        "description": "Check whether binary tree is symmetric",
    },
    "104-max-depth-binary-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_104_max_depth_binary_tree,
        "category": "Trees",
        "description": "Compute maximum depth of a binary tree",
    },
    "110-balanced-binary-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_110_balanced_binary_tree,
        "category": "Trees",
        "description": "Check if binary tree is height-balanced",
    },
    "118-pascals-triangle": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_118_pascals_triangle,
        "category": "Arrays",
        "description": "Generate Pascal's triangle with numRows",
    },
    "121-best-time-buy-sell-stock": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_121_best_time_buy_sell_stock,
        "category": "Arrays",
        "description": "Find max profit buying and selling stock once",
    },
    "125-valid-palindrome": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_125_valid_palindrome,
        "category": "Strings",
        "description": "Validate palindrome with alphanumeric filtering",
    },
    "141-linked-list-cycle": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_141_linked_list_cycle,
        "category": "Linked Lists",
        "description": "Detect cycle in linked list",
    },
    "150-evaluate-rpn": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_150_evaluate_rpn,
        "category": "Stack",
        "description": "Evaluate Reverse Polish Notation expression",
    },
    "155-min-stack": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_155_min_stack,
        "category": "Stack",
        "description": "Design stack that supports push/pop/top/getMin",
    },
    "198-house-robber": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_198_house_robber,
        "category": "Dynamic Programming",
        "description": "Maximize robbery profit without adjacent houses",
    },
    "205-isomorphic-strings": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_205_isomorphic_strings,
        "category": "Strings",
        "description": "Check if strings are isomorphic",
    },
    "206-reverse-linked-list": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_206_reverse_linked_list,
        "category": "Linked Lists",
        "description": "Reverse a singly linked list",
    },
    "217-contains-duplicate": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_217_contains_duplicate,
        "category": "Arrays & Hashing",
        "description": "Check if array contains duplicates",
    },
    "226-invert-binary-tree": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_226_invert_binary_tree,
        "category": "Trees",
        "description": "Invert a binary tree (mirror image)",
    },
    "232-implement-queue-using-stacks": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_232_implement_queue_using_stacks,
        "category": "Stack",
        "description": "Implement queue using two stacks",
    },
    "234-palindrome-linked-list": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_234_palindrome_linked_list,
        "category": "Linked Lists",
        "description": "Check whether linked list is a palindrome",
    },
    "235-lowest-common-ancestor-bst": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_235_lowest_common_ancestor_bst,
        "category": "Trees",
        "description": "Find LCA in binary search tree",
    },
    "238-product-array-except-self": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_238_product_array_except_self,
        "category": "Arrays",
        "description": "Compute product of all elements except self",
    },
    "242-valid-anagram": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_242_valid_anagram,
        "category": "Strings",
        "description": "Check if two strings are anagrams",
    },
    "271-encode-decode-strings": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_271_encode_decode_strings,
        "category": "Arrays & Hashing",
        "description": "Encode and decode list of strings",
    },
    "290-word-pattern": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_290_word_pattern,
        "category": "Strings",
        "description": "Check if string matches pattern",
    },
    "344-reverse-string": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_344_reverse_string,
        "category": "Two Pointers",
        "description": "Reverse character array in-place",
    },
    "347-top-k-frequent": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_347_top_k_frequent,
        "category": "Hashing",
        "description": "Find k most frequent elements",
    },
    "383-ransom-note": {
        "difficulty": Difficulty.EASY,
        "function": easy_solutions.problem_383_ransom_note,
        "category": "Strings",
        "description": "Check if ransom note can be constructed",
    },
    # MEDIUM PROBLEMS
    "3-longest-substring-without-repeating": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_3_longest_substring_without_repeating,
        "category": "Strings",
        "description": "Find longest substring without repeating characters",
    },
    "5-longest-palindromic-substring": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_5_longest_palindromic_substring,
        "category": "Strings",
        "description": "Find the longest palindromic substring",
    },
    "11-container-with-most-water": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_11_container_with_most_water,
        "category": "Two Pointers",
        "description": "Find two lines that form largest container",
    },
    "15-three-sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_15_three_sum,
        "category": "Arrays",
        "description": "Find triplets that sum to zero",
    },
    "24-swap-nodes-in-pairs": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_24_swap_nodes_in_pairs,
        "category": "Linked Lists",
        "description": "Swap adjacent linked list nodes in pairs",
    },
    "54-spiral-matrix": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_54_spiral_matrix,
        "category": "Arrays",
        "description": "Traverse matrix in spiral order",
    },
    "73-set-matrix-zeroes": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_73_set_matrix_zeroes,
        "category": "Arrays",
        "description": "Set matrix elements to zero if they contain zero",
    },
    "92-reverse-linked-list-ii": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_92_reverse_linked_list_ii,
        "category": "Linked Lists",
        "description": "Reverse a portion of linked list",
    },
    "98-validate-bst": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_98_validate_bst,
        "category": "Trees",
        "description": "Validate if tree is binary search tree",
    },
    "102-binary-tree-level-order": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_102_binary_tree_level_order,
        "category": "Trees",
        "description": "Perform level-order traversal on binary tree",
    },
    "105-construct-tree-preorder-inorder": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_105_construct_tree_preorder_inorder,
        "category": "Trees",
        "description": "Construct binary tree from preorder and inorder",
    },
    "139-word-break": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_139_word_break,
        "category": "Dynamic Programming",
        "description": "Determine if string can be segmented into words",
    },
    "148-sort-list": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_148_sort_list,
        "category": "Linked Lists",
        "description": "Sort a linked list in O(n log n)",
    },
    "151-reverse-words": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_151_reverse_words,
        "category": "Strings",
        "description": "Reverse words in a string",
    },
    "152-maximum-product-subarray": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_152_maximum_product_subarray,
        "category": "Dynamic Programming",
        "description": "Find contiguous subarray with max product",
    },
    "160-intersection-two-lists": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_160_intersection_two_lists,
        "category": "Linked Lists",
        "description": "Find intersection of two linked lists",
    },
    "200-number-of-islands": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_200_number_of_islands,
        "category": "Graphs",
        "description": "Count islands in a 2D grid",
    },
    "227-basic-calculator-ii": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_227_basic_calculator_ii,
        "category": "Stack",
        "description": "Implement calculator supporting +,-,*,/",
    },
    "300-longest-increasing-subsequence": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_300_longest_increasing_subsequence,
        "category": "Dynamic Programming",
        "description": "Find length of longest increasing subsequence",
    },
    "394-decode-string": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_394_decode_string,
        "category": "Stack",
        "description": "Decode encoded string",
    },
    "416-partition-equal-subset-sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_416_partition_equal_subset_sum,
        "category": "Dynamic Programming",
        "description": "Partition array into equal sum subsets",
    },
    "494-target-sum": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_494_target_sum,
        "category": "Dynamic Programming",
        "description": "Find ways to assign signs to achieve target sum",
    },
    "621-task-scheduler": {
        "difficulty": Difficulty.MEDIUM,
        "function": medium_solutions.problem_621_task_scheduler,
        "category": "Scheduling",
        "description": "Schedule tasks with cooldown period",
    },
    # HARD PROBLEMS
    "4-median-two-sorted-arrays": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_4_median_two_sorted_arrays,
        "category": "Binary Search",
        "description": "Find median of two sorted arrays",
    },
    "10-regular-expression-matching": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_10_regular_expression_matching,
        "category": "Strings",
        "description": "Regular expression matching with '.' and '*'",
    },
    "23-merge-k-sorted-lists": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_23_merge_k_sorted_lists,
        "category": "Linked Lists",
        "description": "Merge k sorted linked lists",
    },
    "25-reverse-nodes-k-group": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_25_reverse_nodes_k_group,
        "category": "Linked Lists",
        "description": "Reverse nodes in k-group",
    },
    "37-sudoku-solver": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_37_sudoku_solver,
        "category": "Backtracking",
        "description": "Solve a Sudoku puzzle",
    },
    "42-trapping-rain-water": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_42_trapping_rain_water,
        "category": "Arrays",
        "description": "Calculate trapped rainwater",
    },
    "72-edit-distance": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_72_edit_distance,
        "category": "Dynamic Programming",
        "description": "Calculate minimum edit distance (Levenshtein)",
    },
    "84-largest-rectangle-histogram": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_84_largest_rectangle_histogram,
        "category": "Stack",
        "description": "Find largest rectangle area in histogram",
    },
    "123-best-time-buy-sell-stock-iii": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_123_best_time_buy_sell_stock_iii,
        "category": "Dynamic Programming",
        "description": "Max profit with at most 2 transactions",
    },
    "124-binary-tree-max-path-sum": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_124_binary_tree_max_path_sum,
        "category": "Trees",
        "description": "Find maximum path sum in binary tree",
    },
    "146-lru-cache": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_146_lru_cache,
        "category": "Design",
        "description": "Design and implement LRU cache",
    },
    "188-best-time-buy-sell-stock-iv": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_188_best_time_buy_sell_stock_iv,
        "category": "Dynamic Programming",
        "description": "Max profit with at most k transactions",
    },
    "212-word-search-ii": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_212_word_search_ii,
        "category": "Trie",
        "description": "Find words from dictionary in board",
    },
    "295-find-median-data-stream": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_295_find_median_data_stream,
        "category": "Heaps",
        "description": "Find median from data stream",
    },
    "297-serialize-deserialize-bst": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_297_serialize_deserialize_bst,
        "category": "Trees",
        "description": "Serialize and deserialize BST",
    },
    "312-burst-balloons": {
        "difficulty": Difficulty.HARD,
        "function": hard_solutions.problem_312_burst_balloons,
        "category": "Dynamic Programming",
        "description": "Maximize coins by bursting balloons",
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
