# Strings

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.2: Strings**

String manipulation algorithms, palindrome validation, anagram detection, and substring pattern search.

## Key Algorithms

- **Palindromes (`is_palindrome`)**: Two-pointer alphanumeric validation.
- **Anagrams (`are_anagrams`)**: Frequency map / character counting comparison.
- **Longest Common Prefix (`longest_common_prefix`)**: Horizontal scanning.
- **KMP Pattern Search (`kmp_search`)**: Knuth-Morris-Pratt substring search in $O(n + m)$ using $\pi$ prefix failure table.
- **Word Reversal (`reverse_words`)**: In-place whitespace splitting.

## Quick Start

```python
from dsa.strings import is_palindrome, are_anagrams, kmp_search

assert is_palindrome("A man, a plan, a canal: Panama") is True
assert are_anagrams("listen", "silent") is True
assert kmp_search("ABABDABACDABABCABAB", "ABABCABAB") == [10]
```
