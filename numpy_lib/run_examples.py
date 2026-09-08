"""Master CLI runner for NumPy mastery suite."""

from __future__ import annotations

import argparse
import logging

from numpy_lib.arrays.run_examples import (
    run_creation_demo,
    run_manipulation_demo,
    run_slicing_demo,
)
from numpy_lib.broadcasting.run_examples import (
    run_distance_demo,
    run_expansion_demo,
    run_rules_demo,
)
from numpy_lib.optimization.run_examples import (
    run_downcast_demo,
    run_in_place_demo,
    run_layout_demo,
)
from numpy_lib.vectorization.run_examples import (
    run_benchmark_demo,
    run_conditionals_demo,
    run_reductions_demo,
)

logger = logging.getLogger(__name__)


def run_all_arrays() -> None:
    print("================================================================================")
    print("                      NumPy: Array Operations & Slicing                         ")
    print("================================================================================")
    run_creation_demo()
    print()
    run_slicing_demo()
    print()
    run_manipulation_demo()
    print()


def run_all_broadcasting() -> None:
    print("================================================================================")
    print("                     NumPy: Broadcasting Rules & Distance                       ")
    print("================================================================================")
    run_rules_demo()
    print()
    run_expansion_demo()
    print()
    run_distance_demo()
    print()


def run_all_vectorization() -> None:
    print("================================================================================")
    print("                    NumPy: Vectorization & Ufunc Benchmarks                     ")
    print("================================================================================")
    run_conditionals_demo()
    print()
    run_reductions_demo()
    print()
    run_benchmark_demo()
    print()


def run_all_optimization() -> None:
    print("================================================================================")
    print("                 NumPy: Memory Layout, In-Place & Downcasting                   ")
    print("================================================================================")
    run_layout_demo()
    print()
    run_in_place_demo()
    print()
    run_downcast_demo()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="NumPy Master Suite Demonstrations")
    parser.add_argument(
        "--submodule",
        choices=["arrays", "broadcasting", "vectorization", "optimization", "all"],
        default="all",
        help="Submodule to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "arrays": run_all_arrays,
        "broadcasting": run_all_broadcasting,
        "vectorization": run_all_vectorization,
        "optimization": run_all_optimization,
    }

    if args.submodule == "all":
        for fn in dispatch.values():
            fn()
        print("✅ All NumPy demonstrations executed successfully across all submodules!")
    else:
        dispatch[args.submodule]()


if __name__ == "__main__":
    main()
