from typing import List, Tuple, Optional, Callable

from src.graph import Vertex, Graph
from src.shortest_path import cheapest_first_search

class Device(Vertex):
    """Represents a real-world network device, extending the Vertex class with
    device-specific functionality.

    Attributes:
        - name (str): The label of the device.
        - children (Dict[str, Tuple[str, str, float]]): A mapping between child
            device names and nearby devices.
        - network (Graph): A graph representing this device's discovered network.
    """

    def __init__(self, name: str):
        """Initializes a Device.

        Parameters:
            - name (str): The label of the device.
        """
        Vertex.__init__(self, name)
        self.network = Graph([])

    def discover_network(self, find_devices_fn: Callable[[List[str]],
    List[Tuple[str, str, float]]]) -> None:
        """Discovers the surrounding network starting from this device. Once this
        function is called, self.network should contain a representation of the
        device's discovered network.

        Parameters:
            - find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]):
                A function that takes an ordered list of device names(i.e., a path)
                and returns the edges from the last device in the path to its
                immediate children.
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
        It looks for possible devices that are connecged the to last device in
        the given path.

        Parameters:
            - find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]):
                A function that takes an ordered list of device names (i.e., a
                path) and returns the edges from the last device in the path to
                its immediate children.
            - path (List[str]): A list of names of the Device.
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
        """Finds the cheapest path from this device to the specified target device
        using the Cheapest First Search (CFS) algorithm.

        Parameter:
            - d_name (str): The name of the destination device.

        Returns:
            Optional[List[str]]: An ordered list of device names representing the
                path from this device to the target. If no path exists, returns
                None.
        """
        path = self.cheapest_first_search(d_name, [[(self.name,), 0]], [])
        if path is None:
            return None
        return list(path[0])
