"""NumPy Mastery Package: Arrays, Broadcasting, Vectorization, and Optimization."""

from __future__ import annotations

from typing import Any
import numpy as _real_numpy

from . import arrays
from . import broadcasting
from . import optimization
from . import vectorization

__all__ = [
    "arrays",
    "broadcasting",
    "vectorization",
    "optimization",
]


def __getattr__(name: str) -> Any:
    return getattr(_real_numpy, name)


def __dir__() -> list[str]:
    names = set(globals().keys())
    names |= {item for item in dir(_real_numpy) if not item.startswith("_")}
    return sorted(names)
