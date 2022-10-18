import haversine as hs
import numpy as np
import osmnx as ox
import networkx
from matplotlib import pyplot as plt
from graph_elements import *


def load_graph_from_coordinates(start: Coordinates, end: Coordinates) -> networkx.MultiDiGraph:
    """
    Loads a geographical place between two coordinates as a graph
    :param start: starting coordinates of the route
    :param end: ending coordinates of the route
    :return: the graph containing all the intersections as nodes and roads as edges
    """
    G = ox.graph_from_bbox(min(start.lat, end.lat) - .01,
                           max(start.lat, end.lat) + .01,
                           max(start.lon, end.lon) + .01,
                           min(start.lon, end.lon) - .01,
                           network_type='drive',
                           truncate_by_edge=True)
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    return G


def get_nodes(graph: networkx.MultiDiGraph) -> np.ndarray([], dtype=Node):
    """
    Gets all the nodes of a graph in an array
    :param graph: OSMNX graph from which we extract the nodes
    :return: a np array of Node objects
    """
    nodes = np.array([], dtype=object)
    for node in graph.nodes:
        nodes = np.append(nodes, Node(id=node, lat=graph.nodes[node]['y'], lon=graph.nodes[node]['x']))
    return nodes


def get_edges(graph: networkx.MultiDiGraph) -> np.ndarray([], dtype=Edge):
    """
    Gets all the edges of a graph in an array
    :param graph: OSMNX graph from which we extract the edges
    :return: a np array of Edge objects
    """
    edges = np.array([], dtype=object)
    for edge in graph.out_edges(data=True):
        edges = np.append(edges, Edge(edge[0], edge[1], edge[2]['oneway'], edge[2]['length'], edge[2]['travel_time']))
    return edges


def add_h_to_nodes(nodes: np.ndarray, end_node: Node) -> None:
    """
    Adds the travel_time at an average speed between the nodes and the goal point
    :param nodes: array of Node objects, all the nodes in the graph
    :param end_node: Coordinates object
    """
    avg_speed_limit_kmph = 40
    avg_speed_limit_mps = ((avg_speed_limit_kmph * 1000) / 3600)
    for node in nodes:
        node.h = get_geo_distance(node.coordinates, end_node.coordinates) / avg_speed_limit_mps
        node.f = node.h


def find_connected_nodes(node: Node, nodes: np.ndarray([], dtype=Node), edges: np.ndarray([], dtype=Edge)) -> set[Node]:
    """
    Gives all the nodes connected to the node by a single edge, and not being oneway towards the node
    :param node: int, node id from which we search the connected nodes
    :param edges: array of Edge objects, all the edges of the graph
    :param nodes: array of Node objects, all the nodes in the graph
    :return: a set of Node objects, which are all the nodes connected to the node
    """
    connected_nodes = set()
    for edge in edges:
        if not (edge.node_1_id == edge.node_2_id):
            if edge.node_1_id == node.id:  # if the first node of the edge is the current node, a oneway isn't a problem
                new_node = [node for node in nodes if node.id == edge.node_2_id][0]
                new_node.time_from_previous_node = edge.travel_time
                new_node.distance_from_previous_node = edge.length
                connected_nodes.add(new_node)
            elif edge.node_2_id == node.id:
                if not edge.is_oneway:  # if it's the second one we have to make sure it's not oneway
                    new_node = [node for node in nodes if node.id == edge.node_1_id][0]
                    new_node.time_from_previous_node = edge.travel_time
                    new_node.distance_from_previous_node = edge.length
                    connected_nodes.add(new_node)
    return connected_nodes


def find_nearest_node(coordinates: Coordinates, nodes: np.ndarray([], dtype=Node)) -> Node:
    """
    Finds the node of the graph the closest to the coordinates given
    :param coordinates: Coordinate object, from which we want to find the closest node
    :param nodes: np array of Node objects, array of all the nodes of the graph
    :return: a Node object, the closest to the coordinates
    """
    nearest_node = Node(0, 0, 0)
    minimum = 99999999999999
    for node in nodes:
        distance = get_geo_distance(coordinates, node.coordinates)
        if distance < minimum:
            minimum = distance
            nearest_node = node
    return nearest_node


def get_geo_distance(current: Coordinates, goal: Coordinates) -> float:
    """
    Gives the distance between two geographic points
    :param current: Coordinate object of the current position
    :param goal: Coordinate object of the goal position
    :return: a float, the distance between the points in meters
    """
    return hs.haversine((current.lat, current.lon), (goal.lat, goal.lon), unit=hs.Unit.METERS)


def get_cheapest_node(nodes: np.ndarray([], dtype=Node)) -> Node:
    """
    Gets the cheapest node of an array of node, considering their f value
    :param nodes: array of Node objects
    :return: a Node object, the cheapest one
    """
    return min(nodes, key=lambda node: node.f)


def recreate_route(final_node: Node) -> np.ndarray([], dtype=Node):
    """
    Recreates the route took by the algorithm
    :param final_node: Node object, final node of the route
    :return: a Route object, with all the nodes visited in order
    """
    route = Route()
    current_node = final_node
    while current_node:
        route.add_node(current_node)
        current_node = current_node.previous_node
    return route


def draw_graph(G: networkx.MultiDiGraph) -> None:
    """
    Draws the graph with all the nodes and edges as a matplotlib plt
    :param G: OSMNX Graph to draw
    """
    ox.plot_graph(G, show=False, close=False)


def draw_edge(node1: Node, node2: Node, color: str = "r") -> None:
    """
    Draws an edge of the graph plot as a straight line
    :param node1: Node object
    :param node2: Node object
    :param color: char, color of the edge, red by default
    """
    plt.plot((node1.coordinates.lon, node2.coordinates.lon),
             (node1.coordinates.lat, node2.coordinates.lat), c=color)


def draw_node(node: Node, color: str = 'r') -> None:
    """
    Draws a node on the graph plot as a dot
    :param node: Node object we want to draw
    :param color: char, color of the dot, red by default
    """
    plt.plot(node.coordinates.lon, node.coordinates.lat, c=color, marker="o")


def draw_route(route: Route, color: str = 'r') -> None:
    """
    Draws a route on the graph plot
    :param route: Route object, containing all the nodes visited
    :param color: char, color of the drawn route
    """
    for i in range(0, len(route.nodes_visited) - 1):
        draw_edge(route.nodes_visited[i], route.nodes_visited[i + 1], color)
