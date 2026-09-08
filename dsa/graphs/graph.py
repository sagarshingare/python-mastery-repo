"""Graph implementations with BFS, DFS, topological sort, and cycle detection."""

from __future__ import annotations

from collections import defaultdict, deque
import heapq
from typing import Any, Generator, Iterable


class Graph:
    """An adjacency-list graph supporting both directed and undirected edges.

    Example::

        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert g.bfs("A") == ["A", "B", "C"]
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[Any, list[Any]] = defaultdict(list)
        self._weights: dict[tuple[Any, Any], float] = {}
        self._vertices: set[Any] = set()

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex (no-op if it already exists)."""
        self._vertices.add(vertex)

    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        """Add an edge from *u* to *v* with optional weight."""
        self._vertices.update({u, v})
        self._adj[u].append(v)
        self._weights[(u, v)] = weight
        if not self.directed:
            self._adj[v].append(u)
            self._weights[(v, u)] = weight

    @property
    def vertices(self) -> set[Any]:
        return self._vertices

    def neighbors(self, vertex: Any) -> list[Any]:
        """Return the neighbors of *vertex*."""
        return self._adj.get(vertex, [])

    # --- BFS ---

    def bfs(self, start: Any) -> list[Any]:
        """Breadth-first traversal from *start*. O(V + E)."""
        visited: set[Any] = set()
        order: list[Any] = []
        queue: deque[Any] = deque([start])
        visited.add(start)

        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self._adj[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    # --- DFS ---

    def dfs(self, start: Any) -> list[Any]:
        """Depth-first traversal from *start* (iterative). O(V + E)."""
        visited: set[Any] = set()
        order: list[Any] = []
        stack: list[Any] = [start]

        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            order.append(vertex)
            for neighbor in reversed(self._adj[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

        return order

    def dfs_recursive(self, start: Any) -> list[Any]:
        """Depth-first traversal from *start* (recursive). O(V + E)."""
        visited: set[Any] = set()
        order: list[Any] = []

        def _visit(vertex: Any) -> None:
            visited.add(vertex)
            order.append(vertex)
            for neighbor in self._adj[vertex]:
                if neighbor not in visited:
                    _visit(neighbor)

        _visit(start)
        return order

    # --- Topological sort (Kahn's algorithm) ---

    def topological_sort(self) -> list[Any]:
        """Return a topological ordering of a directed acyclic graph.

        Raises:
            ValueError: If the graph has a cycle or is undirected.
        """
        if not self.directed:
            raise ValueError("Topological sort requires a directed graph")

        in_degree: dict[Any, int] = {v: 0 for v in self._vertices}
        for u in self._adj:
            for v in self._adj[u]:
                in_degree[v] = in_degree.get(v, 0) + 1

        queue: deque[Any] = deque(v for v, d in in_degree.items() if d == 0)
        order: list[Any] = []

        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self._adj[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self._vertices):
            raise ValueError("Graph contains a cycle — topological sort not possible")

        return order

    # --- Cycle detection ---

    def has_cycle(self) -> bool:
        """Detect whether the graph contains a cycle."""
        if self.directed:
            return self._has_cycle_directed()
        return self._has_cycle_undirected()

    def _has_cycle_directed(self) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[Any, int] = {v: WHITE for v in self._vertices}

        def _visit(v: Any) -> bool:
            color[v] = GRAY
            for neighbor in self._adj[v]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and _visit(neighbor):
                    return True
            color[v] = BLACK
            return False

        return any(_visit(v) for v in self._vertices if color[v] == WHITE)

    def _has_cycle_undirected(self) -> bool:
        visited: set[Any] = set()

        def _visit(v: Any, parent: Any | None) -> bool:
            visited.add(v)
            for neighbor in self._adj[v]:
                if neighbor not in visited:
                    if _visit(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for v in self._vertices:
            if v not in visited:
                if _visit(v, None):
                    return True
        return False

    # --- Shortest path (unweighted) ---

    def shortest_path(self, start: Any, end: Any) -> list[Any] | None:
        """Find the shortest path between *start* and *end* using BFS.

        Returns:
            The path as a list of vertices, or None if unreachable.
        """
        if start == end:
            return [start]

        visited: set[Any] = {start}
        queue: deque[list[Any]] = deque([[start]])

        while queue:
            path = queue.popleft()
            vertex = path[-1]
            for neighbor in self._adj[vertex]:
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return None

    # --- Dijkstra's algorithm (weighted shortest path) ---

    def dijkstra(self, start: Any) -> tuple[dict[Any, float], dict[Any, Any | None]]:
        """Compute shortest distances and predecessors from start to all vertices using Dijkstra's algorithm.

        Time Complexity: O((V + E) log V).
        """
        if start not in self._vertices:
            raise ValueError(f"Start vertex {start!r} not in graph")

        distances: dict[Any, float] = {v: float("inf") for v in self._vertices}
        predecessors: dict[Any, Any | None] = {v: None for v in self._vertices}
        distances[start] = 0.0

        pq: list[tuple[float, Any]] = [(0.0, start)]

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if curr_dist > distances[u]:
                continue
            for v in self._adj[u]:
                weight = self._weights.get((u, v), 1.0)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (distances[v], v))

        return distances, predecessors

    def dijkstra_shortest_path(self, start: Any, end: Any) -> tuple[float, list[Any]] | None:
        """Find the shortest weighted path and its total cost from start to end.

        Returns (cost, [start, ..., end]) or None if unreachable.
        """
        if start not in self._vertices or end not in self._vertices:
            return None
        distances, predecessors = self.dijkstra(start)
        if distances[end] == float("inf"):
            return None
        path: list[Any] = []
        curr: Any | None = end
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        return distances[end], path

    def __repr__(self) -> str:
        kind = "Directed" if self.directed else "Undirected"
        return f"Graph({kind}, vertices={len(self._vertices)}, edges={dict(self._adj)})"


# ---------------------------------------------------------------------------
# Disjoint Set Union (Union-Find)
# ---------------------------------------------------------------------------

class DisjointSetUnion:
    """Disjoint Set Union (Union-Find) with path compression and union by rank.

    Supports near O(1) amortized operations: find and union (Ackermann inverse α(N)).
    """

    def __init__(self, elements: Iterable[Any] | None = None) -> None:
        self.parent: dict[Any, Any] = {}
        self.rank: dict[Any, int] = {}
        self._count = 0
        if elements is not None:
            for elem in elements:
                self.add(elem)

    def add(self, x: Any) -> None:
        """Add a new element as a disjoint singleton set."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self._count += 1

    def find(self, x: Any) -> Any:
        """Find the canonical representative of the set containing x with path compression."""
        if x not in self.parent:
            self.add(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """Union the sets containing x and y. Returns True if merged, False if already connected."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        self._count -= 1
        return True

    def connected(self, x: Any, y: Any) -> bool:
        """Return True if x and y belong to the same component."""
        return self.find(x) == self.find(y)

    @property
    def count(self) -> int:
        """Return the number of connected components."""
        return self._count

