# Python Object-Oriented Programming

This folder contains comprehensive examples of object-oriented programming concepts in Python.

## Included topics

- `classes_basics.py` - basic classes, encapsulation, properties
- `inheritance.py` - single and multiple inheritance, method overriding
- `polymorphism.py` - polymorphism, duck typing, operator overloading
- `abstraction.py` - abstract classes, interfaces, factory patterns

## Python version

This module is written for Python 3.10+ and uses modern OOP features including protocols and abstract base classes.

## Learning outcomes

- Understand class definition and instantiation
- Implement encapsulation with private attributes
- Use inheritance and method overriding
- Apply polymorphism and duck typing
- Design abstract interfaces and factory patterns

## Usage

Import the classes from `core_python.oops` and use them in your applications.

Example:

```python
from core_python.oops.classes_basics import BankAccount

account = BankAccount("John Doe", 1000.0)
account.deposit(500.0)
print(account.balance)
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each OOP concept.

Run the examples as a Python package:

```bash
python -m core_python.oops.run_examples --module classes_basics
python -m core_python.oops.run_examples --module inheritance
python -m core_python.oops.run_examples --module polymorphism
python -m core_python.oops.run_examples --module abstraction
```