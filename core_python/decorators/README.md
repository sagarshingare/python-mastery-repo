# Python Decorators

This folder contains examples of Python decorators for function instrumentation, caching, validation, and error handling.

## Included topics

- `decorators.py` - timer, retry, memoize, and validation decorators

## Python version

This module is written for Python 3.10+ and uses modern type hints and decorator patterns.

## Learning outcomes

- Understand how decorators work and their use cases
- Implement timing, retry, and caching decorators
- Apply validation decorators for input checking
- Use decorators for cross-cutting concerns

## Usage

Import the decorators from `core_python.decorators` and apply them to your functions.

Example:

```python
from core_python.decorators.decorators import timer, retry

@timer
@retry(max_attempts=3)
def my_function():
    # Your code here
    pass
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each decorator.

Run the examples as a Python package:

```bash
python -m core_python.decorators.run_examples --module timer
python -m core_python.decorators.run_examples --module retry
python -m core_python.decorators.run_examples --module memoize
python -m core_python.decorators.run_examples --module validate
```