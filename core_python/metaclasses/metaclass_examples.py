"""Examples of metaclass usage and type customization in Python."""

from __future__ import annotations

from typing import Any, Dict, Type


class AttributeTrackerMeta(type):
    """A metaclass that tracks class attribute definitions."""

    def __new__(mcs: Type[type], name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        namespace["_tracked_attributes"] = [key for key in namespace if not key.startswith("__")]
        return super().__new__(mcs, name, bases, namespace)


class Base tracked metaclass: # noqa: E999
    """A base class that uses AttributeTrackerMeta."""

    pass
