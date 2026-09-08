"""Run Queue data structure demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.queue.queue_impl import (
    CircularQueue,
    Deque,
    PriorityQueue,
    Queue,
)

logger = logging.getLogger(__name__)


def run_fifo_queue_examples() -> None:
    logger.info("Running standard FIFO Queue demonstrations")
    q: Queue[str] = Queue()
    for item in ["task1", "task2", "task3"]:
        q.enqueue(item)
    print(f"Queue: {q}, peek: {q.peek()}, size: {len(q)}")
    print(f"Dequeued: {q.dequeue()}, remaining: {q}")


def run_circular_queue_examples() -> None:
    logger.info("Running CircularQueue fixed-buffer demonstrations")
    cq: CircularQueue[int] = CircularQueue(capacity=3)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    print(f"CircularQueue full: {cq.is_full}, items: front={cq.peek()}, size={len(cq)}")
    print(f"Dequeued: {cq.dequeue()}")
    cq.enqueue(4)
    print(f"After wrap-around enqueue(4): front={cq.peek()}, size={len(cq)}")


def run_priority_queue_examples() -> None:
    logger.info("Running PriorityQueue demonstrations")
    pq: PriorityQueue[str] = PriorityQueue()
    pq.enqueue("low priority task", priority=5)
    pq.enqueue("critical emergency", priority=1)
    pq.enqueue("medium priority task", priority=3)

    print(f"PriorityQueue size: {len(pq)}")
    while not pq.is_empty:
        print(f"  Dequeued highest priority: {pq.dequeue()}")


def run_deque_examples() -> None:
    logger.info("Running double-ended Deque demonstrations")
    dq: Deque[int] = Deque()
    dq.append_right(10)
    dq.append_left(5)
    dq.append_right(20)
    dq.append_left(1)
    print(f"Deque: {dq}, left={dq.peek_left()}, right={dq.peek_right()}")
    print(f"Popped left: {dq.pop_left()}, Popped right: {dq.pop_right()}, remaining: {dq}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Queue examples")
    parser.add_argument(
        "--module",
        choices=["fifo", "circular", "priority", "deque", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "fifo": run_fifo_queue_examples,
        "circular": run_circular_queue_examples,
        "priority": run_priority_queue_examples,
        "deque": run_deque_examples,
    }

    if args.module == "all":
        for fn in dispatch.values():
            fn()
    else:
        dispatch[args.module]()


if __name__ == "__main__":
    main()
