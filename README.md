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

## Learning Path & Curriculum

Follow the structured 11-stage learning sequence designed to take you from core Python foundations to advanced distributed computing and microservices:

> 📘 **Full Curriculum Guide**: See [**`LEARNING_PATH.md`**](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md) for the complete roadmap, module details, and prerequisites.

| Stage | Sequence | Directory | Description |
|:---:|:---|:---|:---|
| **01** | **Core Python** | [`core_python/`](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python) | Fundamentals, OOP, Iterators, Generators, Typing, Concurrency |
| **02** | **DSA** | [`dsa/`](file:///Users/sagarshingare/Documents/python-mastery-repo/dsa) | Data structures & algorithms (Arrays to System Design DSA) |
| **03** | **LeetCode** | [`leetcode/`](file:///Users/sagarshingare/Documents/python-mastery-repo/leetcode) | Algorithmic interview problem practice & CLI runner |
| **04** | **SQL** | [`sql/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql) | Fundamentals, Joins, Window Functions, CTEs, Optimization |
| **05** | **Data Analytics** | [`numpy_lib/`](file:///Users/sagarshingare/Documents/python-mastery-repo/numpy_lib), [`pandas_lib/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib), [`statistics/`](file:///Users/sagarshingare/Documents/python-mastery-repo/statistics) | Numerical arrays, DataFrame transformations, Statistics |
| **06** | **Big Data** | [`pyspark/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pyspark) | Apache Spark, DataFrames, Transformations & Actions |
| **07** | **Testing** | [`testing/`](file:///Users/sagarshingare/Documents/python-mastery-repo/testing) | Pytest, Mocking, In-memory DB Fixtures, Micro-benchmarking |
| **08** | **API Development** | [`api_development/`](file:///Users/sagarshingare/Documents/python-mastery-repo/api_development) | FastAPI, Flask, JWT, Rate Limiting, Production Observability |
| **09** | **Cloud** | [`cloud/`](file:///Users/sagarshingare/Documents/python-mastery-repo/cloud) | AWS, Azure, Databricks Lakehouse, Snowflake |
| **10** | **Projects** | [`projects/`](file:///Users/sagarshingare/Documents/python-mastery-repo/projects) | Production batch ETL pipelines, Customer 360, Streaming |
| **11** | **Interview & Docs**| [`interview_prep/`](file:///Users/sagarshingare/Documents/python-mastery-repo/interview_prep), [`docs/`](file:///Users/sagarshingare/Documents/python-mastery-repo/docs) | Architecture diagrams, cheatsheets, system design prep |

## Getting started

1. Clone the repository:

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

5. Run full repository validation:

```bash
make check
```

6. Launch the example API service:

```bash
make run-api
```

## Run learning modules

The repository is designed for hands-on learning. Each module includes a `README.md` with specific examples, and many contain a CLI runner.

### Core Python basics

Run the examples as a Python package so imports resolve correctly:

```bash
python -m core_python.basics.examples --module all
```

Run a single basics module:

```bash
python -m core_python.basics.examples --module control_flow
```

### Standardized module entry points

Many training modules now support a standardized alias format via `examples.py` in each package. That means major example packages can be launched with:

```bash
python -m core_python.oops.examples
python -m pyspark.basics.examples
```

The `leetcode` package continues to use the problem runner directly:

```bash
python -m leetcode.run_problems list
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

A top-level architecture diagram is available in `docs/diagrams/repo_architecture.md` for a quick visual map of the repo.

### Repository hierarchy

```text
python-mastery-repo/
├── api_development/            # FastAPI and Flask API examples, auth, rate limiting, production patterns
├── cloud/                      # Cloud provider guides and architecture for AWS, Azure, Databricks, Snowflake
├── core_python/                # Python fundamentals and advanced language topics
│   ├── basics/
│   ├── advanced_patterns/
│   ├── async_programming/
│   ├── decorators/
│   ├── generators/
│   ├── iterators/
│   ├── metaclasses/
│   └── typing/
├── docs/                       # Architecture diagrams, best practices, cheatsheets, interview notes
├── dsa/                        # Data structures and algorithms by category
├── interview_prep/             # Behavioral and technical interview preparation content
├── leetcode/                    # Algorithm practice by difficulty, solution registry, CLI runner
│   ├── easy/
│   ├── medium/
│   ├── hard/
│   └── run_problems.py
├── numpy_lib/                  # NumPy tutorials, vectorization, arrays, optimization
├── pandas_lib/                 # pandas examples and wrapper package to avoid name collision
│   ├── basics/
│   ├── groupby/
│   └── joins/
├── projects/                   # End-to-end projects and production-style pipelines
├── pyspark/                    # Spark and Big Data examples, SQL, streaming, transformations
├── sql/                        # SQL query patterns, joins, window functions, optimization
├── statistics/                 # Practical statistics and hypothesis testing examples
├── testing/                    # Pytest-based validation and repository test suite
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── pyproject.toml
└── setup.py
```

### Notes on package naming

- `pandas_lib/` is intentionally separate from the installed `pandas` package so local examples do not shadow the real library.
- The repo uses repeated module entry points like `README.md`, `__init__.py`, `run_examples.py`, and `solutions.py` in package folders. This is normal for modular training content, but you can standardize naming further if desired.

## Contributing

See `CONTRIBUTING.md` for contribution guidelines, branch strategy, and commit message conventions.
