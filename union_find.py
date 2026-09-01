from typing import List

class UnionFind:
    def __init__(self, elements: List[str]):
        """Initializes the Union-Find data structure for n elements. Initially,
        each element is in its own set (its parent is itself). The rank (or
        size) of each set is initialized to 0.

        Parameters:
            - elements (List[str]): The list of elements in the Union-Find data
                structure.
        """
        self.parent = {elem: elem for elem in elements}
        self.rank = {elem: 0 for elem in elements}

    def find(self, x: str) -> str:
        """Find the root (or representative) of the set containing the element x.

        Parameters:
            - x (str): The element whose root we want to find.

        Returns:
            - str: The root of the set that contains x.
        """
        parent = self.parent[x]
        if parent == x:
            return parent
        return self.find(parent)

    def union(self, x: str, y: str) -> bool:
        """Union (or merge) the sets containing elements x and y. Return True if
        union was successful. If x and y are already in the same set, do nothing
        (return False).

        Parameters:
            - x (str): The first element (set to be united).
            - y (str): The second element (set to be united).

        Returns:
            - bool: True if x and y are successfully union-ed. False if x and y
                are already in the same set (no union needed).
        """
        x_root = self.find(x)
        y_root = self.find(y)

        # x and y in the same set
        if x_root == y_root:
            return False

        # x and y not in the same set
        if self.rank[x_root] < self.rank[y_root]: # Union x set to y set
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]: # Union y set to x set
            self.parent[y_root] = x_root
        else: # A tie in the ranks, union x set to y set
            self.parent[x_root] = y_root
            self.rank[y_root] = self.rank[x_root] + 1

        return True
