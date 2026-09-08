"""
CLI to run exception handling examples.

This script provides a command-line interface to demonstrate various
exception handling techniques and best practices.
"""
import argparse
import logging

from core_python.exception_handling.best_practices import (
    bad_practice_generic_exception,
    bad_practice_swallow_exception,
    good_practice_clear_error_message,
    good_practice_finally_for_cleanup,
    good_practice_specific_exception,
)
from core_python.exception_handling.context_managers import SuppressAndLog
from core_python.exception_handling.custom_exceptions import (
    ResourceUnavailableError,
    ValidationError,
)
from core_python.exception_handling.handling_strategies import (
    guard_against_resource_failure,
    safe_execute,
    validate_input,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_strategies_examples() -> None:
    """Demonstrate handling strategies."""
    print("--- Running Handling Strategies Examples ---")

    # safe_execute
    print("[safe_execute]")
    result = safe_execute(lambda: 1 / 0, default="Division failed")
    print(f"safe_execute handled ZeroDivisionError, result: {result}")

    # validate_input
    print("[validate_input]")
    try:
        validate_input("")
    except ValidationError as e:
        print(f"Caught expected validation error: {e}")

    # guard_against_resource_failure
    print("[guard_against_resource_failure]")
    try:
        guard_against_resource_failure("Database", available=False)
    except ResourceUnavailableError as e:
        print(f"Caught expected resource error: {e}")


def run_contexts_examples() -> None:
    """Demonstrate context manager examples."""
    print("--- Running Context Manager Examples ---")

    # SuppressAndLog
    print("[SuppressAndLog]")
    with SuppressAndLog(ZeroDivisionError, TypeError):
        print("Attempting 1 / 0...")
        1 / 0
        print("This line is not reached.")

    print("Exception was suppressed and logged. Continuing execution.")

    with SuppressAndLog(TypeError):
        print("Attempting 'a' + 1...")
        "a" + 1
        print("This line is not reached either.")

    print("Another exception was suppressed. The program is stable.")


def run_practices_examples() -> None:
    """Demonstrate best and worst practices."""
    print("--- Running Best Practices Examples ---")

    # Bad practices
    print("[Bad Practice: Generic Exception]")
    bad_practice_generic_exception(1, 0)

    print("[Bad Practice: Swallow Exception]")
    bad_practice_swallow_exception("non_existent_file.txt")
    print("Error from missing file was swallowed. Did you notice?")

    # Good practices
    print("[Good Practice: Specific Exception]")
    good_practice_specific_exception(1, 0)

    print("[Good Practice: Finally for Cleanup]")
    good_practice_finally_for_cleanup()

    print("[Good Practice: Clear Error Message]")
    try:
        good_practice_clear_error_message(-1)
    except ValueError as e:
        print(f"Caught clear error message: {e}")


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Run exception handling examples."
    )
    parser.add_argument(
        "example",
        nargs="?",
        choices=["all", "strategies", "contexts", "practices"],
        default="all",
        help="The specific set of examples to run.",
    )

    args = parser.parse_args()

    if args.example == "all":
        run_strategies_examples()
        run_contexts_examples()
        run_practices_examples()
    elif args.example == "strategies":
        run_strategies_examples()
    elif args.example == "contexts":
        run_contexts_examples()
    elif args.example == "practices":
        run_practices_examples()


if __name__ == "__main__":
    main()
