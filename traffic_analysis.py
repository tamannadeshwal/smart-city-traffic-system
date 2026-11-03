"""Task 5 - Traffic Analysis using Bellman-Ford."""
from route_planner import build_path


def bellman_ford(g, source):
    """Each undirected road = two directed arcs. Returns (dist, prev, log)."""
    arcs = []
    for (u, v), w in g.edges.items():
        arcs += [(u, v, w), (v, u, w)]
    dist = {n: float("inf") for n in g.nodes}
    prev = {n: None for n in g.nodes}
    dist[source] = 0
    log = []
    for i in range(1, len(g.nodes)):
        changed = False
        for u, v, w in arcs:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed = True
                log.append({"Pass": i, "Relaxed": f"{u} -> {v}", "New Dist": dist[v]})
        if not changed:
            break
    return dist, prev, log


def bf_route(g, source, target):
    dist, prev, log = bellman_ford(g, source)
    return build_path(prev, source, target), dist[target], log


def apply_congestion(g, changes):
    """changes: list of (u, v, multiplier). Returns a new congested network."""
    g2 = g.copy()
    for u, v, factor in changes:
        key = tuple(sorted((u, v)))
        g2.edges[key] = g.edges[key] * factor
    return g2


def compare_routes(g, changes, source, target):
    p1, c1, _ = bf_route(g, source, target)
    g2 = apply_congestion(g, changes)
    p2, c2, log2 = bf_route(g2, source, target)
    return {"original_path": p1, "original_cost": c1, "new_path": p2, "new_cost": c2,
            "delta": c2 - c1, "pct": ((c2 - c1) / c1 * 100) if c1 else 0.0,
            "rerouted": p1 != p2, "congested_graph": g2, "log": log2}
