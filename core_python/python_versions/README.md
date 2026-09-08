# Modern Python Version Evolution (3.8 — 3.13)

[![Curriculum Stage](https://img.shields.io/badge/Stage%2001-Step%201.17%3A%20Python%20Versions-6366f1?style=for-the-badge&logo=python&logoColor=white)](../../LEARNING_PATH.md#step-117-python-versions)

A comprehensive guide to landmark language features, syntax evolution, typing enhancements, and runtime architecture from **Python 3.8 to Python 3.13**.

---

## 1. Quick Reference & Version Matrix

| Version | Release | Landmark Features | Typing & Stdlib | Performance & Runtime |
| :--- | :--- | :--- | :--- | :--- |
| **Python 3.8** | Oct 2019 | Walrus operator `:=`<br>Positional-only `/`<br>f-string `{x=}` | `TypedDict`, `Literal`, `Final`, `Protocol`<br>`math.prod`, `math.isqrt` | Parallel filesystem cache |
| **Python 3.9** | Oct 2020 | Dict merge `\|` & update `\|= `<br>`removeprefix()` / `removesuffix()` | PEP 585 built-in generics (`list[int]`)<br>`zoneinfo` (IANA timezones)<br>`graphlib.TopologicalSorter` | Fast method calls (`vectorcall`) |
| **Python 3.10** | Oct 2021 | Structural pattern matching (`match/case`)<br>Parenthesized context managers | PEP 604 type unions (`X \| Y`)<br>`zip(..., strict=True)`<br>`ParamSpec`, `TypeAlias` | Precise error locations |
| **Python 3.11** | Oct 2022 | Exception groups (`ExceptionGroup`, `except*`)<br>Exception notes (`add_note()`) | `typing.Self`, `TypeVarTuple`<br>`tomllib` (standard TOML)<br>`asyncio.TaskGroup` | **Faster CPython**: Specializing Adaptive Interpreter (10-60% faster) |
| **Python 3.12** | Oct 2023 | Formalized f-strings (PEP 701)<br>Nested quotes & backslashes | PEP 695 type parameter syntax (`type X = ...`, `def f[T]()`)<br>`typing.override` | PEP 684 Per-Interpreter GIL<br>Inlined comprehensions |
| **Python 3.13** | Oct 2024 | PEP 703 Free-Threaded CPython (No-GIL build)<br>Tier 2 copy-and-patch JIT | PEP 742 `typing.TypeIs`<br>PEP 702 `@warnings.deprecated` | PyPy-based interactive REPL<br>Mimalloc memory allocator |

---

## 2. Deep Dive by Version

### Python 3.8
- **Walrus Operator (`:=`)**: Enables assignment expressions inside conditionals, loops, and comprehensions:
  ```python
  if (n := len(data)) > 100:
      print(f"Large payload with {n} items")
  ```
- **Positional-Only Parameters (`/`)**: Prevents callers from binding to internal parameter names:
  ```python
  def calculate(amount, rate, /, currency="USD", *, tax=0.0):
      ...
  ```
- **f-string Debugging**: Convenient syntax for logging expressions and their evaluated values:
  ```python
  print(f"{user_id=}, {status=}")
  ```

### Python 3.9
- **Dictionary Merge (`|`) & Update (`|=`)**:
  ```python
  combined = default_config | user_overrides
  ```
- **Prefix / Suffix Stripping**:
  ```python
  clean = "tbl_orders_temp".removeprefix("tbl_").removesuffix("_temp")
  ```
- **Built-in Generics (PEP 585)**: Deprecates `from typing import List, Dict` in favor of standard collections:
  ```python
  def process_batch(items: list[dict[str, int]]) -> set[str]:
      ...
  ```
- **`graphlib.TopologicalSorter`**: Standard DAG dependency resolver for pipelines and build systems.

### Python 3.10
- **Structural Pattern Matching (`match / case`)**:
  ```python
  match event:
      case {"type": "click", "x": int(x), "y": int(y)}:
          handle_click(x, y)
      case {"type": "error", "code": int(c)} if c >= 500:
          handle_server_error(c)
      case [command, *args]:
          dispatch_cli(command, args)
      case _:
          handle_unknown()
  ```
- **Type Union Operator (`|`)**: Replaces verbose `Union[int, str]` with `int | str`.
- **`zip(..., strict=True)`**: Raises `ValueError` if iterables differ in length.

### Python 3.11
- **Exception Groups & `except*`**:
  ```python
  try:
      fetch_all_endpoints()
  except* ConnectionError as eg:
      log_network_issue(eg)
  except* ValueError as eg:
      log_payload_issue(eg)
  ```
- **`add_note()`**: Diagnostic context appended to exceptions without rewrapping or changing type.
- **`asyncio.TaskGroup`**: First-class structured concurrency.
- **`tomllib`**: Fast, secure, read-only TOML parser directly in the standard library.

### Python 3.12
- **PEP 695 Type Parameter Syntax**: Clean generic declarations without `TypeVar` boilerplate:
  ```python
  type Matrix[T] = list[list[T]]

  def first_element[T](items: list[T]) -> T:
      return items[0]
  ```
- **PEP 701 f-strings**: Nested quotation marks, comments, and escaped characters within interpolation expressions:
  ```python
  print(f"Summary: {', '.join([f'{k}={v}' for k, v in metrics.items()])}")
  ```
- **`typing.override`**: Verified override decorator preventing silent refactor breakage.

### Python 3.13
- **PEP 703 Free-Threaded CPython (No-GIL)**: An experimental build option disabling the Global Interpreter Lock, enabling CPU-bound multithreading across multiple physical CPU cores.
- **Copy-and-Patch JIT**: Tier 2 bytecode execution compiler emitting native instructions for hot loops.
- **`typing.TypeIs`**: Bidirectional type guard narrowing both truthy and falsy branches.
- **`@warnings.deprecated`**: Standardized deprecation metadata for static type checkers and IDEs.

---

## 3. Running Feature Demos

Run the version matrix and interactive suite:

```bash
# Display capability matrix and run demonstrations
python3 -m core_python.python_versions.run_examples

# Or run individual version modules
python3 core_python/python_versions/python_38.py
python3 core_python/python_versions/python_39.py
python3 core_python/python_versions/python_310.py
python3 core_python/python_versions/python_311.py
python3 core_python/python_versions/python_312.py
python3 core_python/python_versions/python_313.py
```
