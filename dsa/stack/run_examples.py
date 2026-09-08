"""Run Stack data structure and algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.stack.stack import (
    MinStack,
    Stack,
    evaluate_postfix,
    is_balanced,
    next_greater_element,
)

logger = logging.getLogger(__name__)


def run_stack_basics_examples() -> None:
    logger.info("Running Stack basic operations")
    st: Stack[int] = Stack()
    for x in [10, 20, 30]:
        st.push(x)
    print(f"Stack: {st}, peek: {st.peek()}, size: {len(st)}")
    print(f"Popped: {st.pop()}, remaining: {st}")


def run_min_stack_examples() -> None:
    logger.info("Running MinStack O(1) minimum demonstrations")
    ms: MinStack[int] = MinStack()
    for x in [5, 2, 7, 1, 9]:
        ms.push(x)
        print(f"Pushed {x}, current min: {ms.get_min()}")

    ms.pop()  # pops 9
    ms.pop()  # pops 1
    print(f"After popping two elements, current min: {ms.get_min()}")


def run_parentheses_examples() -> None:
    logger.info("Running balanced parentheses validation")
    expressions = ["({[]})", "([)]", "{[()]}", "((("]
    for expr in expressions:
        valid = is_balanced(expr)
        print(f"Expression: {expr!r:10} -> Balanced: {valid}")


def run_postfix_and_monotonic_examples() -> None:
    logger.info("Running postfix evaluation and Next Greater Element")
    expr = "3 4 + 2 * 7 /"
    result = evaluate_postfix(expr)
    print(f"Postfix '{expr}' evaluated to: {result}")

    nums = [4, 5, 2, 10, 8]
    nge = next_greater_element(nums)
    print(f"Next Greater Element for {nums}: {nge}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Stack examples")
    parser.add_argument(
        "--module",
        choices=["basic", "min_stack", "parentheses", "postfix", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "basic": run_stack_basics_examples,
        "min_stack": run_min_stack_examples,
        "parentheses": run_parentheses_examples,
        "postfix": run_postfix_and_monotonic_examples,
    }

    if args.module == "all":
        for fn in dispatch.values():
            fn()
    else:
        dispatch[args.module]()


if __name__ == "__main__":
    main()
