from typing import List, Tuple

from src.graph import Graph
from src.union_find import UnionFind

# Function to implement Kruskal's algorithm
def kruskal_mst(graph: Graph) -> List[Tuple[str, str, float]]:
    """Kruskal's Algorithm for Minimum Spanning Tree (MST).

    Parameters:
        - graph (Graph): The graph for which we compute the MST.

    Returns:
        - List[Tuple[str, str, float]]: A list of edges in the MST.
        - Each edge is represented as a tuple (source vertex, destination
            vertex, weight).
    """

    result = []  # The final MST placeholder

    # Step 1: Get edge list
    edge_lst0 = []

    vertices = graph.get_vertices()
    for v in vertices:
        # v.children is a dict mapping name -> edge tuple
        for edge in v.children.values():
            edge_lst0.append(edge)

    # Step 2: Sort edges by weight
    edge_lst1 = []

    if not edge_lst0:
        return edge_lst1

    # Simple selection-sort style
    while edge_lst0:
        smallest = edge_lst0[0]
        for edge in edge_lst0:
            if edge[2] <= smallest[2]:
                smallest = edge
        edge_lst0.remove(smallest)
        edge_lst1.append(smallest)

    # Step 3: Initialize Union-Find data structures
    v_names = [v.name for v in vertices]
    union_find = UnionFind(v_names)

    # Step 4: Iterate over the sorted edges to build MST
    for edge in edge_lst1:
        if union_find.find(edge[0]) != union_find.find(edge[1]):
            result.append(edge)
            union_find.union(edge[0], edge[1])

        if len(result) == len(v_names) - 1:
            return result

    return result

    # Suggested steps for Kruskal MST
    # Step 1: Get edge list
    # Step 2: Sort edges by weight
    # Step 3: Initialize Union-Find data structures
    # (to track the connected sets of vertices as we add edges to the MST)
    # Step 4: Iterate over the sorted edges to build MST

# Function to implement Prim's algorithm
def prim_mst(graph: Graph) -> List[Tuple[str, str, float]]:
    """Prim's Algorithm for Minimum Spanning Tree (MST).

    Parameters:
        - graph (Graph): The graph for which we compute the MST.

    Returns:
        - List[Tuple[str, str, float]]: A list of edges in the MST. Each edge is
            represented as a tuple (source vertex, destination vertex, weight).
    """

    result = []  # The final MST
    vertices = graph.get_vertices()

    # Step 1: Pick starting vertex
    # Step 1 (a): Empty graph
    if not vertices:
        return result
    # Step 1 (b): Single vertex graph
    if len(vertices) == 1:
        return result
    # Step 1 (c): Regular graph with >= 2 vertices

    # Step 2: Get starting node edges
    start_vertex = vertices[0]
    o_set = [edge for edge in start_vertex.children.values()]  # outgoing edges
    c_set = [start_vertex.name]  # visited set (names only)

    # Step 3–4: Continue until MST has |V| - 1 edges
    while len(result) < len(vertices) - 1:

        # Open set empty → no MST possible
        if not o_set:
            return result

        # Find the smallest edge in o_set
        smallest = o_set[0]
        for edge in o_set:
            if edge[2] <= smallest[2]:
                smallest = edge

        # Remove the smallest edge from open set
        o_set.remove(smallest)

        u, v, w = smallest

        # Skip if destination is already visited (prevents cycle)
        if v in c_set:
            continue

        # Accept this edge
        result.append(smallest)
        c_set.append(v)

        # Add all outgoing edges from vertex v
        for vertex in vertices:
            if vertex.name == v:
                for edge in vertex.children.values():
                    if edge[1] not in c_set:
                        o_set.append(edge)

    return result
