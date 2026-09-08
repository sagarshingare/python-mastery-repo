"""
Examples of metaclass usage, type customization, and __init_subclass__ in Python.
================================================================================
Covers:
- `AttributeTrackerMeta`: Inspecting and tracking class attributes at definition time
- `SingletonMeta`: Thread-safe singleton creation via metaclass `__call__`
- `InterfaceEnforcerMeta`: Contract and abstract method enforcement
- `PluginBase` with `__init_subclass__`: Modern Python 3.6+ lightweight alternative to metaclasses
"""

from __future__ import annotations
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, Tuple, Type


# --- 1. Attribute Tracking Metaclass ---

class AttributeTrackerMeta(type):
    """A metaclass that inspects and records defined class attributes."""

    def __new__(mcs: Type[type], name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        namespace["_tracked_attributes"] = [key for key in namespace if not key.startswith("__")]
        return super().__new__(mcs, name, bases, namespace)


class BaseTrackedModel(metaclass=AttributeTrackerMeta):
    """Base class utilizing AttributeTrackerMeta."""
    pass


# --- 2. Singleton Metaclass ---

class SingletonMeta(type):
    """Metaclass that enforces a single shared instance per class."""

    _instances: ClassVar[Dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def clear_instances(mcs) -> None:
        """Utility for test suites to reset singleton instances."""
        mcs._instances.clear()


# --- 3. Interface Enforcement Metaclass ---

class InterfaceEnforcerMeta(type):
    """Metaclass ensuring subclasses implement required contract methods."""

    required_methods: ClassVar[List[str]] = []

    def __new__(mcs: Type[type], name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # Skip abstract base itself
            for method in mcs.required_methods:
                if method not in namespace or not callable(namespace[method]):
                    raise TypeError(f"Class '{name}' must implement required method '{method}()'")
        return cls


# --- 4. Modern Alternative: PEP 487 __init_subclass__ ---

class PluginRegistryBase:
    """Modern base class using __init_subclass__ instead of a custom metaclass.

    Avoids metaclass conflicts while allowing automatic registration and validation.
    """

    _registry: ClassVar[Dict[str, Type[PluginRegistryBase]]] = {}
    plugin_name: ClassVar[str] = ""

    def __init_subclass__(cls, plugin_name: Optional[str] = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower().removesuffix("plugin")
        cls.plugin_name = name
        cls._registry[name] = cls

    @classmethod
    def get_plugin(cls, name: str) -> Optional[Type[PluginRegistryBase]]:
        return cls._registry.get(name)

    @classmethod
    def list_plugins(cls) -> List[str]:
        return list(cls._registry.keys())
