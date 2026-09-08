"""
Python Version Evolution Interactive Runner
===========================================
Executes feature demonstrations across Python 3.8 to 3.13.
"""

from __future__ import annotations
import sys
from .version_matrix import print_capability_report
from .python_38 import run_python_38_demos
from .python_39 import run_python_39_demos
from .python_310 import run_python_310_demos
from .python_311 import run_python_311_demos
from .python_312 import run_python_312_demos
from .python_313 import run_python_313_demos


def run_all_version_demos() -> None:
    """Run capability matrix report and all version demonstrations sequentially."""
    print("\n" + "#" * 80)
    print(" PYTHON VERSION EVOLUTION SUITE (Python 3.8 - 3.13)")
    print("#" * 80 + "\n")

    print_capability_report()

    print("\n--- [1/6] Running Python 3.8 Feature Demos ---")
    run_python_38_demos()

    print("\n--- [2/6] Running Python 3.9 Feature Demos ---")
    run_python_39_demos()

    print("\n--- [3/6] Running Python 3.10 Feature Demos ---")
    run_python_310_demos()

    print("\n--- [4/6] Running Python 3.11 Feature Demos ---")
    run_python_311_demos()

    print("\n--- [5/6] Running Python 3.12 Feature Demos ---")
    run_python_312_demos()

    print("\n--- [6/6] Running Python 3.13 Feature Demos ---")
    run_python_313_demos()

    print("#" * 80)
    print(" ALL PYTHON VERSION SUITES EXECUTED SUCCESSFULLY")
    print("#" * 80 + "\n")


if __name__ == "__main__":
    run_all_version_demos()
