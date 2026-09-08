"""Python packaging guide — reference examples for project structure and metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class BuildSystem(str, Enum):
    """Supported Python build systems."""

    SETUPTOOLS = "setuptools"
    FLIT = "flit"
    POETRY = "poetry"
    HATCH = "hatch"
    PDM = "pdm"


@dataclass(frozen=True)
class PackageMetadata:
    """Metadata for a Python package.

    This mirrors the fields found in a ``pyproject.toml`` ``[project]`` table.
    """

    name: str
    version: str
    description: str = ""
    author: str = ""
    author_email: str = ""
    license: str = "MIT"
    python_requires: str = ">=3.9"
    keywords: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)

    def to_pyproject_dict(self) -> dict[str, Any]:
        """Serialise metadata into a ``pyproject.toml``-compatible dict."""
        return {
            "project": {
                "name": self.name,
                "version": self.version,
                "description": self.description,
                "requires-python": self.python_requires,
                "license": {"text": self.license},
                "authors": [{"name": self.author, "email": self.author_email}],
                "keywords": self.keywords,
                "dependencies": self.dependencies,
            }
        }


@dataclass
class PackageLayout:
    """Represents the directory layout of a Python package.

    Attributes:
        root: The project root directory.
        src_layout: Whether the project uses a ``src/`` layout.
        package_name: Top-level importable package name.
    """

    root: Path
    src_layout: bool = True
    package_name: str = ""

    @property
    def package_dir(self) -> Path:
        """Return the path to the importable package directory."""
        if self.src_layout:
            return self.root / "src" / self.package_name
        return self.root / self.package_name

    def expected_files(self) -> list[Path]:
        """Return a list of files a minimal package should contain."""
        pkg = self.package_dir
        return [
            self.root / "pyproject.toml",
            self.root / "README.md",
            self.root / "LICENSE",
            pkg / "__init__.py",
        ]


PYPROJECT_TEMPLATE = '''\
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "{name}"
version = "{version}"
description = "{description}"
requires-python = ">={python_requires}"
license = {{text = "{license}"}}

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff",
    "mypy",
]

[tool.setuptools.packages.find]
where = ["src"]
'''


def render_pyproject_toml(metadata: PackageMetadata) -> str:
    """Render a ``pyproject.toml`` string from metadata."""
    return PYPROJECT_TEMPLATE.format(
        name=metadata.name,
        version=metadata.version,
        description=metadata.description,
        python_requires=metadata.python_requires.lstrip(">="),
        license=metadata.license,
    )


SETUP_PY_TEMPLATE = '''\
"""Legacy setup.py for backward compatibility."""

from setuptools import setup, find_packages

setup(
    name="{name}",
    version="{version}",
    description="{description}",
    author="{author}",
    author_email="{author_email}",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    python_requires="{python_requires}",
    install_requires={dependencies!r},
)
'''


def render_setup_py(metadata: PackageMetadata) -> str:
    """Render a legacy ``setup.py`` string from metadata."""
    return SETUP_PY_TEMPLATE.format(
        name=metadata.name,
        version=metadata.version,
        description=metadata.description,
        author=metadata.author,
        author_email=metadata.author_email,
        python_requires=metadata.python_requires,
        dependencies=metadata.dependencies,
    )


class DistributionType(str, Enum):
    """Types of Python package distributions."""
    SDIST = "sdist"      # Source archive (e.g. .tar.gz)
    WHEEL = "wheel"      # Built binary package (e.g. .whl)


@dataclass(frozen=True)
class ConsoleScript:
    """Represents a CLI command entrypoint mapped in [project.scripts]."""
    command_name: str
    target_module: str
    entry_function: str

    def to_toml_entry(self) -> str:
        return f'{self.command_name} = "{self.target_module}:{self.entry_function}"'


def validate_package_layout(layout: PackageLayout) -> dict[str, Any]:
    """Check existence of expected project files for a package."""
    status = {}
    for path in layout.expected_files():
        status[path.name] = path.exists()
    return status
