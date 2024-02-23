from heapq import heappush, heappop

class Node:
    def __init__(self, id, distance, parent=None):
        self.id = id
        self.distance = distance
        self.parent = parent

    def __lt__(self, other):
        return self.distance < other.distance

class Graph:
    def __init__(self, nodes, edges, weights):
        self.nodes = nodes
        self.edges = edges
        self.weights = weights

    def get_neighbors(self, node_id):
        return [n for n, w in self.edges[node_id]]

    def get_weight(self, node1_id, node2_id):
        return self.weights[(node1_id, node2_id)]

def dijkstra(graph, start, end, priority_level):
    visited = set()
    pq = []
    heappush(pq, Node(start, 0))

    while pq:
        current = heappop(pq)
        if current.id == end:
            return reconstruct_path(current)

        if current.id in visited:
            continue

        visited.add(current.id)

        for neighbor in graph.get_neighbors(current.id):
            if neighbor in visited:
                continue

            new_distance = current.distance + graph.get_weight(current.id, neighbor)
            if priority_level >= 2 and neighbor in graph.traffic_lights:
                new_distance -= graph.get_weight(current.id, neighbor)  # Account for opening traffic light
            elif priority_level >= 1 and neighbor in graph.traffic_lights:
                new_distance -= graph.get_weight(current.id, neighbor) / 2  # Account for partial opening

            if not any(node.id == neighbor and node.distance <= new_distance for node in pq):
                heappush(pq, Node(neighbor, new_distance, current))

    return None  # No path found

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.id)
        node = node.parent
    path.reverse()
    return path

# Example usage
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
edges = {
    'A': [('B', 1), ('C', 2)],
    'B': [('C', 3), ('D', 4)],
    'C': [('D', 1), ('E', 5)],
    'D': [('E', 2), ('F', 6)],
    'E': [('F', 3), ('G', 4)],
    'F': [('G', 1), ('H', 2)],
    'G': [('H', 3)],
    'H': [],
}
weights = {(a, b): w for a, b, w in [(a, b, w) for a in nodes for b, w in edges[a]]}
graph = Graph(nodes, edges, weights)
graph.traffic_lights = {'B', 'D', 'F'}  # Set of intersections with traffic lights

start = 'A'
end = 'H'
priority_level = 2

path = dijkstra(graph, start, end, priority_level)

if path:
    print("Shortest path:", path)
else:
    print("No path found")
