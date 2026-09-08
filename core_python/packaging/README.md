# Packaging

> **Learning Path**: [Stage 01: Core Python Mastery](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-01-core-python-mastery) ▸ **Step 1.16: Packaging & Distribution**

Reference guide for Python package structure, metadata, and distribution.

## Topics covered

- `pyproject.toml` configuration (PEP 621)
- Legacy `setup.py` patterns
- `src/` layout vs flat layout
- Build systems: setuptools, flit, poetry, hatch, pdm
- Entry points and console scripts
- Versioning best practices

## Key classes

- `PackageMetadata` — structured representation of project metadata
- `PackageLayout` — directory layout helper
- `render_pyproject_toml()` — generate `pyproject.toml` from metadata
- `render_setup_py()` — generate legacy `setup.py` from metadata
