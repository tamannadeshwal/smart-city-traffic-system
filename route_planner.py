"""Task 4 - Route Planning using Dijkstra's algorithm."""
import heapq


def dijkstra(g, source, target=None):
    """Return (dist, prev, steps). steps logs every distance update."""
    adj = g.adjacency_list()
    dist = {n: float("inf") for n in g.nodes}
    prev = {n: None for n in g.nodes}
    dist[source] = 0
    pq = [(0, source)]
    visited = set()
    steps = []
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        steps.append({"Visit": u, "Dist(u)": d, "Updated": "-", "New Dist": "-", "Via": "-"})
        if u == target:
            break
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
                steps.append({"Visit": u, "Dist(u)": d, "Updated": v, "New Dist": dist[v], "Via": u})
    return dist, prev, steps


def build_path(prev, source, target):
    path, cur = [], target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else []


def shortest_route(g, source, target):
    dist, prev, steps = dijkstra(g, source, target)
    return build_path(prev, source, target), dist[target], steps
