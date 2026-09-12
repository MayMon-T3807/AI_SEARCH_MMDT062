from flask import Flask, jsonify, request, render_template
import json

from uninformed import bfs, dfs, ucs, ids
from informed import greedy, astar

app = Flask(__name__)

with open("map_data.json") as f:
    map_data = json.load(f)

coords = map_data["nodes"]

graph = {}
for city in coords:
    graph[city] = []

for edge in map_data["edges"]:
    a = edge["from"]
    b = edge["to"]
    weight = edge["distance_km"]
    graph[a].append((b, weight))
    graph[b].append((a, weight))

algorithm_info = {
    "bfs": {
        "name": "BFS",
        "main_idea": "Explores all neighbouring cities before moving one step further out, expanding outward ring by ring.",
        "node_selection": "Picks whichever city was added to the search frontier earliest (a FIFO queue).",
        "info_used": "Depth only — no path cost or heuristic is used.",
    },
    "dfs": {
        "name": "DFS",
        "main_idea": "Follows a single road as far as it can go, only backtracking once it hits a dead end.",
        "node_selection": "Picks whichever city was added to the frontier most recently (a LIFO stack).",
        "info_used": "None beyond the search tree itself — no path cost or heuristic is used.",
    },
    "ucs": {
        "name": "UCS",
        "main_idea": "Always expands whichever path currently has the lowest total travel cost.",
        "node_selection": "Picks the city with the lowest cumulative path cost so far (a priority queue).",
        "info_used": "Path cost only.",
    },
    "ids": {
        "name": "IDS",
        "main_idea": "Repeats a depth-limited search, increasing the depth limit each round until the goal is found.",
        "node_selection": "Within each attempt, behaves like DFS — picks the most recently added city, bounded by the current depth limit.",
        "info_used": "Depth only.",
    },
    "greedy": {
        "name": "Greedy Best-First",
        "main_idea": "Always moves toward whichever city appears closest to the destination right now.",
        "node_selection": "Picks the city with the lowest estimated straight-line distance to the goal.",
        "info_used": "Heuristic only — path cost so far is ignored.",
    },
    "astar": {
        "name": "A*",
        "main_idea": "Balances how far it has already travelled with how far it estimates still remains.",
        "node_selection": "Picks the city with the lowest combined score of (path cost so far + estimated distance to goal).",
        "info_used": "A combination of path cost and heuristic.",
    },
}

algorithm_functions = {
    "bfs": lambda start, goal: bfs(graph, start, goal),
    "dfs": lambda start, goal: dfs(graph, start, goal),
    "ucs": lambda start, goal: ucs(graph, start, goal),
    "ids": lambda start, goal: ids(graph, start, goal),
    "greedy": lambda start, goal: greedy(graph, coords, start, goal),
    "astar": lambda start, goal: astar(graph, coords, start, goal),
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")


@app.route("/cities")
def cities():
    city_list = []
    for name, latlon in coords.items():
        city_list.append({"name": name, "lat": latlon["lat"], "lon": latlon["lon"]})
    return jsonify(city_list)


@app.route("/search")
def search():
    start = request.args.get("start")
    goal = request.args.get("goal")
    algorithm = request.args.get("algorithm")

    if start not in graph or goal not in graph:
        return jsonify({"error": "unknown city"}), 400

    if algorithm not in algorithm_functions:
        return jsonify({"error": "unknown algorithm"}), 400

    if start == goal:
        return jsonify({"error": "start and goal must be different"}), 400

    result = algorithm_functions[algorithm](start, goal)
    result["concept_note"] = algorithm_info[algorithm]

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)