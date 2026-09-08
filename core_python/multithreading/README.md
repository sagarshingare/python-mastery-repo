# Multithreading

> **Learning Path**: [Stage 01: Core Python Mastery](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-01-core-python-mastery) ▸ **Step 1.13: Concurrency: Multithreading**

I/O-bound concurrency using Python's `threading` module and `concurrent.futures`.

## Topics covered

- Thread-safe counter with `threading.Lock`
- Producer-consumer pattern with `queue.Queue`
- `ThreadPoolExecutor` for concurrent I/O tasks
- Read-write lock for concurrent read / exclusive write access

## Run examples

```bash
python -m core_python.multithreading.run_examples
python -m core_python.multithreading.run_examples --module counter
python -m core_python.multithreading.run_examples --module producer_consumer
python -m core_python.multithreading.run_examples --module io_tasks
```
