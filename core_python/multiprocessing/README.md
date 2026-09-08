# Multiprocessing

> **Learning Path**: [Stage 01: Core Python Mastery](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-01-core-python-mastery) ▸ **Step 1.14: Concurrency: Multiprocessing**

CPU-bound parallelism using Python's `multiprocessing` module and `concurrent.futures`.

## Topics covered

- `ProcessPoolExecutor` for parallel task execution
- Shared state with `multiprocessing.Value` and `Lock`
- `parallel_map` utility for distributing work across processes
- Prime counting as a CPU-bound benchmark

## Run examples

```bash
python -m core_python.multiprocessing.run_examples
python -m core_python.multiprocessing.run_examples --module primes
python -m core_python.multiprocessing.run_examples --module parallel_map
python -m core_python.multiprocessing.run_examples --module shared_counter
```
