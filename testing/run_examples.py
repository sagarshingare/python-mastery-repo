"""Runner for testing demonstrations: mocking, integration testing, and performance testing."""

from __future__ import annotations

from testing.integration_testing.integration_patterns import run_all as run_integration
from testing.mocking.mock_examples import run_all as run_mocking
from testing.performance_testing.benchmark_utils import run_all as run_performance


def main() -> None:
    print("==================================================")
    print("       Python Mastery Testing Demonstrations      ")
    print("==================================================")
    run_mocking()
    run_integration()
    run_performance()
    print("\nAll testing demonstrations completed successfully!")


if __name__ == "__main__":
    main()
