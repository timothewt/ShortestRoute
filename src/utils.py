import haversine as hs
import osmnx as ox
from matplotlib import pyplot as plt
from graph_elements import *


def get_nodes(graph):
    """
    Gets all the nodes of a graph in an array
    :param graph: OSMNX graph from which we extract the nodes
    :return: a np array of Node objects
    """
    nodes = np.array([], dtype=object)
    for node in graph.nodes:
        nodes = np.append(nodes, Node(id=node, lat=graph.nodes[node]['y'], lon=graph.nodes[node]['x']))
    return nodes


def get_edges(graph):
    """
    Gets all the edges of a graph in an array
    :param graph: OSMNX graph from which we extract the edges
    :return: a np array of Edge objects
    """
    edges = np.array([], dtype=object)
    for edge in graph.out_edges(data=True):
        edges = np.append(edges, Edge(edge[0], edge[1], edge[2]['length']))
    return edges


def add_h_to_nodes(nodes, end_coordinates):
    """
    Adds the geo-distance between the nodes and the goal point
    :param nodes: array of Node objects, all the nodes in the graph
    :param end_coordinates: Coordinates object
    """
    for node in nodes:
        node.h = get_geo_distance(node.coordinates, end_coordinates)
        node.f = node.h


def find_connected_nodes(node_id: int, nodes, edges):
    """
    Gives all the nodes connected to the node of id 'node_id' by a single edge
    :param node_id: int, node id from which we search the connected nodes
    :param edges: array of Edge objects, all the edges of the graph
    :param nodes: array of Node objects, all the nodes in the graph
    :return: a set of Node objects, which are all the nodes connected to the node of id 'node_id'
    """
    connected_nodes = set()
    for edge in edges:
        if edge.node_1_id == node_id or edge.node_2_id == node_id:
            new_node_id = [id for id in [edge.node_1_id, edge.node_2_id] if id != node_id][0]
            new_node = [node for node in nodes if node.id == new_node_id][0]
            new_node.distance_from_previous_node = edge.length
            connected_nodes.add(new_node)
    return connected_nodes


def find_nearest_node(coordinates, nodes) -> Node:
    """
    Finds the node of the graph the closest to the coordinates given
    :param coordinates: Coordinate object, from which we want to find the closest node
    :param nodes: np array of Node objects, array of all the nodes of the graph
    :return: a Node object, the closest to the coordinates
    """
    nearest_node = Node(0, 0, 0)
    minimum = 100000000000000
    for node in nodes:
        diff = pow(abs(coordinates.lat - node.coordinates.lat), 2) + pow(abs(coordinates.lon - node.coordinates.lon), 2)
        if diff < minimum:
            minimum = diff
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


def get_cheapest_node(nodes) -> Node:
    """
    Gets the cheapest node of an array of node, considering their f value
    :param nodes: array of Node objects
    :return: a Node object, the cheapest one
    """
    return min(nodes, key=lambda node: node.f)


def recreate_route(final_node):
    """
    Recreates the route took by the algorithm
    :param final_node: Node object, final node of the route
    :return: a Route object, with all the nodes visited in order
    """
    route = Route()
    current_node = final_node
    while current_node.previous_node:
        route.add_node(current_node)
        current_node = current_node.previous_node
    return route


def draw_graph(G):
    """
    Draws the graph with all the nodes and edges as a matplotlib plt
    :param G: OSMNX Graph to draw
    :return the elements of the plot
    """
    fig, ax = ox.plot_graph(G, show=False, close=False)
    return fig, ax


def draw_edge(node1: Node, node2: Node, color="r"):
    """
    Draws an edge of the graph plot as a straight line
    :param node1: Node object
    :param node2: Node object
    :param color: char, color of the edge, red by default
    """
    plt.plot((node1.coordinates.lon, node2.coordinates.lon),
             (node1.coordinates.lat, node2.coordinates.lat), c=color)


def draw_node(node: Node, color='r'):
    """
    Draws a node on the graph plot as a dot
    :param node: Node object we want to draw
    :param color: char, color of the dot, red by default
    """
    plt.plot(node.coordinates.lon, node.coordinates.lat, c=color, marker="o")


def draw_route(route: Route, color='r'):
    """
    Draws a route on the graph plot
    :param route: Route object, containing all the nodes visited
    :param color: char, color of the drawn route
    """
    for i in range(0, len(route.nodes_visited) - 1):
        draw_edge(route.nodes_visited[i], route.nodes_visited[i + 1], color)
