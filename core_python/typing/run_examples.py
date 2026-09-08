"""Run typing examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging

from core_python.typing.typing_examples import (
    Coordinate,
    Registry,
    Result,
    Stack,
    configure_log_level,
    create_user_profile,
    find_minimum,
    get_user_order,
    normalize,
    UserId,
    OrderId,
)

logger = logging.getLogger(__name__)


def run_generics() -> None:
    """Demonstrate generic types."""
    print("\n--- Generics ---")

    stack: Stack[int] = Stack()
    for v in [10, 20, 30]:
        stack.push(v)
    print(f"Stack: {stack}")
    print(f"Popped: {stack.pop()}")

    registry: Registry[str, int] = Registry()
    registry.register("alpha", 1)
    registry.register("beta", 2)
    print(f"Lookup 'alpha': {registry.lookup('alpha')}")
    print(f"'gamma' in registry: {'gamma' in registry}")


def run_protocols() -> None:
    """Demonstrate protocol-based structural typing."""
    print("\n--- Protocols ---")
    items = [5, 2, 8, 1, 9]
    print(f"Minimum of {items}: {find_minimum(items)}")


def run_typed_dict() -> None:
    """Demonstrate TypedDict usage."""
    print("\n--- TypedDict ---")
    profile = create_user_profile(1, "alice", "alice@example.com")
    print(f"User profile: {profile}")


def run_literal_newtype() -> None:
    """Demonstrate Literal and NewType."""
    print("\n--- Literal & NewType ---")
    print(configure_log_level("DEBUG"))
    result = get_user_order(UserId(42), OrderId(101))
    print(f"User order: {result}")


def run_overloads() -> None:
    """Demonstrate overloaded functions."""
    print("\n--- Overloads ---")
    print(f"normalize(' Hello ') = {normalize(' Hello ')!r}")
    print(f"normalize(-42)       = {normalize(-42)}")
    print(f"normalize(3.14159)   = {normalize(3.14159)}")


def run_result_pattern() -> None:
    """Demonstrate the Result monad pattern."""
    print("\n--- Result Pattern ---")
    ok: Result[int] = Result.ok(42)
    err: Result[int] = Result.fail("something went wrong")
    print(f"Ok result:  is_ok={ok.is_ok}, value={ok.value}")
    print(f"Err result: is_ok={err.is_ok}, error={err.error}")


def run_namedtuple() -> None:
    """Demonstrate NamedTuple."""
    print("\n--- NamedTuple ---")
    a = Coordinate(0.0, 0.0)
    b = Coordinate(3.0, 4.0)
    print(f"Distance from {a} to {b}: {a.distance_to(b)}")


def main() -> None:
    """Main entry point for typing examples."""
    parser = argparse.ArgumentParser(description="Run typing examples")
    parser.add_argument(
        "--module",
        choices=["generics", "protocols", "typed_dict", "literal", "overloads", "result", "namedtuple"],
        help="Specific example to run",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    runners = {
        "generics": run_generics,
        "protocols": run_protocols,
        "typed_dict": run_typed_dict,
        "literal": run_literal_newtype,
        "overloads": run_overloads,
        "result": run_result_pattern,
        "namedtuple": run_namedtuple,
    }

    if args.module:
        runners[args.module]()
    else:
        for runner in runners.values():
            runner()


if __name__ == "__main__":
    main()
