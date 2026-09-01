from typing import List, Optional

from src.graph import Graph

def cheapest_first_search(self, dst: str, o_set: List[list],
                          c_set: List[str]) -> Optional[list]:
    """Return the cheapest path from this device to destination device dst.
    This is the helper method for Device.find_path.

    Parameters:
        - dst (str): The name of the destination device.
        - o_set (List[Tuple[str, str, str], float]): All undiscovered paths.
        - c_set (str): Set of all discovered vertex's names.

    Returns:
        - Optional[List[Tuple, float]]: List contains the cheapest path from
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
