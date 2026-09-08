"""
Python 3.12 Landmark Features & Idioms
=====================================
Released: October 2023

Key Features:
1. PEP 695: New Type Parameter Syntax (`type Point = ...`, `def f[T]():`)
2. PEP 701: Syntactic Formalization of f-strings (nested quotes, backslashes in `{}`)
3. PEP 698: `typing.override` Decorator for Explicit Method Overrides
4. PEP 684: Per-Interpreter GIL (Independent GIL per Subinterpreter)
5. Comprehension Inlining & Performance Optimizations
"""

from __future__ import annotations
import sys
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")

# --- 1. PEP 695: New Type Parameter Syntax ---
# In Python 3.12+:
# type Coordinate = tuple[float, float]
# type Matrix[T] = list[list[T]]
# def get_first[T](items: list[T]) -> T:
#     return items[0]
PEP695_CODE = """
type Vector[T] = list[T]

def get_head[T](collection: list[T]) -> T:
    return collection[0]
"""

if sys.version_info >= (3, 12):
    _local_312_scope: Dict[str, Any] = {}
    exec(PEP695_CODE, globals(), _local_312_scope)
    get_head = _local_312_scope["get_head"]
else:
    def get_head(collection: List[T]) -> T:
        """Pre-3.12 generic equivalent using TypeVar."""
        return collection[0]


# --- 2. PEP 698: typing.override Decorator ---
def _create_override_decorator() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    try:
        from typing import override  # Python 3.12+
        return override
    except ImportError:
        def override(method: Callable[..., Any]) -> Callable[..., Any]:
            """Polyfill for typing.override decorator."""
            setattr(method, "__override__", True)
            return method
        return override

override = _create_override_decorator()


class BaseWorker:
    def execute(self) -> str:
        return "base execution"


class CustomWorker(BaseWorker):
    @override
    def execute(self) -> str:
        """Explicitly marked as overriding BaseWorker.execute."""
        return "customized worker execution"


# --- 3. PEP 701: Formalized f-strings ---
# In Python 3.12+, inner expressions can reuse quotes and include backslashes directly:
# print(f"Joined: {'\n'.join(items)}")
def demonstrate_fstring_enhancements() -> str:
    if sys.version_info >= (3, 12):
        # Native Python 3.12 nested quote f-string
        return eval('f"Items: {\', \'.join([\\"alpha\\", \\"beta\\"])}"')
    else:
        # Pre-3.12 equivalent requiring separate variable or outer/inner quote juggling
        inner = ", ".join(["alpha", "beta"])
        return f"Items: {inner}"


def run_python_312_demos() -> None:
    """Execute all Python 3.12 feature demonstrations."""
    print("=== Python 3.12 Feature Demonstrations ===")

    # 1. PEP 695 Type Parameters
    print(f"1. PEP 695 Type Parameter Syntax (Native: {sys.version_info >= (3, 12)}):")
    data = ["core", "python", "mastery"]
    head = get_head(data)
    print(f"   get_head({data}) -> '{head}'")

    # 2. typing.override
    worker = CustomWorker()
    print(f"\n2. typing.override demo: {worker.execute()}")
    print(f"   Base worker response: {BaseWorker().execute()}")

    # 3. PEP 701 f-strings
    print(f"\n3. Formalized f-strings output: {demonstrate_fstring_enhancements()}")

    # 4. Per-Interpreter GIL
    print("\n4. PEP 684 Per-Interpreter GIL Summary:")
    print("   Allows embedding separate Python subinterpreters in C or via `_interpreters`,")
    print("   each possessing its own independent GIL for multi-core parallelism.")

    print("Python 3.12 demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_python_312_demos()
