"""Statistics package wrapper.

This package serves learning content while delegating attribute access to the
standard library statistics module.
"""

from __future__ import annotations

import importlib.util
import sys
import sysconfig
from pathlib import Path
from types import ModuleType
from typing import Any

_external_module_name = "_external_statistics"
_external_statistics: ModuleType | None = None


def _load_external_statistics() -> ModuleType | None:
    global _external_statistics
    if _external_statistics is not None:
        return _external_statistics

    stdlib_path = Path(sysconfig.get_paths()["stdlib"]) / "statistics.py"
    if stdlib_path.exists():
        spec = importlib.util.spec_from_file_location(_external_module_name, stdlib_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[_external_module_name] = module
            spec.loader.exec_module(module)
            _external_statistics = module
            return _external_statistics
    return None


_load_external_statistics()


def __getattr__(name: str) -> Any:
    if _external_statistics is not None:
        return getattr(_external_statistics, name)
    raise AttributeError(name)


def __dir__() -> list[str]:
    names = set(globals().keys())
    if _external_statistics is not None:
        names |= {item for item in dir(_external_statistics) if not item.startswith("_")}
    return sorted(names)
