# Typing

> **Learning Path**: [Stage 01: Core Python Mastery](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-01-core-python-mastery) ▸ **Step 1.8: Modern Static Typing**

Modern Python type annotation examples covering the full `typing` module.

## Topics covered

- **Generics** — `TypeVar`, `Generic`, multi-parameter generics
- **Protocols** — structural subtyping, `@runtime_checkable`
- **TypedDict** — typed dictionaries with required/optional fields
- **Literal** — restricting values at type-check time
- **NewType** — domain-specific type aliases
- **Overloads** — `@overload` for type-narrowing
- **NamedTuple** — immutable typed tuples
- **Result pattern** — generic `Result[T]` monad

## Run examples

```bash
python -m core_python.typing.run_examples
python -m core_python.typing.run_examples --module generics
python -m core_python.typing.run_examples --module protocols
```
