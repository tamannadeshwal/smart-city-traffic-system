"""Task 6 - Network connectivity using BFS and DFS."""
from collections import deque


def bfs(g, start):
    adj = g.adjacency_list()
    seen, order, q = {start}, [], deque([start])
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return order


def dfs(g, start):
    adj = g.adjacency_list()
    seen, order = set(), []

    def visit(u):
        seen.add(u)
        order.append(u)
        for v, _ in adj[u]:
            if v not in seen:
                visit(v)
    visit(start)
    return order


def unreachable(g, start):
    return [n for n in g.nodes if n not in set(bfs(g, start))]
