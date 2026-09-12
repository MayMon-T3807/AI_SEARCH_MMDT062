import json
from uninformed import bfs, dfs, ucs, ids, load_graph
from informed import greedy, astar, load_graph as load_graph_with_coords

graph = load_graph("map_data.json")
graph2, coords = load_graph_with_coords("map_data.json")

test_pairs = [
    ("Yangon", "Mandalay"),
    ("Sittwe", "Myitkyina"),
    ("Dawei", "Myeik"),
    ("Pathein", "Lashio"),
    ("Taunggyi", "Sittwe"),
]

for start, goal in test_pairs:
    print(f"\n=== {start} -> {goal} ===")

    results = {
        "BFS": bfs(graph, start, goal),
        "DFS": dfs(graph, start, goal),
        "UCS": ucs(graph, start, goal),
        "IDS": ids(graph, start, goal),
        "Greedy": greedy(graph2, coords, start, goal),
        "A*": astar(graph2, coords, start, goal),
    }

    for name, r in results.items():
        hops = len(r["path"]) - 1 if r["path"] else None
        print(f"{name:8} hops={hops!s:5} cost={r['cost']!s:8} visited={len(r['visited_order'])}")

    # sanity checks
    bfs_hops = len(results["BFS"]["path"]) - 1
    ids_hops = len(results["IDS"]["path"]) - 1
    ucs_cost = results["UCS"]["cost"]
    astar_cost = results["A*"]["cost"]

    print("-- checks --")
    print("BFS hops == IDS hops:", bfs_hops == ids_hops)
    print("UCS cost == A* cost:", abs(ucs_cost - astar_cost) < 0.01)