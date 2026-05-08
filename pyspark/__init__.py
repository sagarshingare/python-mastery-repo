"""PySpark package wrapper.

This package preserves local PySpark learning content while delegating runtime
access to the installed pyspark library.
"""

from __future__ import annotations

import importlib.util
import site
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

_external_module_name = "_external_pyspark"
_external_pyspark: ModuleType | None = None


def _load_external_pyspark() -> ModuleType | None:
    global _external_pyspark
    if _external_pyspark is not None:
        return _external_pyspark

    for base in site.getsitepackages() + [site.getusersitepackages()]:
        path = Path(base) / "pyspark"
        if path.exists():
            spec = importlib.util.spec_from_file_location("pyspark", path / "__init__.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                original_pyspark = sys.modules.get("pyspark")
                sys.modules["pyspark"] = module
                root_dir = str(Path(__file__).resolve().parent.parent)
                original_sys_path = sys.path.copy()
                sys.path = [entry for entry in sys.path if entry not in (root_dir, "", ".")]
                try:
                    spec.loader.exec_module(module)
                finally:
                    sys.path = original_sys_path
                    if original_pyspark is not None:
                        sys.modules["pyspark"] = original_pyspark
                    else:
                        sys.modules.pop("pyspark", None)
                _external_pyspark = module
                return _external_pyspark
    return None


_load_external_pyspark()


def __getattr__(name: str) -> Any:
    if _external_pyspark is not None:
        return getattr(_external_pyspark, name)
    raise AttributeError(name)


def __dir__() -> list[str]:
    names = set(globals().keys())
    if _external_pyspark is not None:
        names |= {item for item in dir(_external_pyspark) if not item.startswith("_")}
    return sorted(names)
