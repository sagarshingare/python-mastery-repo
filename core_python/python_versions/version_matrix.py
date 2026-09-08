"""
Python Version Capability Matrix & Runtime Feature Detection
============================================================
Provides introspective capabilities to detect which language features,
syntax extensions, and standard library modules are natively supported
by the active Python interpreter.
"""

from __future__ import annotations
import sys
from typing import Any, Dict, NamedTuple


class VersionCapability(NamedTuple):
    feature_name: str
    introduced_version: str
    is_supported: bool
    description: str


def has_walrus_operator() -> bool:
    """Assignment expressions (:=) introduced in Python 3.8 (PEP 572)."""
    return sys.version_info >= (3, 8)


def has_positional_only_params() -> bool:
    """Positional-only syntax (/) introduced in Python 3.8 (PEP 570)."""
    return sys.version_info >= (3, 8)


def has_dict_merge_operators() -> bool:
    """Dictionary merge (|) and update (|=) introduced in Python 3.9 (PEP 584)."""
    return sys.version_info >= (3, 9)


def has_removeprefix_suffix() -> bool:
    """String methods removeprefix() & removesuffix() introduced in Python 3.9 (PEP 616)."""
    return hasattr(str, "removeprefix") and hasattr(str, "removesuffix")


def has_pep585_generics() -> bool:
    """Builtin generics like list[int] and dict[str, Any] in Python 3.9 (PEP 585)."""
    return sys.version_info >= (3, 9)


def has_pattern_matching() -> bool:
    """Structural Pattern Matching (match/case) introduced in Python 3.10 (PEP 634)."""
    return sys.version_info >= (3, 10)


def has_union_type_operator() -> bool:
    """Type union operator (X | Y) introduced in Python 3.10 (PEP 604)."""
    return sys.version_info >= (3, 10)


def has_strict_zip() -> bool:
    """zip(..., strict=True) introduced in Python 3.10 (PEP 618)."""
    return sys.version_info >= (3, 10)


def has_parenthesized_context_managers() -> bool:
    """Parenthesized with-statements introduced in Python 3.10."""
    return sys.version_info >= (3, 10)


def has_exception_groups() -> bool:
    """Exception groups and except* syntax introduced in Python 3.11 (PEP 654)."""
    return sys.version_info >= (3, 11) and hasattr(__builtins__, "ExceptionGroup") if isinstance(__builtins__, dict) else hasattr(__builtins__, "ExceptionGroup")


def has_exception_notes() -> bool:
    """BaseException.add_note() introduced in Python 3.11 (PEP 678)."""
    return hasattr(BaseException, "add_note")


def has_asyncio_taskgroup() -> bool:
    """asyncio.TaskGroup structured concurrency in Python 3.11 (PEP 654)."""
    import asyncio
    return hasattr(asyncio, "TaskGroup")


def has_tomllib() -> bool:
    """tomllib standard TOML parser in Python 3.11 (PEP 680)."""
    try:
        import tomllib  # noqa: F401
        return True
    except ImportError:
        return False


def has_pep695_generics() -> bool:
    """PEP 695 type parameter syntax ('type X = ...', 'def f[T]():') in Python 3.12."""
    return sys.version_info >= (3, 12)


def has_pep701_fstrings() -> bool:
    """PEP 701 formalized f-strings syntax (nested quotes, escapes) in Python 3.12."""
    return sys.version_info >= (3, 12)


def has_type_override() -> bool:
    """typing.override decorator in Python 3.12 (PEP 698)."""
    import typing
    return hasattr(typing, "override")


def has_nogil() -> bool:
    """PEP 703 Free-threaded CPython (No-GIL build) in Python 3.13."""
    if sys.version_info >= (3, 13):
        return getattr(sys, "_is_gil_enabled", lambda: True)() is False
    return False


def has_type_is() -> bool:
    """typing.TypeIs type form narrowing in Python 3.13 (PEP 742)."""
    import typing
    return hasattr(typing, "TypeIs")


def has_deprecated_decorator() -> bool:
    """warnings.deprecated decorator in Python 3.13 (PEP 702)."""
    import warnings
    return hasattr(warnings, "deprecated")


def get_all_capabilities() -> list[VersionCapability]:
    """Return an inventory of all Python version capabilities and support status."""
    return [
        VersionCapability("Walrus Operator (:=)", "3.8", has_walrus_operator(), "Assignment expressions inside conditions/loops"),
        VersionCapability("Positional-Only Params (/)", "3.8", has_positional_only_params(), "Enforce positional call semantics"),
        VersionCapability("Dict Merge & Update (|)", "3.9", has_dict_merge_operators(), "Merge dictionaries with pipe operators"),
        VersionCapability("removeprefix / suffix", "3.9", has_removeprefix_suffix(), "Strip string prefix/suffix cleanly"),
        VersionCapability("PEP 585 Built-in Generics", "3.9", has_pep585_generics(), "list[T] and dict[K, V] without typing module"),
        VersionCapability("Structural Pattern Match", "3.10", has_pattern_matching(), "match / case pattern matching"),
        VersionCapability("Type Union Operator (|)", "3.10", has_union_type_operator(), "X | Y type annotation syntax"),
        VersionCapability("zip(strict=True)", "3.10", has_strict_zip(), "Ensure zipped iterables match lengths"),
        VersionCapability("Exception Groups (except*)", "3.11", has_exception_groups(), "Handle multiple concurrent exceptions"),
        VersionCapability("Exception Notes (add_note)", "3.11", has_exception_notes(), "Enrich exceptions with diagnostic notes"),
        VersionCapability("asyncio.TaskGroup", "3.11", has_asyncio_taskgroup(), "Native structured concurrency scope"),
        VersionCapability("tomllib (Standard TOML)", "3.11", has_tomllib(), "Parse TOML configurations natively"),
        VersionCapability("PEP 695 Type Syntax", "3.12", has_pep695_generics(), "type Alias = ... and generic syntax def f[T]"),
        VersionCapability("PEP 701 Nested f-strings", "3.12", has_pep701_fstrings(), "Reusable quotes and backslashes in f-strings"),
        VersionCapability("typing.override", "3.12", has_type_override(), "Decorator indicating explicit method override"),
        VersionCapability("Free-threaded (No-GIL)", "3.13", has_nogil(), "PEP 703 true multi-core CPU threading"),
        VersionCapability("typing.TypeIs", "3.13", has_type_is(), "PEP 742 type-narrowing predicate returns"),
        VersionCapability("warnings.deprecated", "3.13", has_deprecated_decorator(), "PEP 702 standard deprecation decorator"),
    ]


def print_capability_report() -> None:
    """Prints a styled terminal report of the active runtime's capabilities."""
    version_str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print("=" * 80)
    print(f" PYTHON RUNTIME CAPABILITY MATRIX (Active: Python {version_str})")
    print("=" * 80)
    print(f"{'Feature Name':<30} | {'Since':<6} | {'Status':<11} | {'Description'}")
    print("-" * 80)

    caps = get_all_capabilities()
    for cap in caps:
        status = "ACTIVE" if cap.is_supported else "FUTURE"
        symbol = "[x]" if cap.is_supported else "[ ]"
        print(f"{symbol} {cap.feature_name:<26} | {cap.introduced_version:<6} | {status:<11} | {cap.description}")

    print("=" * 80)
    print(f"Supported on current host: {sum(1 for c in caps if c.is_supported)} / {len(caps)}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print_capability_report()
