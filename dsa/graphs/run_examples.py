"""Run Graph data structure and algorithm demonstrations."""

from __future__ import annotations

import argparse
import logging

from dsa.graphs.graph import DisjointSetUnion, Graph

logger = logging.getLogger(__name__)


def run_traversal_examples() -> None:
    logger.info("Running Graph BFS & DFS demonstrations")
    g = Graph(directed=False)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E")]:
        g.add_edge(u, v)

    print(f"BFS from 'A': {g.bfs('A')}")
    print(f"DFS from 'A': {g.dfs('A')}")
    print(f"Shortest path (unweighted) A to E: {g.shortest_path('A', 'E')}")
    print(f"Has cycle: {g.has_cycle()}")


def run_topological_sort_examples() -> None:
    logger.info("Running DAG Topological Sort demonstrations")
    dag = Graph(directed=True)
    # Task dependency graph
    dag.add_edge("compile", "link")
    dag.add_edge("link", "run")
    dag.add_edge("parse", "compile")
    dag.add_edge("lint", "compile")

    order = dag.topological_sort()
    print(f"Topological build order: {order}")


def run_dijkstra_examples() -> None:
    logger.info("Running Dijkstra's weighted shortest path")
    wg = Graph(directed=True)
    wg.add_edge("A", "B", weight=4.0)
    wg.add_edge("A", "C", weight=2.0)
    wg.add_edge("C", "B", weight=1.0)
    wg.add_edge("B", "D", weight=5.0)
    wg.add_edge("C", "D", weight=8.0)
    wg.add_edge("C", "E", weight=10.0)
    wg.add_edge("D", "E", weight=2.0)

    cost, path = wg.dijkstra_shortest_path("A", "E")
    print(f"Dijkstra shortest path A -> E: path={path}, cost={cost}")


def run_dsu_examples() -> None:
    logger.info("Running Disjoint Set Union (Union-Find) demonstrations")
    dsu = DisjointSetUnion(["A", "B", "C", "D", "E"])
    print(f"Initial component count: {dsu.count}")

    dsu.union("A", "B")
    dsu.union("B", "C")
    print(f"After union(A,B) and union(B,C), connected(A, C): {dsu.connected('A', 'C')}")
    print(f"connected(A, D): {dsu.connected('A', 'D')}")
    print(f"Current component count: {dsu.count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Graph examples")
    parser.add_argument(
        "--module",
        choices=["traversal", "toposort", "dijkstra", "dsu", "all"],
        default="all",
        help="Demonstration section to execute",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "traversal": run_traversal_examples,
        "toposort": run_topological_sort_examples,
        "dijkstra": run_dijkstra_examples,
        "dsu": run_dsu_examples,
    }

    if args.module == "all":
        for fn in dispatch.values():
            fn()
    else:
        dispatch[args.module]()


if __name__ == "__main__":
    main()
