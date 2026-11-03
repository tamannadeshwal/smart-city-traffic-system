"""Smart City Traffic Management System - Streamlit app.  Run: streamlit run app.py"""
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from graph_model import RoadNetwork, sample_city, random_network
from route_planner import shortest_route
from traffic_analysis import bf_route, compare_routes
from connectivity_module import bfs, dfs, unreachable
from mst_planner import prim, kruskal
import benchmark

st.set_page_config(page_title="Smart City Traffic System", layout="wide")
if "g" not in st.session_state:
    st.session_state.g = sample_city()
g: RoadNetwork = st.session_state.g


def draw(graph, path=None, mst=None, title="", color="tab:red"):
    G = nx.Graph()
    G.add_nodes_from(graph.nodes)
    for (u, v), w in graph.edges.items():
        G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=7)
    fig, ax = plt.subplots(figsize=(7, 5))
    nx.draw_networkx(G, pos, ax=ax, node_color="#cfe8ff", edge_color="#bbbbbb", node_size=700, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, "weight"), ax=ax, font_size=7)
    hl = []
    if path and len(path) > 1:
        hl = list(zip(path, path[1:]))
    if mst:
        hl = [(u, v) for u, v, _ in mst]
    if hl:
        nx.draw_networkx_edges(G, pos, edgelist=hl, edge_color=color, width=3, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist={x for e in hl for x in e}, node_color="#ffd27f", node_size=700, ax=ax)
    ax.set_title(title)
    ax.axis("off")
    st.pyplot(fig)
    plt.close(fig)


st.title("🚦 Smart City Traffic Management & Route Optimization")

with st.sidebar:
    st.header("City network")
    choice = st.selectbox("Load network", ["Keep current", "Sample city", "Random 10", "Random 25", "Random 50", "Random 100", "Empty"])
    if st.button("Load") and choice != "Keep current":
        st.session_state.g = (sample_city() if choice == "Sample city" else RoadNetwork() if choice == "Empty"
                              else random_network(int(choice.split()[1])))
        st.rerun()
    up = st.file_uploader("…or upload CSV (u,v,weight)", type="csv")
    if up is not None and st.button("Import CSV"):
        df = pd.read_csv(up)
        ng = RoadNetwork()
        for _, r in df.iterrows():
            ng.add_road(str(r.iloc[0]), str(r.iloc[1]), float(r.iloc[2]))
        st.session_state.g = ng
        st.rerun()
    st.caption(f"{len(g.nodes)} intersections · {len(g.edges)} roads")

t1, t2, t3, t4, t5, t6 = st.tabs(["1 Network", "2 Route Planning", "3 Traffic Analysis",
                                  "4 Connectivity", "5 Infrastructure (MST)", "6 Comparison"])

with t1:
    c1, c2 = st.columns(2)
    with c1:
        n = st.text_input("New intersection name")
        if st.button("Add intersection") and n:
            g.add_intersection(n)
            st.rerun()
        if len(g.nodes) >= 2:
            a = st.selectbox("From", g.nodes, key="ra")
            b = st.selectbox("To", g.nodes, index=1, key="rb")
            w = st.number_input("Travel cost (km / min)", 1.0, 1000.0, 5.0)
            if st.button("Add road"):
                try:
                    g.add_road(a, b, w)
                    st.rerun()
                except ValueError as e:
                    st.error(e)
    with c2:
        draw(g, title="City road network")
    if g.nodes:
        st.subheader("Adjacency list")
        st.code("\n".join(f"{u}: {nb}" for u, nb in g.adjacency_list().items()))
        st.subheader("Adjacency matrix")
        st.dataframe(g.adjacency_matrix())

if len(g.nodes) < 2:
    st.info("Add at least 2 intersections to use the other modules.")
    st.stop()

with t2:
    s = st.selectbox("Source", g.nodes, key="ps")
    d = st.selectbox("Destination", g.nodes, index=len(g.nodes) - 1, key="pd")
    if st.button("Find shortest route (Dijkstra)"):
        path, cost, steps = shortest_route(g, s, d)
        if not path:
            st.error("Destination is not reachable.")
        else:
            st.success(f"Route: {' → '.join(path)}  |  Total cost: {cost:g}")
            draw(g, path=path, title=f"{s} → {d}  (cost {cost:g})")
            st.subheader("Distance updates")
            st.dataframe(pd.DataFrame(steps), use_container_width=True)

with t3:
    s3 = st.selectbox("Source", g.nodes, key="ts")
    d3 = st.selectbox("Destination", g.nodes, index=len(g.nodes) - 1, key="td")
    roads = [f"{u} — {v}" for (u, v) in g.edges]
    sel = st.multiselect("Congested roads", roads)
    factor = st.slider("Congestion multiplier", 1.0, 10.0, 3.0, 0.5)
    if st.button("Analyse traffic (Bellman-Ford)"):
        changes = [(x.split(" — ")[0], x.split(" — ")[1], factor) for x in sel]
        r = compare_routes(g, changes, s3, d3)
        if not r["original_path"]:
            st.error("Destination is not reachable.")
        else:
            a, b = st.columns(2)
            with a:
                draw(g, r["original_path"], title=f"Original (cost {r['original_cost']:g})", color="tab:green")
            with b:
                draw(r["congested_graph"], r["new_path"], title=f"After congestion (cost {r['new_cost']:g})")
            st.metric("Travel cost change", f"{r['new_cost']:g}", f"{r['delta']:+g} ({r['pct']:+.1f}%)", delta_color="inverse")
            st.write("**Rerouted:**", "Yes" if r["rerouted"] else "No — same route is still best")
            st.write("Original:", " → ".join(r["original_path"]), "| New:", " → ".join(r["new_path"]))
            st.subheader("Bellman-Ford relaxations (congested network)")
            st.dataframe(pd.DataFrame(r["log"]), use_container_width=True)

with t4:
    st0 = st.selectbox("Start intersection", g.nodes, key="cs")
    b_, d_ = bfs(g, st0), dfs(g, st0)
    c1, c2 = st.columns(2)
    c1.write("**BFS order:** " + " → ".join(b_))
    c2.write("**DFS order:** " + " → ".join(d_))
    st.write(f"**Reachable ({len(b_)}):** {', '.join(b_)}")
    un = unreachable(g, st0)
    st.write("**Unreachable:** " + (", ".join(un) if un else "none — network is connected from here"))

with t5:
    p, pt = prim(g)
    k, kt = kruskal(g)
    c1, c2 = st.columns(2)
    for col, name, mst, tot in ((c1, "Prim", p, pt), (c2, "Kruskal", k, kt)):
        with col:
            draw(g, mst=mst, title=f"{name} MST — cost {tot:g}", color="tab:blue")
            st.dataframe(pd.DataFrame(mst, columns=["From", "To", "Cost"]))
            st.metric(f"{name} total infrastructure cost", f"{tot:g}")
    if len(p) < len(g.nodes) - 1:
        st.warning("Network is disconnected — result is not a full spanning tree.")

with t6:
    if st.button("Run benchmarks (10/25/50/100 intersections)"):
        for name, df in benchmark.run().items():
            st.subheader(name)
            st.dataframe(df, use_container_width=True)
