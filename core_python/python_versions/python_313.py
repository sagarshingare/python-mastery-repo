"""
Python 3.13 Landmark Features & Idioms
=====================================
Released: October 2024

Key Features:
1. PEP 703: Free-threaded CPython (No-GIL / GIL-Disabled Build)
2. Experimental Copy-and-Patch JIT Compiler (Tier 2 bytecode compiler)
3. PEP 742: `typing.TypeIs` for Precise Bidirectional Type Narrowing
4. PEP 702: `@warnings.deprecated` Standard Deprecation Decorator
5. Next-Generation Interactive Interpreter / REPL (colored, multi-line editing)
"""

from __future__ import annotations
import sys
import warnings
from typing import Any, Callable, List, Optional, TypeVar

T = TypeVar("T")


# --- 1. PEP 703: Free-Threaded CPython (No-GIL) Architecture ---
def is_free_threaded_build() -> bool:
    """Detects if running on a free-threaded (No-GIL) Python 3.13 build."""
    if sys.version_info >= (3, 13):
        return getattr(sys, "_is_gil_enabled", lambda: True)() is False
    return False


def get_gil_architecture_notes() -> dict[str, str]:
    """Provides key architectural concepts of the Free-Threaded Python 3.13 runtime."""
    return {
        "Biased Reference Counting (BRC)": (
            "Thread-local reference counts avoid atomic instructions for single-thread objects, "
            "switching to atomic operations only when shared across threads."
        ),
        "Immortal Objects": (
            "Core singletons (None, True, False, small ints) have refcounts with a special flag "
            "so they are never modified, eliminating cache-line contention across CPU cores."
        ),
        "Mimalloc Integration": (
            "Microsoft mimalloc provides fast, thread-isolated heap allocation with low fragmentation."
        ),
        "Scaling Advantage": (
            "CPU-bound thread workloads scale linearly across multi-core systems without "
            "requiring multiprocessing process fork/spawn and IPC serialization."
        ),
    }


# --- 2. PEP 702: Standard @warnings.deprecated Decorator ---
def _get_deprecated_decorator() -> Callable[..., Any]:
    try:
        from warnings import deprecated  # Python 3.13+
        return deprecated
    except ImportError:
        def deprecated(message: str, category: type[Warning] = DeprecationWarning, stacklevel: int = 1) -> Callable[..., Any]:
            """Polyfill for PEP 702 @warnings.deprecated."""
            def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
                def wrapper(*args: Any, **kwargs: Any) -> Any:
                    warnings.warn(message, category=category, stacklevel=stacklevel + 1)
                    return func(*args, **kwargs)
                setattr(wrapper, "__deprecated__", message)
                return wrapper
            return decorator
        return deprecated

deprecated = _get_deprecated_decorator()


@deprecated("Use fetch_user_v2 instead; v1 will be removed in next release.")
def fetch_user_v1(user_id: int) -> dict[str, Any]:
    """Legacy user lookup function."""
    return {"id": user_id, "name": "Legacy User", "version": 1}


def fetch_user_v2(user_id: int) -> dict[str, Any]:
    """Modern user lookup function."""
    return {"id": user_id, "name": "Modern User", "version": 2}


# --- 3. PEP 742: typing.TypeIs (Type Narrowing) ---
# In Python 3.13:
# def is_string_list(val: list[object]) -> TypeIs[list[str]]:
#     return all(isinstance(x, str) for x in val)
# Unlike TypeGuard, TypeIs narrows BOTH branches (if -> list[str], else -> remaining types)
def check_is_string_list(items: list[Any]) -> bool:
    return all(isinstance(x, str) for x in items)


def run_python_313_demos() -> None:
    """Execute all Python 3.13 feature demonstrations."""
    print("=== Python 3.13 Feature Demonstrations ===")

    # 1. No-GIL status & architecture
    no_gil_active = is_free_threaded_build()
    print(f"1. Free-Threaded (No-GIL) Active: {no_gil_active}")
    print("   Architecture pillars:")
    for concept, explanation in get_gil_architecture_notes().items():
        print(f"   - {concept}: {explanation[:70]}...")

    # 2. @warnings.deprecated (PEP 702)
    print("\n2. PEP 702 @warnings.deprecated Demonstration:")
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        user = fetch_user_v1(42)
        print(f"   Called deprecated API: {user}")
        if captured:
            print(f"   Captured warning: {captured[-1].message}")

    # 3. JIT Compiler overview
    print("\n3. Copy-and-Patch JIT Overview:")
    print("   Compiles Tier 2 high-frequency execution traces directly to native assembly.")
    print("   Enabled via: python3.13 --experimental-jit")

    print("\nPython 3.13 demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_python_313_demos()
