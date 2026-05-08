# Python Generators

This folder contains examples of generator functions and lazy evaluation patterns in Python.

## Included topics

- `generator_examples.py` - fibonacci, chunked, filter, and string normalization generators

## Python version

This module is written for Python 3.10+ and uses modern generator syntax and type hints.

## Learning outcomes

- Understand generator functions and the yield keyword
- Implement lazy evaluation for memory efficiency
- Create streaming data processing pipelines
- Use generators for infinite sequences

## Usage

Import the generator functions from `core_python.generators` and use them in your code.

Example:

```python
from core_python.generators.generator_examples import fibonacci_generator

for num in fibonacci_generator(100):
    print(num)
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each generator concept.

Run the examples as a Python package:

```bash
python -m core_python.generators.run_examples --module fibonacci
python -m core_python.generators.run_examples --module chunked
python -m core_python.generators.run_examples --module filter
python -m core_python.generators.run_examples --module normalized
```