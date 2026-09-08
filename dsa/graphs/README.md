# Graphs

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.10: Graphs**

Adjacency-list graph representation, graph search traversals, cycle detection, and topological sorting.

## Key Data Structures & Algorithms

- **`Graph`**: Flexible adjacency list supporting directed and undirected graphs, weighted edges, and vertex sets.
- **`bfs(start)`**: Breadth-First Search queue exploration for shortest unweighted paths.
- **`dfs(start)`**: Depth-First Search recursive exploration.
- **`topological_sort()`**: Kahn's in-degree algorithm or DFS post-order ordering for DAG dependency resolution.
- **`has_cycle()`**: Cycle detection in directed (3-color DFS) and undirected (parent tracking) graphs.

## Quick Start

```python
from dsa.graphs import Graph

g = Graph(directed=True)
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")

assert g.bfs("A") == ["A", "B", "C", "D"]
```
