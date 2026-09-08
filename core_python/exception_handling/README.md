# Core Python: Exception Handling

> **Learning Path**: [Stage 01: Core Python Mastery](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-01-core-python-mastery) ▸ **Step 1.7: Exception Handling**

This module provides a comprehensive guide to exception handling in Python, covering fundamental concepts, advanced techniques, and best practices.

## Introduction

Exception handling is a critical aspect of writing robust and reliable Python code. This module explores how to handle errors gracefully, create custom exception types, and use context managers for resource management.

## Module Structure

The module is organized into the following components:

-   `custom_exceptions.py`: Defines custom exception classes like `ValidationError` and `ResourceUnavailableError` to represent specific error conditions in your domain.
-   `handling_strategies.py`: Contains functions that implement various error handling patterns, such as `safe_execute`, which prevents exceptions from crashing the application.
-   `context_managers.py`: Includes context managers like `SuppressAndLog` that provide a clean and reusable way to manage resources and handle exceptions within a specific context.
-   `best_practices.py`: A collection of functions that illustrate both good and bad practices in exception handling, serving as a learning tool for writing better code.
-   `run_examples.py`: A command-line interface (CLI) to demonstrate the concepts and code in action.

## Running the Examples

To see the exception handling examples in action, run the `run_examples.py` script from the root of the repository. This script provides a CLI to execute different sets of examples.

You can run all examples at once or choose a specific set.

```bash
# Run all examples
python -m core_python.exception_handling.run_examples all

# Run only the handling strategies examples
python -m core_python.exception_handling.run_examples strategies

# Run only the context manager examples
python -m core_python.exception_handling.run_examples contexts

# Run only the best practices examples
python -m core_python.exception_handling.run_examples practices
```

### Example Output

Running the `strategies` examples will produce output like this:

```
--- Running Handling Strategies Examples ---

[safe_execute]
2026-06-23 15:30:00 - ERROR - safe_execute failed for <lambda>
safe_execute handled ZeroDivisionError, result: Division failed

[validate_input]
Caught expected validation error: string value cannot be empty

[guard_against_resource_failure]
Caught expected resource error: Resource 'Database' is unavailable
```
