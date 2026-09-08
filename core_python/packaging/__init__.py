"""
Python packaging module for build systems, metadata, and distribution patterns.
"""

from .packaging_guide import (
    BuildSystem,
    ConsoleScript,
    DistributionType,
    PackageLayout,
    PackageMetadata,
    render_pyproject_toml,
    render_setup_py,
    validate_package_layout,
)

__all__ = [
    "BuildSystem",
    "ConsoleScript",
    "DistributionType",
    "PackageLayout",
    "PackageMetadata",
    "render_pyproject_toml",
    "render_setup_py",
    "validate_package_layout",
]
