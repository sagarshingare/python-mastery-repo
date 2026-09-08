"""
Metaclasses module for type creation customization and class construction hooks.
"""

from .metaclass_examples import (
    AttributeTrackerMeta,
    BaseTrackedModel,
    InterfaceEnforcerMeta,
    PluginRegistryBase,
    SingletonMeta,
)

__all__ = [
    "AttributeTrackerMeta",
    "BaseTrackedModel",
    "InterfaceEnforcerMeta",
    "PluginRegistryBase",
    "SingletonMeta",
]