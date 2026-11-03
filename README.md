# Smart City Traffic Management & Route Optimization System
Capstone Project | BCA (AI & DS) - A | Tamanna (2401201138)

Models a city as a weighted graph (intersections = vertices, roads = edges, weight = distance/time) and applies graph algorithms in an interactive Streamlit app.

| Module | File | Algorithms |
|---|---|---|
| Road network modelling | `graph_model.py` | Adjacency list / matrix |
| Route planning | `route_planner.py` | Dijkstra (with step log) |
| Traffic analysis | `traffic_analysis.py` | Bellman-Ford, congestion simulation |
| Connectivity | `connectivity_module.py` | BFS, DFS |
| Infrastructure planning | `mst_planner.py` | Prim, Kruskal |
| Comparative analysis | `benchmark.py` | Timing/memory on 10/25/50/100 nodes |
| UI | `app.py` | Streamlit |

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
python benchmark.py             # console comparison tables
jupyter notebook project_notebook.ipynb
```
CSV import format: `from,to,weight` (one road per row).

## Screenshots
See `screenshots/`. Report: `REPORT.md`; full report with cover page in `report/` (PDF and Word).
