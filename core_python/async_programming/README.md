# Async Programming

This folder contains comprehensive examples of asynchronous programming in Python using asyncio.

## Included topics

- `async_basics.py` - fundamental async/await patterns, basic coroutines, and sequential vs concurrent execution
- `async_tasks.py` - asyncio Task creation, management, cancellation, and exception handling
- `async_concurrency.py` - producer-consumer patterns, semaphore-based limiting, and concurrent data processing
- `event_loops.py` - event loop lifecycle management, executor integration, and sync-async bridging

## Python version

This module is written for Python 3.10+ and uses modern asyncio features available in Python 3.10 and later.

## Learning outcomes

- Understand async/await syntax and coroutine execution
- Create and manage asyncio Tasks for concurrent operations
- Implement producer-consumer patterns with asyncio.Queue
- Use semaphores and other synchronization primitives
- Manage event loop lifecycle and integrate with synchronous code
- Handle exceptions and cancellation in async contexts

## Usage

Import the core modules directly from `core_python.async_programming` and use the async functions in your application.

Example:

```python
import asyncio
from core_python.async_programming.async_basics import async_delayed_greeting

async def main():
    greeting = await async_delayed_greeting("Alice", 0.5)
    print(greeting)

asyncio.run(main())
```

## Run examples interactively

This package includes a CLI example runner that demonstrates each async programming concept module.

Run the examples as a Python package so the package imports resolve correctly:

```bash
python -m core_python.async_programming.run_examples --module basics
python -m core_python.async_programming.run_examples --module tasks
python -m core_python.async_programming.run_examples --module concurrency
python -m core_python.async_programming.run_examples --module loops
python -m core_python.async_programming.run_examples --module sync
python -m core_python.async_programming.run_examples --module all
```

## Key concepts covered

### Async Basics
- Defining async functions with `async def`
- Using `await` for asynchronous operations
- Sequential vs concurrent execution patterns
- Basic event loop usage

### Task Management
- Creating tasks with `asyncio.create_task()`
- Using `asyncio.gather()` for concurrent execution
- Task cancellation and timeout handling
- Exception handling in concurrent tasks

### Concurrency Patterns
- Producer-consumer pattern with `asyncio.Queue`
- Resource limiting with `asyncio.Semaphore`
- Async context managers for resource management
- Concurrent data processing with error handling

### Event Loop Management
- Running async code from synchronous contexts
- Using executors for blocking operations
- Event loop lifecycle management
- Thread-based async execution