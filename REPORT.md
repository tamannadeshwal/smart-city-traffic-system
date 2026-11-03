# Smart City Traffic Management and Route Optimization System
**Name:** Tamanna | **Roll No:** 2401201138 | **Course:** BCA (AI & DS) - A, Capstone Project | **Faculty:** Ms. Aarti Sangwan

## 1. Introduction
**Smart city concepts.** Smart cities use data and algorithms to manage transport, utilities and services. A road network maps naturally onto a graph, so classic graph algorithms can answer routing and planning questions.
**Importance of traffic optimization.** Congestion wastes time and fuel, delays emergency response and raises emissions. Fast shortest-path computation, rerouting under congestion and well-planned infrastructure reduce these costs.

## 2. Experimental Results
### 2.1 Sample road network (12 roads, 8 intersections)
Airport, Central, Mall, Market, Station, Hospital, University, Stadium (see `sample_city()` in `graph_model.py`).

![Network tab](<screenshots/1_network.png.png>)
![Adjacency list and matrix](<screenshots/1_network_matrix.png.png>)

### 2.2 Route calculation (Dijkstra)
Airport → Stadium: **Airport → Mall → Stadium, cost 22**.

![Route planning](<screenshots/2.0_route.png.png>)
![Shortest path on graph](<screenshots/2_route.png>)
![Distance updates](<screenshots/2_route_steps.png.png>)

### 2.3 Traffic analysis (Bellman-Ford)
Mall—Stadium multiplied by ×5: the route is **rerouted** to Airport → Mall → Hospital → Stadium, cost 22 → 26 (about +18%).

![Congestion input](<screenshots/3.0_traffic.png..png>)
![Original vs congested](<screenshots/3_traffic.png.jpeg>)
![Bellman-Ford relaxations](<screenshots/3_traffic_table.png (2).png>)

### 2.4 Traversal outputs (start = Airport)
- BFS: Airport, Central, Mall, Market, Station, Hospital, Stadium, University
- DFS: Airport, Central, Mall, Hospital, Stadium, University, Station, Market
- All 8 intersections reachable; the network is fully connected.

![Connectivity](<screenshots/4_connectivity.png..png>)

### 2.5 MST outputs
Prim and Kruskal both give total cost **36**.

![Prim and Kruskal MST](<screenshots/5_mst.png..png>)
![Selected roads](<screenshots/5_mst_table.png..png>)

### 2.6 Benchmarks
![BFS vs DFS](<screenshots/6_compare_bfs_dfs.png.png>)
![Dijkstra vs Bellman-Ford](<screenshots/6_compare_dijkstra_bf.png.png>)
![Prim vs Kruskal](<screenshots/6_compare_prim_kruskal.png.png>)

| Nodes | Roads | Dijkstra ms | Bellman-Ford ms | Prim ms | Kruskal ms |
|---|---|---|---|---|---|
| 10 | 24 | 0.2824 | 0.3383 | 0.1408 | 0.0944 |
| 25 | 61 | 0.5349 | 1.0711 | 0.2371 | 0.1798 |
| 50 | 124 | 2.1288 | 2.8290 | 0.8748 | 0.3005 |
| 100 | 249 | 4.5508 | 8.2699 | 2.0680 | 0.7490 |

## 3. Analysis
- **BFS vs DFS:** both O(V+E). BFS finds fewest-hop reachability and uses a queue; DFS goes deep (recursion). BFS suits "what is within N junctions" monitoring; DFS suits exploring/connectivity checks.
- **Dijkstra vs Bellman-Ford:** Dijkstra O((V+E)log V) is about twice as fast here and ideal for live navigation (non-negative weights). Bellman-Ford O(VE) is slower but handles negative weights and detects negative cycles; useful for what-if analysis.
- **Prim vs Kruskal:** both give the same optimal cost. Kruskal O(E log E) was faster on these sparse graphs; Prim is better for dense graphs.
- **Traffic observations:** raising weights on a main road either increases cost on the same path or triggers an alternate route; the module reports the delta and percentage.
- **Infrastructure insights:** the MST gives the cheapest way to connect all junctions but has no redundancy, so it is a baseline, not a final design.

## 4. Conclusion
**Key findings:** Dijkstra is best for routing, Bellman-Ford for flexible analysis, BFS/DFS for reachability, and Prim/Kruskal give equal-cost minimal networks.
**Benefits:** graph algorithms give fast, explainable, optimal decisions for navigation, rerouting and planning.
**Future improvements:** directed one-way roads, A*, live traffic data, real map import (OpenStreetMap), time-dependent weights, MST with redundancy.

## References
Cormen et al., *Introduction to Algorithms*; Kleinberg & Tardos, *Algorithm Design*; NetworkX and Streamlit documentation.
