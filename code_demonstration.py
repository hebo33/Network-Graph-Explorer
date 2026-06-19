from typing import List, Dict, Tuple, Optional, Callable
class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        name (str): The label or identifier of the vertex.
        children (Dict[str, Tuple[str, str, float]]):
            A mapping between child vertex names and edges.
            Each edge is represented as a tuple:
                (source vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None):
        """
        Initializes a Vertex.
a
        Args:
            name (str): The label or identifier of the vertex.
            children (Optional[Dict[str, Tuple[str, str, float]]]):
                A mapping between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """
        Returns all edges from this vertex.

        Returns:
            List[Tuple[str, str, float]]: The list of edges from this vertex.
        """

        l = []
        for key in self.children:
            l.append(self.children[key])
        return l


class Graph:
    """
    Represents a graph consisting of multiple vertices.

    Attributes:
        vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """
        Initializes a Graph.

        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """
        Returns all vertices in the graph.

        Returns:
            List[Vertex]: The list of vertices in the graph.
        """
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """
        Checks if vertex v_name is a child of vertex u_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the potential child vertex.

        Returns:
            bool: True if the vertex v_name is a child of the vertex u_name, False otherwise.
        """
        for vertex in self.vertices:  # Find vertex u
            if vertex.name == u_name:
                return v_name in vertex.children  # Find v by key name

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """
        Retrieves the edge between u_name and v_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the child vertex.

        Returns:
            Optional[Tuple[str, str, float]]: The edge if it exists,
            or None if no such edge is found.
        """
        # Check u parent v child
        for vertex in self.vertices:
            if vertex.name == u_name:
                if v_name in vertex.children:
                    return vertex.children[v_name]  # Found edge

        return None  # Did not find edge

    def add_vertex(self, v: Vertex) -> None:
        """Add vertex v to the Graph.

        Args:
            v (Vertex): The vertex needs to be added to the Graph.
        """
        self.vertices.append(v)


class Device(Vertex):
    """
    Represents a network device, extending the Vertex class with
    device-specific functionality.

    Attributes:
        name (str): The label or identifier of the device.
        children (Dict[str, Tuple[str, str, float]]):
            A mapping between child device names and nearby devices.
        network (Graph): A graph representing this device's discovered network.
    """

    def __init__(self, name: str):
        """
        Initializes a Device.

        Args:
            name (str): The label or identifier of the device.
        """
        Vertex.__init__(self, name)
        self.network = Graph([])

    def discover_network(self, find_devices_fn: Callable[[List[str]], List[Tuple[str, str, float]]]) -> None:
        """
        Discovers the surrounding network starting from this device. Once this
        function is called, self.network should contain a representation of the
        device's discovered network.

        Args:
            find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]):
                A function that takes an ordered list of device names (i.e., a path)
                and returns the edges from the last device in the path to its immediate children.
        """
        path = [self.name]  # Initial path
        self.network = Graph([])  # Initial network
        self.network.add_vertex(self)  # Add this device to network

        # Explore network
        self.discover_network_helper(find_devices_fn, path)

    def discover_network_helper(self,
                                find_devices_fn: Callable[[List[str]],
                                List[Tuple[str, str, float]]],
                                path: List[str]) -> None:
        """Discover the network by calling find_devices_fn recursively on path.

        Args:
            find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]):
            A function that takes an ordered list of device names (i.e., a path)
            and returns the edges from the last device in the path to its
            immediate children.
            path (List[str]): A list of names of the Device.
        """
        children = find_devices_fn(path)  # Immediate children

        if not children:  # No child
            return None

        last_device_name = path[-1]
        last_device = None

        # Find device of the last node
        for v in self.network.vertices:
            if v.name == last_device_name:
                last_device = v
                break

        # Did not find device of the last node
        if last_device is None:
            return None

        # There exists children & Add children to network
        for child in children:
            in_network = False
            for v in self.network.vertices:
                if v.name == child[1]:
                    in_network = True

            if in_network is True:
                existing_edge = last_device.children.get(child[1])
                if existing_edge is None or existing_edge[2] > child[2]:
                    last_device.children[child[1]] = child
                continue

            if in_network is False:  # Child not in the network & Add to network
                new_device = Device(child[1])
                self.network.add_vertex(new_device)

            # Add this child to current device's children dictionary
            last_device.children[child[1]] = child

            # Investigate current child
            path.append(child[1])

            self.discover_network_helper(find_devices_fn, path)

            path.pop()


    def find_path(self, d_name: str) -> Optional[List[str]]:
        """
        Finds the cheapest path from this device to the specified target device
        using the Cheapest-First Search (CFS) algorithm.

        Args:
            d_name (str): The name of the destination device.

        Returns:
            Optional[List[str]]: An ordered list of device names representing the path
            from this device to the target. If no path exists, returns None.
        """
        path =  self.cheapest_first_search(d_name, [[(self.name,), 0]], [])
        if path is None:
            return None
        return list(path[0])

    def cheapest_first_search(self, dst: str, o_set: List[list],
                              c_set: List[str]) -> Optional[list]:
        """Return the cheapest path from this device to destination device dst.
        This is the helper method for Device.find_path.

        Args:
            dst (str): The name of the destination device.
            o_set (List[Tuple[str, str, str], float]): All undiscovered paths.
            c_set (str): Set of all discovered vertex's names.

        Returns:
            Optional[List[Tuple, float]]: List contains the cheapest path from
            this device to the destination device dst, and the weight of the
            path. If no path exists, return None.
        """
        # This device does not have child
        if not o_set:
            return None

        curr = o_set.pop(0)  # Withdrawal

        # Check if curr contains the path we wanted
        if curr[0][-1] == dst:
            return curr

        c_set.append(curr[0][-1])  # record visited device

        # Find curr[0][-1] in network to access its children
        for device in self.network.vertices:
            if device.name == curr[0][-1]:

                # Case: Last node has no child
                if device.children == {}:
                    break

                # Case: Last node has children
                children_lst = []
                for key in device.children:
                    children_lst.append(device.children[key])
                children_lst.sort(key=lambda x: x[2])  # Sort children_lst by weight
                for child in children_lst:
                    if child[1] not in c_set:
                        o_set.append([curr[0] + (child[1],), curr[1] + child[-1]])

                # Resort the open set
                o_set.sort(key=lambda x: x[1])

        return self.cheapest_first_search(dst, o_set, c_set)

# ----------------------------------------------------------------------
# Mock function for testing
# ----------------------------------------------------------------------
def find_devices_fn(path: List[str]) -> List[Tuple[str, str, float]]:
    """
    A mock function that simulates network discovery.

    Args:
        path (List[str]): The sequence of device names representing the discovery path.

    Returns:
        List[Tuple[str, str, float]]: A list of edges, where each tuple contains:
            - source device name (str),
            - child device name (str),
            - edge weight (float).
    """
    if not path:
        return []

    last_device = path[-1]

    mock_network = {
        "chandra-s25": [
            ("chandra-s25", "router-051797", 1.0),
            ("chandra-s25", "helen-pc", 2.0),
        ],
        "router-051797": [
            ("router-051797", "ws-102", 1.2),
            ("router-051797", "switch-12", 0.8),
            ("router-051797", "srv-07", 1.0),
        ],
        "helen-pc": [
            ("helen-pc", "ws-14", 1.5),
        ],
    }

    return mock_network.get(last_device, [])
