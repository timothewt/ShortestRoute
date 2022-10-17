import numpy as np


class Coordinates:
    """
    Used to indicate the geographical coordinates (latitude and longitude) of an element in the graph
    ----
    Attributes:
        lat: float
            Latitude
        lon: float
            Longitude
    """

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def __str__(self) -> str:
        return f"(Lat: {self.lat}, Lon: {self.lon})"


class Node:
    """
    Used to represent a node of the graph
    ----
    Attributes:
        id: int
            OSMNX id of the node
        coordinates: Coordinates object
            Geographical coordinates of the node
        has_been_visited: boolean
            Indicates if the node has been visited when looking for a route
        previous_node: float
            Distance from the previous node in the route
        previous_node: Node object
            Previous node of the route using this node
        h: float
            Evaluation of the remaining distance to reach the goal node
        g: float
            Distance travelled from the starting node of the route, which is the cost of the route
        f: float
            f = g + h, evaluate the cost of the route from this node to the goal node
    """

    def __init__(self, id: int, lat: float, lon: float) -> None:
        self.id = id
        self.coordinates = Coordinates(lat, lon)
        self.has_been_visited = False
        self.distance_from_previous_node = 0.0
        self.previous_node = None
        self.h = 0.0
        self.g = 0.0
        self.f = 0.0

    def __str__(self) -> str:
        return f"-----Node-----\n" \
               f"id: {self.id}\n" \
               f"Coordinates: {self.coordinates}\n" \
               f"Has been visited: {self.has_been_visited}\n" \
               f"f: {self.f}\n"


class Edge:
    """
    Used to represent an edge of the graph
    ----
    Attributes:
        node_1_id: Node object
            First node connected by the edge
        node_2_id: Node object
            Second node connected by the edge
        is_oneway: bool
            Indicates if the edge can only be taken from node_1 to node_2 but not from node_2 to node_1
        length: float
            Length of the edge
    """

    def __init__(self, node_1_id: int, node_2_id: int, is_oneway: bool, length: float) -> None:
        self.node_1_id = node_1_id
        self.node_2_id = node_2_id
        self.is_oneway = is_oneway
        self.length = length

    def __str__(self) -> str:
        return f"-----Edge-----\n" \
               f"Node 1: {self.node_1_id}\n" \
               f"Node 2: {self.node_2_id}\n" \
               f"Oneway: {self.is_oneway}\n" \
               f"Length: {self.length}\n"


class Route:
    """
    Used to represent a route in the graph
    ----
    Attributes:
        nodes_visited: array of Node objects
            Nodes visited that constitute the route
        distance_travelled: float
            Total distance travelled during the route
    """

    def __init__(self, final_node: Node = None, distance_travelled: float = 0.0) -> None:
        self.nodes_visited = np.empty((0, 1), dtype=object)
        if final_node:
            self.add_node(final_node)
        self.distance_travelled = distance_travelled

    def __str__(self) -> str:
        nodes_visited_by_id = []
        for node in self.nodes_visited:
            nodes_visited_by_id.append(node.id)
        return f"-----Route-----\n" \
               f"Nodes visited: {nodes_visited_by_id}\n" \
               f"Length: {self.distance_travelled}\n"

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the route
        :param node: Node object
        """
        self.nodes_visited = np.append(self.nodes_visited, node)
