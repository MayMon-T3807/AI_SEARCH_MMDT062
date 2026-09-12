import requests
import json
import time
import math

cities = [
    "Yangon", "Bago", "Pyay", "Mandalay", "Pyin Oo Lwin", "Meiktila",
    "Naypyidaw", "Nyaung-U", "Monywa", "Sagaing", "Shwebo", "Pathein",
    "Myaungmya", "Magway", "Taungdwingyi", "Dawei", "Myeik", "Taunggyi",
    "Kalaw", "Lashio", "Mawlamyine", "Hpa-An", "Loikaw", "Sittwe", "Myitkyina"
]

manual_overrides = {
    "Nyaung-U": {"lat": 21.1939539, "lon": 94.9071494},
    "Myaungmya": {"lat": 16.5833554, "lon": 94.9039424},
}

headers = {"User-Agent": "MMDT-search-visualizer-student-project"}


def geocode_city(name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": f"{name}, Myanmar", "format": "json", "limit": 5, "countrycodes": "mm"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if not data:
        return None

    good_types = ["city", "town", "village", "municipality"]

    for match in data:
        if match.get("addresstype") in good_types:
            return {"lat": float(match["lat"]), "lon": float(match["lon"])}

    return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}


def get_road_distance(coord1, coord2):
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1['lon']},{coord1['lat']};{coord2['lon']},{coord2['lat']}"
    params = {"overview": "false"}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("code") != "Ok":
        return None
    meters = data["routes"][0]["distance"]
    return round(meters / 1000, 1)


def straight_line_distance(coord1, coord2):
    return math.hypot(coord1["lat"] - coord2["lat"], coord1["lon"] - coord2["lon"])


def build_nodes():
    nodes = {}
    for city in cities:
        if city in manual_overrides:
            print("using manual override for", city)
            nodes[city] = manual_overrides[city]
            continue

        print("geocoding", city)
        coord = geocode_city(city)
        if coord:
            nodes[city] = coord
        else:
            print("no result for", city)
        time.sleep(1)
    return nodes


def build_edges(nodes, k=3):
    edges = []
    added = set()
    for city in nodes:
        distances = []
        for other in nodes:
            if other != city:
                d = straight_line_distance(nodes[city], nodes[other])
                distances.append((d, other))
        distances.sort()
        nearest = distances[:k]

        for _, other in nearest:
            pair = tuple(sorted([city, other]))
            if pair in added:
                continue
            added.add(pair)

            print("routing", city, "->", other)
            km = get_road_distance(nodes[city], nodes[other])
            time.sleep(1)
            if km is None:
                continue
            edges.append({"from": city, "to": other, "distance_km": km})

    return edges


def find_components(nodes, edges):
    graph = {c: [] for c in nodes}
    for e in edges:
        graph[e["from"]].append(e["to"])
        graph[e["to"]].append(e["from"])

    visited = set()
    components = []
    for start in nodes:
        if start in visited:
            continue
        comp = set()
        stack = [start]
        while stack:
            n = stack.pop()
            if n not in comp:
                comp.add(n)
                visited.add(n)
                stack.extend(graph[n])
        components.append(comp)
    return components


def bridge_components(nodes, edges):
    components = find_components(nodes, edges)
    print("found", len(components), "separate clusters")

    while len(components) > 1:
        comp_a = components[0]
        best = None
        for other_comp in components[1:]:
            for city_a in comp_a:
                for city_b in other_comp:
                    d = straight_line_distance(nodes[city_a], nodes[city_b])
                    if best is None or d < best[0]:
                        best = (d, city_a, city_b)

        _, city_a, city_b = best
        print("bridging cluster gap:", city_a, "->", city_b)
        km = get_road_distance(nodes[city_a], nodes[city_b])
        time.sleep(1)
        if km is not None:
            edges.append({"from": city_a, "to": city_b, "distance_km": km})

        components = find_components(nodes, edges)

    return edges


if __name__ == "__main__":
    nodes = build_nodes()
    edges = build_edges(nodes)
    edges = bridge_components(nodes, edges)

    for city, coord in nodes.items():
        if not (9 <= coord["lat"] <= 29 and 92 <= coord["lon"] <= 102):
            print("SUSPICIOUS (outside Myanmar bounding box):", city, coord)

    map_data = {"nodes": nodes, "edges": edges}

    with open("map_data.json", "w") as f:
        json.dump(map_data, f, indent=2)

    print("done —", len(nodes), "cities,", len(edges), "edges")