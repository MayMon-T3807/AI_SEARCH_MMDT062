import json
import math


def load_graph(filepath):
    with open(filepath) as f:
        data = json.load(f)

    graph = {}
    coords = {}

    for city, latlon in data["nodes"].items():
        graph[city] = []
        coords[city] = latlon

    for edge in data["edges"]:
        a = edge["from"]
        b = edge["to"]
        weight = edge["distance_km"]
        graph[a].append((b, weight))
        graph[b].append((a, weight))

    return graph, coords


def get_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        for neighbor, weight in graph[current]:
            if neighbor == next_city:
                total += weight
    return total


def haversine(coords, city_a, city_b):
    lat1, lon1 = coords[city_a]["lat"], coords[city_a]["lon"]
    lat2, lon2 = coords[city_b]["lat"], coords[city_b]["lon"]

    R = 6371  # earth radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def greedy(graph, coords, start, goal):
    frontier = [[haversine(coords, start, goal), [start]]]
    visited = [start]
    visited_order = []

    while frontier:
        frontier.sort(key=lambda x: x[0])
        h, path = frontier.pop(0)
        city = path[-1]
        visited_order.append(city)

        if city == goal:
            return {"path": path, "visited_order": visited_order, "cost": get_cost(graph, path)}

        for neighbor, weight in graph[city]:
            if neighbor not in visited:
                visited.append(neighbor)
                new_path = path + [neighbor]
                new_h = haversine(coords, neighbor, goal)
                frontier.append([new_h, new_path])

    return {"path": None, "visited_order": visited_order, "cost": None}


def astar(graph, coords, start, goal):
    frontier = [[haversine(coords, start, goal), 0, [start]]]
    best_cost = {start: 0}
    visited_order = []

    while frontier:
        frontier.sort(key=lambda x: x[0])
        f, cost, path = frontier.pop(0)
        city = path[-1]
        visited_order.append(city)

        if city == goal:
            return {"path": path, "visited_order": visited_order, "cost": cost}

        for neighbor, weight in graph[city]:
            new_cost = cost + weight
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                new_path = path + [neighbor]
                new_f = new_cost + haversine(coords, neighbor, goal)
                frontier.append([new_f, new_cost, new_path])

    return {"path": None, "visited_order": visited_order, "cost": None}


if __name__ == "__main__":
    test_graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("A", 1), ("C", 2), ("D", 5)],
        "C": [("A", 4), ("B", 2), ("D", 1)],
        "D": [("B", 5), ("C", 1)],
    }
    test_coords = {
        "A": {"lat": 0, "lon": 0},
        "B": {"lat": 0, "lon": 0.01},
        "C": {"lat": 0.01, "lon": 0},
        "D": {"lat": 0.01, "lon": 0.01},
    }
    print("Greedy:", greedy(test_graph, test_coords, "A", "D"))
    print("A*:", astar(test_graph, test_coords, "A", "D"))

    print("\n--- now testing against real Myanmar data ---")
    real_graph, real_coords = load_graph("map_data.json")
    print("Greedy:", greedy(real_graph, real_coords, "Yangon", "Mandalay"))
    print("A*:", astar(real_graph, real_coords, "Yangon", "Mandalay"))