"""Road network model: vertices = intersections, edges = roads (undirected, weighted)."""
import random
import pandas as pd


class RoadNetwork:
    def __init__(self):
        self.nodes = []
        self.edges = {}  # (u, v) with u < v  ->  weight

    def add_intersection(self, name):
        name = str(name).strip()
        if name and name not in self.nodes:
            self.nodes.append(name)

    def add_road(self, u, v, w):
        if u == v:
            raise ValueError("A road must connect two different intersections.")
        if w <= 0:
            raise ValueError("Travel cost must be positive.")
        self.add_intersection(u)
        self.add_intersection(v)
        self.edges[tuple(sorted((u, v)))] = float(w)

    def set_weight(self, u, v, w):
        key = tuple(sorted((u, v)))
        if key not in self.edges:
            raise KeyError(f"No road between {u} and {v}.")
        self.edges[key] = float(w)

    def adjacency_list(self):
        adj = {n: [] for n in self.nodes}
        for (u, v), w in self.edges.items():
            adj[u].append((v, w))
            adj[v].append((u, w))
        for n in adj:
            adj[n].sort()
        return adj

    def adjacency_matrix(self):
        df = pd.DataFrame(0.0, index=self.nodes, columns=self.nodes)
        for (u, v), w in self.edges.items():
            df.loc[u, v] = w
            df.loc[v, u] = w
        return df

    def copy(self):
        g = RoadNetwork()
        g.nodes = list(self.nodes)
        g.edges = dict(self.edges)
        return g


def sample_city():
    g = RoadNetwork()
    roads = [("Airport", "Central", 12), ("Airport", "Mall", 7), ("Central", "Mall", 4),
             ("Central", "Station", 5), ("Mall", "Hospital", 9), ("Station", "Hospital", 3),
             ("Station", "University", 8), ("Hospital", "University", 6),
             ("University", "Stadium", 5), ("Hospital", "Stadium", 10), ("Mall", "Stadium", 15)]
    for u, v, w in roads:
        g.add_road(u, v, w)
    return g


def random_network(n, extra_ratio=1.5, seed=42):
    """Connected random network with n intersections (~n*(1+extra_ratio) roads)."""
    rnd = random.Random(seed)
    g = RoadNetwork()
    names = [f"I{i}" for i in range(n)]
    for x in names:
        g.add_intersection(x)
    for i in range(1, n):  # random tree guarantees connectivity
        g.add_road(names[i], names[rnd.randrange(i)], rnd.randint(1, 20))
    target = int(n * extra_ratio)
    tries = 0
    while target > 0 and tries < 20 * n:
        tries += 1
        a, b = rnd.sample(names, 2)
        if tuple(sorted((a, b))) not in g.edges:
            g.add_road(a, b, rnd.randint(1, 20))
            target -= 1
    return g
