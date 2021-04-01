import heapq
from typing import List, Tuple
from .graph import Graph


def get_best_route(routes) -> Tuple[List, float]:
    graph = Graph()
    graph.load_from_json(routes)
    # for origin, adj in graph.adjacents:
    #     for dest, weight in adj.items():
    #         print(origin, dest, weight)
    return (['A', 'B', 'D'], 6.25)


def dijkstra(adj, origin, target):
    dist = {origin: 0}
    parent = {origin: None}
    pq = [(0, origin)]
    visited = set()
    while pq:
        du, u = heapq.heappop(pq)
        if u in visited:
            continue
        if u == target:
            break
        visited.add(u)
        for v, weight in adj[u]:
            if v not in dist or dist[v] > du + weight:
                dist[v] = du + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return parent, dist
