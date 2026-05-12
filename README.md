# Python Mastery Repository

A production-grade, enterprise-ready repository for Python mastery. This repository is designed to help developers progress from beginner to advanced through hands-on examples, architecture guidance, interview preparation, and real-world projects.

**Python Version**: 3.9+

## What’s included

- **Core Python foundation** - Variables, data types, control flow, functions, collections, file I/O, modules, debugging, and logging
- **Advanced Python concepts** - Decorators, OOP (classes, inheritance, polymorphism, abstraction), generators, iterators, context managers, metaclasses, memory management, multiprocessing, multithreading, async programming, exception handling, packaging, and typing
- **Design patterns** - Singleton, factory, observer, strategy, and decorator patterns
- Data structures and algorithms
- LeetCode-style practice
- Pandas and NumPy mastery
- Statistics for data engineering and data science
- PySpark and big data workflows
- SQL query patterns and optimization
- API development with FastAPI
- Production engineering best practices
- Docker, CI/CD, and monitoring
- Interview notes and architectural guidance

## Getting started

1. Clone the repository:
ð
```bash
git clone <repo-url>
cd python-mastery-repo
```

2. Create and activate your virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the Python path for module imports:

```bash
export PYTHONPATH=$(pwd)  # Add this to your shell profile for persistence
```

4. Run core tests:

```bash
make test
```

5. Launch the example API service:

```bash
make run-api
```

## Run learning modules

The repository is designed for hands-on learning. Each module includes a `README.md` with specific examples, and many contain a CLI runner.

### Core Python basics

Run the examples as a Python package so imports resolve correctly:

```bash
python -m core_python.basics.run_examples --module all
```

Run a single basics module:

```bash
python -m core_python.basics.run_examples --module control_flow
```

### Advanced Python modules

Each advanced module includes interactive examples:

```bash
# Decorators
python -m core_python.decorators.run_examples --module timer

# Object-oriented programming
python -m core_python.oops.run_examples --module classes_basics

# Generators
python -m core_python.generators.run_examples --module fibonacci

# Design patterns
python -m core_python.advanced_patterns.run_examples --module singleton

# Context managers
python -m core_python.context_managers.run_examples --module change_directory

# Async programming
python -m core_python.async_programming.run_examples --module basics

# And more... check each module's README.md for available options
```

### Projects

Run the sample batch ETL pipeline:

```bash
python projects/batch_etl_pipeline/etl.py --config projects/batch_etl_pipeline/config.yaml
```

### Test and verify

Run only Python basics tests:

```bash
python -m pytest testing/pytest/test_python_basics.py -q
```

Run all repository tests:

```bash
python -m pytest -q
```

## Repository structure

The repo is organized as a learning and engineering workspace with modular packages, example pipelines, infrastructure configuration, and interview-focused content.

## Contributing

See `CONTRIBUTING.md` for contribution guidelines, branch strategy, and commit message conventions.
