# Python Advanced Patterns

This folder contains examples of advanced programming patterns and design patterns in Python.

## Included topics

- `design_patterns.py` - singleton, factory, observer, strategy, and decorator patterns

## Python version

This module is written for Python 3.10+ and uses modern Python features including protocols and metaclasses.

## Learning outcomes

- Understand common design patterns and their implementation
- Apply patterns for better code organization
- Use metaclasses for advanced class behavior
- Implement observer and strategy patterns
- Create extensible code with factory and decorator patterns

## Usage

Import the pattern implementations from `core_python.advanced_patterns` and use them in your applications.

Example:

```python
from core_python.advanced_patterns.design_patterns import ShapeFactory

circle = ShapeFactory.create_shape("circle", radius=5.0)
print(circle.area())
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each pattern.

Run the examples as a Python package:

```bash
python -m core_python.advanced_patterns.run_examples --module singleton
python -m core_python.advanced_patterns.run_examples --module factory
python -m core_python.advanced_patterns.run_examples --module observer
python -m core_python.advanced_patterns.run_examples --module strategy
python -m core_python.advanced_patterns.run_examples --module decorator
```