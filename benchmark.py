"""Task 8 - Comparative analysis across network sizes."""
import time
import tracemalloc
import pandas as pd
from graph_model import random_network
from route_planner import dijkstra, build_path
from traffic_analysis import bellman_ford
from connectivity_module import bfs, dfs
from mst_planner import prim, kruskal

SIZES = [10, 25, 50, 100]


def timed(fn, *a, repeat=20):
    tracemalloc.start()
    t0 = time.perf_counter()
    for _ in range(repeat):
        out = fn(*a)
    ms = (time.perf_counter() - t0) / repeat * 1000
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    return out, ms, mem


def run(sizes=SIZES):
    rows = {"BFS vs DFS": [], "Dijkstra vs Bellman-Ford": [], "Prim vs Kruskal": []}
    for n in sizes:
        g = random_network(n)
        s, t, m = g.nodes[0], g.nodes[-1], len(g.edges)
        base = {"Intersections": n, "Roads": m}
        for name, f in (("BFS", bfs), ("DFS", dfs)):
            o, ms, mem = timed(f, g, s)
            rows["BFS vs DFS"].append({**base, "Algorithm": name, "Time (ms)": round(ms, 4),
                                       "Nodes visited": len(o), "Memory (KB)": round(mem, 1)})
        for name, f in (("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)):
            o, ms, mem = timed(f, g, s)
            rows["Dijkstra vs Bellman-Ford"].append({**base, "Algorithm": name, "Time (ms)": round(ms, 4),
                                                     "Route cost": o[0][t], "Memory (KB)": round(mem, 1)})
        for name, f in (("Prim", prim), ("Kruskal", kruskal)):
            o, ms, mem = timed(f, g)
            rows["Prim vs Kruskal"].append({**base, "Algorithm": name, "Time (ms)": round(ms, 4),
                                            "MST cost": o[1], "Memory (KB)": round(mem, 1)})
    return {k: pd.DataFrame(v) for k, v in rows.items()}


if __name__ == "__main__":
    for k, df in run().items():
        print(f"\n== {k} ==\n{df.to_string(index=False)}")
