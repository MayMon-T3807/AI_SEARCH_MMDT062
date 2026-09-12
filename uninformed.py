from collections import deque
import json


def load_graph(filepath):
    with open(filepath) as f:
        data = json.load(f)

    graph = {}
    for city in data["nodes"]:
        graph[city] = []

    for edge in data["edges"]:
        a = edge["from"]
        b = edge["to"]
        weight = edge["distance_km"]
        graph[a].append((b, weight))
        graph[b].append((a, weight))

    return graph


def get_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        for neighbor, weight in graph[current]:
            if neighbor == next_city:
                total += weight
    return total


def bfs(graph, start, goal):
    queue = deque()
    queue.append([start])
    visited = [start]
    visited_order = []

    while queue:
        path = queue.popleft()
        city = path[-1]
        visited_order.append(city)

        if city == goal:
            return {"path": path, "visited_order": visited_order, "cost": get_cost(graph, path)}

        for neighbor, weight in graph[city]:
            if neighbor not in visited:
                visited.append(neighbor)
                new_path = path + [neighbor]
                queue.append(new_path)

    return {"path": None, "visited_order": visited_order, "cost": None}


def dfs(graph, start, goal):
    stack = [[start]]
    visited = []
    visited_order = []

    while stack:
        path = stack.pop()
        city = path[-1]

        if city in visited:
            continue
        visited.append(city)
        visited_order.append(city)

        if city == goal:
            return {"path": path, "visited_order": visited_order, "cost": get_cost(graph, path)}

        for neighbor, weight in graph[city]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                stack.append(new_path)

    return {"path": None, "visited_order": visited_order, "cost": None}


def ucs(graph, start, goal):
    frontier = [[0, [start]]]
    visited_order = []
    best_cost = {start: 0}

    while frontier:
        frontier.sort(key=lambda x: x[0])
        cost, path = frontier.pop(0)
        city = path[-1]

        visited_order.append(city)

        if city == goal:
            return {"path": path, "visited_order": visited_order, "cost": cost}

        for neighbor, weight in graph[city]:
            new_cost = cost + weight
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                new_path = path + [neighbor]
                frontier.append([new_cost, new_path])

    return {"path": None, "visited_order": visited_order, "cost": None}


def ids(graph, start, goal):
    visited_order = []

    def dfs_limited(city, path, depth, limit, visited):
        visited_order.append(city)

        if city == goal:
            return path

        if depth == limit:
            return None

        for neighbor, weight in graph[city]:
            if neighbor not in visited:
                visited.append(neighbor)
                result = dfs_limited(neighbor, path + [neighbor], depth + 1, limit, visited)
                if result is not None:
                    return result
                visited.remove(neighbor)

        return None

    total_cities = len(graph)
    for limit in range(total_cities + 1):
        visited = [start]
        result = dfs_limited(start, [start], 0, limit, visited)
        if result is not None:
            return {"path": result, "visited_order": visited_order, "cost": get_cost(graph, result)}

    return {"path": None, "visited_order": visited_order, "cost": None}


if __name__ == "__main__":
    test_graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("A", 1), ("C", 2), ("D", 5)],
        "C": [("A", 4), ("B", 2), ("D", 1)],
        "D": [("B", 5), ("C", 1)],
    }
    print("BFS:", bfs(test_graph, "A", "D"))
    print("DFS:", dfs(test_graph, "A", "D"))
    print("UCS:", ucs(test_graph, "A", "D"))
    print("IDS:", ids(test_graph, "A", "D"))

    print("\n--- now testing against real Myanmar data ---")
    real_graph = load_graph("map_data.json")
    print("BFS:", bfs(real_graph, "Yangon", "Mandalay"))
    print("UCS:", ucs(real_graph, "Yangon", "Mandalay"))