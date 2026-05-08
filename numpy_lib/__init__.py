"""NumPy mastery package wrapper.

This package namespace holds learning content and also delegates attribute access
for the installed NumPy library.
"""

from __future__ import annotations

import importlib.util
import site
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

_external_module_name = "_external_numpy"
_external_numpy: ModuleType | None = None


def _load_external_numpy() -> ModuleType | None:
    global _external_numpy
    if _external_numpy is not None:
        return _external_numpy

    for base in site.getsitepackages() + [site.getusersitepackages()]:
        path = Path(base) / "numpy"
        if path.exists():
            spec = importlib.util.spec_from_file_location("numpy", path / "__init__.py")
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                original_numpy = sys.modules.get("numpy")
                sys.modules["numpy"] = module
                root_dir = str(Path(__file__).resolve().parent.parent)
                original_sys_path = sys.path.copy()
                sys.path = [entry for entry in sys.path if entry not in (root_dir, "", ".")]
                try:
                    spec.loader.exec_module(module)
                finally:
                    sys.path = original_sys_path
                    if original_numpy is not None:
                        sys.modules["numpy"] = original_numpy
                    else:
                        sys.modules.pop("numpy", None)
                _external_numpy = module
                return _external_numpy
    return None


_load_external_numpy()


def __getattr__(name: str) -> Any:
    if _external_numpy is not None:
        return getattr(_external_numpy, name)
    raise AttributeError(name)


def __dir__() -> list[str]:
    names = set(globals().keys())
    if _external_numpy is not None:
        names |= {item for item in dir(_external_numpy) if not item.startswith("_")}
    return sorted(names)
