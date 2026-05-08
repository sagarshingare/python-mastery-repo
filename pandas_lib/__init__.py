"""Pandas mastery package wrapper.

This package namespace contains learning examples and also delegates attribute access
for the real pandas library to avoid shadowing the installed package.
"""

from __future__ import annotations

import importlib.util
import site
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

_external_module_name = "_external_pandas"
_external_pandas: ModuleType | None = None


def _load_external_pandas() -> ModuleType | None:
    global _external_pandas
    if _external_pandas is not None:
        return _external_pandas

    for base in site.getsitepackages() + [site.getusersitepackages()]:
        path = Path(base) / "pandas"
        if path.exists():
            spec = importlib.util.spec_from_file_location("pandas", path / "__init__.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                original_pandas = sys.modules.get("pandas")
                sys.modules["pandas"] = module
                root_dir = str(Path(__file__).resolve().parent.parent)
                original_sys_path = sys.path.copy()
                sys.path = [entry for entry in sys.path if entry not in (root_dir, "", ".")]
                try:
                    spec.loader.exec_module(module)
                finally:
                    sys.path = original_sys_path
                    if original_pandas is not None:
                        sys.modules["pandas"] = original_pandas
                    else:
                        sys.modules.pop("pandas", None)
                _external_pandas = module
                return _external_pandas
    return None


_load_external_pandas()


def __getattr__(name: str) -> Any:
    if _external_pandas is not None:
        return getattr(_external_pandas, name)
    raise AttributeError(name)


def __dir__() -> list[str]:
    names = set(globals().keys())
    if _external_pandas is not None:
        names |= {item for item in dir(_external_pandas) if not item.startswith("_")}
    return sorted(names)
