"""Run String algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.strings.string_algorithms import (
    are_anagrams,
    first_unique_char,
    is_palindrome,
    kmp_search,
    longest_common_prefix,
    longest_common_substring,
    longest_substring_without_repeats,
    reverse_words,
)

logger = logging.getLogger(__name__)


def run_palindrome_anagram_examples() -> None:
    logger.info("Running palindrome and anagram validation")
    test_strings = ["A man, a plan, a canal: Panama", "race a car", "Was it a car or a cat I saw?"]
    for s in test_strings:
        print(f"is_palindrome({s!r}) -> {is_palindrome(s)}")

    print(f"are_anagrams('listen', 'silent') -> {are_anagrams('listen', 'silent')}")
    print(f"are_anagrams('hello', 'world') -> {are_anagrams('hello', 'world')}")


def run_matching_and_prefix_examples() -> None:
    logger.info("Running KMP pattern search and longest common prefix")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    matches = kmp_search(text, pattern)
    print(f"KMP search '{pattern}' in '{text}' -> indices: {matches}")

    words = ["flower", "flow", "flight"]
    lcp = longest_common_prefix(words)
    print(f"longest_common_prefix({words}) -> '{lcp}'")


def run_substring_and_transform_examples() -> None:
    logger.info("Running substring analysis and transformations")
    s = "abcabcbb"
    sub = longest_substring_without_repeats(s)
    length = len(sub)
    print(f"longest_substring_without_repeats('{s}') -> length={length}, substring='{sub}'")

    s1, s2 = "photograph", "autograph"
    lcs = longest_common_substring(s1, s2)
    print(f"longest_common_substring('{s1}', '{s2}') -> '{lcs}'")

    phrase = "  the sky   is blue  "
    reversed_phrase = reverse_words(phrase)
    print(f"reverse_words('{phrase}') -> '{reversed_phrase}'")

    uniq_idx = first_unique_char("loveleetcode")
    print(f"first_unique_char('loveleetcode') -> index {uniq_idx}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run String algorithm examples")
    parser.add_argument(
        "--module",
        choices=["palindromes", "matching", "substrings", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "palindromes":
        run_palindrome_anagram_examples()
    elif args.module == "matching":
        run_matching_and_prefix_examples()
    elif args.module == "substrings":
        run_substring_and_transform_examples()
    else:
        run_palindrome_anagram_examples()
        run_matching_and_prefix_examples()
        run_substring_and_transform_examples()


if __name__ == "__main__":
    main()
