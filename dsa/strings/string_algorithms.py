"""String algorithms: pattern matching, palindromes, anagrams, and more."""

from __future__ import annotations

from collections import Counter


def is_palindrome(s: str) -> bool:
    """Check whether *s* is a palindrome (case-insensitive, alphanumeric only).

    O(n) time, O(1) space using two pointers.
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def are_anagrams(s1: str, s2: str) -> bool:
    """Check whether *s1* and *s2* are anagrams. O(n)."""
    return Counter(s1.lower().replace(" ", "")) == Counter(s2.lower().replace(" ", ""))


def longest_common_prefix(strings: list[str]) -> str:
    """Return the longest common prefix of a list of strings. O(S) total chars."""
    if not strings:
        return ""
    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def kmp_search(text: str, pattern: str) -> list[int]:
    """Find all occurrences of *pattern* in *text* using the KMP algorithm.

    Returns a list of starting indices. O(n + m).
    """
    if not pattern:
        return []

    # Build partial match (failure) table
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    # Search
    matches: list[int] = []
    j = 0  # index in pattern
    for i, char in enumerate(text):
        while j > 0 and char != pattern[j]:
            j = lps[j - 1]
        if char == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)
            j = lps[j - 1]

    return matches


def longest_substring_without_repeats(s: str) -> str:
    """Return the longest substring without repeating characters. O(n)."""
    char_index: dict[str, int] = {}
    start = 0
    best_start = 0
    best_length = 0

    for i, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = i
        current_length = i - start + 1
        if current_length > best_length:
            best_length = current_length
            best_start = start

    return s[best_start : best_start + best_length]


def longest_common_substring(s1: str, s2: str) -> str:
    """Return the longest common substring of *s1* and *s2*. O(n * m)."""
    if not s1 or not s2:
        return ""

    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    max_len = 0
    end_index = 0

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_index = i

    return s1[end_index - max_len : end_index]


def reverse_words(s: str) -> str:
    """Reverse the order of words in *s*. O(n)."""
    return " ".join(s.split()[::-1])


def first_unique_char(s: str) -> int:
    """Return the index of the first non-repeating character, or -1. O(n)."""
    counts = Counter(s)
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
    return -1
