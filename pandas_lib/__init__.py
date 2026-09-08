"""Pandas Mastery Package: Basics, GroupBy, Joins, Window Functions, and Optimization."""

from __future__ import annotations

from typing import Any
import pandas as _real_pandas

from . import basics
from . import groupby
from . import joins
from . import window_functions
from . import optimization

__all__ = [
    "basics",
    "groupby",
    "joins",
    "window_functions",
    "optimization",
]


def __getattr__(name: str) -> Any:
    return getattr(_real_pandas, name)


def __dir__() -> list[str]:
    names = set(globals().keys())
    names |= {item for item in dir(_real_pandas) if not item.startswith("_")}
    return sorted(names)
