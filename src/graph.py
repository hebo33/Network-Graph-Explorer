from typing import List, Dict, Tuple, Optional, Callable

class Vertex:
    """Generate a vertex in a graph. Represents a device in a computer network.

    Attributes:
        - name (str): The label of the vertex.
        - children (Dict[str, Tuple[str, str, float]]): A mapping between child
            vertex names and edges. Each edge is represented as a tuple: (source
            vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str,
    Tuple[str, str, float]]] = None):
        """Initializes a Vertex.

        Parameters:
            - name (str): The label or identifier of the vertex.
            - children (Optional[Dict[str, Tuple[str, str, float]]]): A mapping
                between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] \
            = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """Returns all edges from this vertex.

        Returns:
            - List[Tuple[str, str, float]]: The list of edges from this vertex.
        """

        l = []
        for key in self.children:
            l.append(self.children[key])
        return l


class Graph:
    """Represents a graph consisting of multiple vertices. Simulates a computer
    network.

    Attributes:
        - vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """Initializes a Graph.

        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """Returns all vertices in the graph.

        Returns:
            - List[Vertex]: The list of vertices in the graph.
        """
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """Checks if vertex v_name is a child of vertex u_name.

        Parameters:
            - u_name (str): The name of the parent vertex.
            - v_name (str): The name of the potential child vertex.

        Returns:
            - bool: True if the vertex v_name is a child of the vertex u_name,
                False otherwise.
        """
        for vertex in self.vertices:
            if vertex.name == u_name:
                return v_name in vertex.children

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """ Retrieves the edge between u_name and v_name.

        Parameters:
            - u_name (str): The name of the parent vertex.
            - v_name (str): The name of the child vertex.

        Returns:
            - Optional[Tuple[str, str, float]]: The edge if it exists, or None
                if no such edge is found.
        """
        for vertex in self.vertices:
            if vertex.name == u_name:
                if v_name in vertex.children:
                    return vertex.children[v_name]

        return None

    def add_vertex(self, v: Vertex) -> None:
        """Add vertex v to the Graph.

        Parameters:
            - v (Vertex): The vertex needs to be added to the Graph.
        """
        self.vertices.append(v)

