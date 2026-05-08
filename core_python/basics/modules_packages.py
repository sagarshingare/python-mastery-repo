"""Python module and package mechanics for import-time behavior.

This file contains production-focused utilities for dynamic import, module
introspection, path resolution, and safe loading of Python packages.

Python compatibility: 3.10+
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


def load_module_by_name(name: str) -> ModuleType:
    """Dynamically import a module by import path.

    Args:
        name: The fully qualified module name, such as "json" or "os.path".

    Returns:
        The loaded module object.

    Raises:
        ModuleNotFoundError: when the module cannot be imported.
    """
    return importlib.import_module(name)


def safe_import_module(name: str) -> ModuleType | None:
    """Import a module safely without raising if it is unavailable.

    This helper is useful when optional dependencies may not be installed.

    Args:
        name: The module name to import.

    Returns:
        The imported module or None if the import failed.
    """
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        return None


def is_module_installed(name: str) -> bool:
    """Check whether a Python module or package is available on sys.path."""
    return importlib.util.find_spec(name) is not None


def get_module_attribute(module_name: str, attribute_name: str) -> Any:
    """Return a named attribute from a module.

    Args:
        module_name: The module import path.
        attribute_name: The attribute name to retrieve.

    Returns:
        The requested value.

    Raises:
        AttributeError: When the module does not expose the attribute.
    """
    module = load_module_by_name(module_name)
    if not hasattr(module, attribute_name):
        raise AttributeError(f"{module_name} does not define {attribute_name}")
    return getattr(module, attribute_name)


def list_module_attributes(module_name: str, public_only: bool = True) -> list[str]:
    """List all attributes exposed by a module.

    Args:
        module_name: The target module name.
        public_only: If True, filter out private names that start with an underscore.

    Returns:
        A sorted list of attribute names for the module.
    """
    module = load_module_by_name(module_name)
    names = list(dir(module))
    if public_only:
        names = [name for name in names if not name.startswith("_")]
    return sorted(names)


def get_module_file_path(module_name: str) -> Path:
    """Return the resolved filesystem path of a loaded module."""
    module = load_module_by_name(module_name)
    module_file = getattr(module, "__file__", None)
    if module_file is None:
        raise ImportError(f"Module {module_name} does not have a file path")
    return Path(module_file).resolve()


def is_package(module_name: str) -> bool:
    """Return True when the name points to a Python package rather than a plain module."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None and spec.submodule_search_locations is not None


def reload_module(module: ModuleType) -> ModuleType:
    """Reload a module object to refresh its imported state."""
    return importlib.reload(module)


def import_module_from_path(path: Path, module_name: str | None = None) -> ModuleType:
    """Load a module directly from a filesystem path.

    This function supports importing both single-file modules and package directories.

    Args:
        path: Path to a .py file or a package directory containing __init__.py.
        module_name: Optional import name to assign to the loaded module.

    Returns:
        The loaded module object.

    Raises:
        FileNotFoundError: When the path does not exist.
        ImportError: When the path cannot be loaded as a module.
    """
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Unable to find module path: {path}")

    if path.is_dir():
        source_path = path / "__init__.py"
        if not source_path.exists():
            raise ImportError(f"Package directory {path} does not contain __init__.py")
        name = module_name or path.name
    else:
        source_path = path
        name = module_name or path.stem

    spec = importlib.util.spec_from_file_location(name, source_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create import spec for {source_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def get_module_version(module_name: str) -> str | None:
    """Return a module's version string when available."""
    module = safe_import_module(module_name)
    if module is None:
        return None
    return getattr(module, "__version__", None)
