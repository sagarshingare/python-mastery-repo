"""Run Linked List algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.linked_list.linked_list import DoublyLinkedList, SinglyLinkedList

logger = logging.getLogger(__name__)


def run_singly_linked_list_examples() -> None:
    logger.info("Running SinglyLinkedList demonstrations")
    sll: SinglyLinkedList[int] = SinglyLinkedList()
    for val in [10, 20, 30, 40, 50]:
        sll.append(val)
    print(f"SinglyLinkedList: {sll}, length: {len(sll)}")

    sll.prepend(5)
    print(f"After prepend(5): {sll}")

    mid = sll.middle_node()
    print(f"Middle node value: {mid}")

    sll.reverse()
    print(f"After reverse(): {sll}")

    print(f"Contains 30: {30 in sll}, Contains 99: {99 in sll}")
    sll.delete(30)
    print(f"After delete(30): {sll}")


def run_doubly_linked_list_examples() -> None:
    logger.info("Running DoublyLinkedList demonstrations")
    dll: DoublyLinkedList[str] = DoublyLinkedList()
    dll.append("alpha")
    dll.append("beta")
    dll.append("gamma")
    dll.prepend("omega")
    print(f"DoublyLinkedList forward: {dll.to_list()}")
    print(f"DoublyLinkedList backward: {dll.to_list_reversed()}")

    dll.delete("beta")
    print(f"After deleting 'beta': {dll.to_list()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Linked List examples")
    parser.add_argument(
        "--module",
        choices=["singly", "doubly", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "singly":
        run_singly_linked_list_examples()
    elif args.module == "doubly":
        run_doubly_linked_list_examples()
    else:
        run_singly_linked_list_examples()
        run_doubly_linked_list_examples()


if __name__ == "__main__":
    main()
