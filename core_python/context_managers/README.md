# Python Context Managers

This folder contains examples of context managers for safe resource handling in Python.

## Included topics

- `resource_contexts.py` - custom context managers for file handling and directory changes

## Python version

This module is written for Python 3.10+ and uses modern context manager patterns.

## Learning outcomes

- Understand context managers and the with statement
- Implement custom context managers using classes and decorators
- Use context managers for resource cleanup
- Apply context managers for temporary state changes

## Usage

Import the context managers from `core_python.context_managers` and use them with the with statement.

Example:

```python
from core_python.context_managers.resource_contexts import change_directory

with change_directory("/tmp"):
    # Code runs in /tmp directory
    pass
# Back to original directory
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each context manager.

Run the examples as a Python package:

```bash
python -m core_python.context_managers.run_examples --module change_directory
python -m core_python.context_managers.run_examples --module file_open
```