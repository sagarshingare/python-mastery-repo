"""
Python Version Evolution & Modern Features (Python 3.8 — 3.13)
==============================================================
A comprehensive guide, runtime checker, and demonstration suite of features
introduced across modern Python releases.
"""

from .version_matrix import (
    get_all_capabilities,
    print_capability_report,
    has_walrus_operator,
    has_positional_only_params,
    has_dict_merge_operators,
    has_removeprefix_suffix,
    has_pep585_generics,
    has_pattern_matching,
    has_union_type_operator,
    has_exception_groups,
    has_asyncio_taskgroup,
    has_pep695_generics,
    has_nogil,
)

__all__ = [
    "get_all_capabilities",
    "print_capability_report",
    "has_walrus_operator",
    "has_positional_only_params",
    "has_dict_merge_operators",
    "has_removeprefix_suffix",
    "has_pep585_generics",
    "has_pattern_matching",
    "has_union_type_operator",
    "has_exception_groups",
    "has_asyncio_taskgroup",
    "has_pep695_generics",
    "has_nogil",
]
