import heapq
from typing import Dict, Tuple

from wtforms.validators import ValidationError
from .graph import Graph


def get_best_route(routes: list, origin: str, target: str) -> tuple:
    """Get the best route according shortest distance between origin and target.

    Args:
        routes (list): Routes list from given map.
        origin (str): Origin point.
        target (str): Destination point.

    Returns:
        tuple: shortest path, disntance between origin and target.
    """
    graph = Graph()
    graph.load_from_json(routes)

    str_list = ", ".join(graph.vertices)
    if origin not in graph.vertices:
        raise ValidationError(
            f"Field 'origin' must be a letter in the range: [{str_list}]")

    if target not in graph.vertices:
        raise ValidationError(
            f"Field 'destiny' must be a letter in the range: [{str_list}]")

    paths, distances = dijkstra(graph.adjacents, origin, target)

    best_path = find_best_path(target=target, paths=paths)

    return (best_path, distances.get(target))


def find_best_path(target: str, paths: dict) -> list:
    """Go throght paths result to find the best path (shortest)

    Args:
        target (str): Destination point.
        paths (dict): Paths result from dijkstra algorithm.

    Returns:
        list: Shortest path according given input parameters.
    """
    dest = target
    path = []
    while dest:
        el = paths.get(dest)
        if el is None:
            break
        path.append(el)
        dest = el

    if len(path) > 0:
        path.append(target)
        path.sort()
    return path


def dijkstra(adj: Dict, origin: str, target: str) -> Tuple[Dict, Dict]:
    """Dijkstra algorithm implementation using priority queue heap to find
        the shortest path between origin and target.

    Args:
        adj (Dict): Adjacent list implementation from the graph.
        origin (str): Origin point to start searching.
        target (str): Destination point of the search.

    Returns:
        tuple[Dict, Dict]: Dict of parent vertex according origin to target and
            Dict of distances from each vertices.
    """
    dist = {origin: 0}
    parent = {origin: None}
    pq = [(0, origin)]
    explored = set()
    while pq:
        du, u = heapq.heappop(pq)
        if u in explored:
            continue
        if u == target:
            break
        explored.add(u)
        for v, weight_str in adj[u].items():
            weight = int(weight_str)
            if v not in dist or dist[v] > du + weight:
                dist[v] = du + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return parent, dist
