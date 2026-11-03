"""Task 7 - Infrastructure planning: Prim's and Kruskal's MST."""
import heapq


def prim(g, start=None):
    adj = g.adjacency_list()
    start = start or g.nodes[0]
    seen, mst, total = {start}, [], 0.0
    pq = [(w, start, v) for v, w in adj[start]]
    heapq.heapify(pq)
    while pq and len(seen) < len(g.nodes):
        w, u, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        mst.append((u, v, w))
        total += w
        for x, wx in adj[v]:
            if x not in seen:
                heapq.heappush(pq, (wx, v, x))
    return mst, total


def kruskal(g):
    parent = {n: n for n in g.nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst, total = [], 0.0
    for (u, v), w in sorted(g.edges.items(), key=lambda e: e[1]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            mst.append((u, v, w))
            total += w
    return mst, total
