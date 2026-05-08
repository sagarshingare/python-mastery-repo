# Python Basics

This folder contains foundational Python examples and concepts for developers who are building strong engineering fundamentals.

## Included topics

- `variables.py` - arithmetic, validation, and defensive programming
- `data_types.py` - parsing primitive values, datetime handling, and string normalization
- `control_flow.py` - conditionals, loops, comprehensions, and branching
- `functions.py` - function design, default arguments, variadic arguments, memoization
- `collections.py` - list, tuple, set, frozenset, dict, OrderedDict, Counter, ChainMap, deque, defaultdict, namedtuple, and UserDict patterns
- `file_io.py` - JSON and CSV input/output utilities
- `modules_packages.py` - dynamic imports and package mechanics
- `debugging_logging.py` - logger setup and diagnostic logging patterns

## Python version

This module is written for Python 3.10+ and uses modern type hints, pattern matching, and collection features available in Python 3.10 and later.

## Learning outcomes

- Understand Python types and control structures
- Write reusable, modular functions
- Apply collection utilities in real-world scenarios
- Read and write structured files safely
- Use logging and debugging conventions
- Work with modules and dynamic imports

## Usage

Import the core modules directly from `core_python.basics` and use the functions in your application or tests.

Example:

```python
from core_python.basics.control_flow import categorize_scores

categories = categorize_scores([92, 85, 73, 59])
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each basic concept module.

Run the examples as a Python package so the package imports resolve correctly:

```bash
python -m core_python.basics.run_examples --module variables
python -m core_python.basics.run_examples --module control_flow
python -m core_python.basics.run_examples --module functions
python -m core_python.basics.run_examples --module data_types
python -m core_python.basics.run_examples --module collections
python -m core_python.basics.run_examples --module file_io
python -m core_python.basics.run_examples --module logging
python -m core_python.basics.run_examples --module all
```

Each command prints sample output and shows how the functions behave in a real scenario.
