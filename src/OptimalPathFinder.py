from utils import *
from graph_elements import *


class OptimalPathFinder:
    def __init__(self, start: Coordinates = 0, end: Coordinates = 0) -> None:
        """
        :param start: Coordinate object, starting point
        :param end: Coordinate object, ending point
        """
        self.start = start
        self.end = end

    def solve(self) -> (networkx.MultiDiGraph, Route):
        """
        Finds the shortest route between two points in the graph
        :return: a Route object, the shortest on in the graph between the two points
        """

        # Fetching the graph with OSMNX

        print('Downloading graph data...')

        G = load_graph_from_coordinates(self.start, self.end)
        print('Done')
        # Setup

        nodes = get_nodes(G)
        edges = get_edges(G)

        start_node = find_nearest_node(self.start, nodes)
        end_node = find_nearest_node(self.end, nodes)
        start_node.h = get_geo_distance(start_node.coordinates, end_node.coordinates)
        start_node.f = start_node.g + start_node.h
        add_h_to_nodes(nodes, end_node)
        result_node = None

        # A*

        print("Looking for the shortest path...")

        open_list = np.array([start_node], dtype=object)

        while len(open_list) > 0:
            cheapest_node = get_cheapest_node(open_list)
            cheapest_node.has_been_visited = True

            if cheapest_node.id == end_node.id:
                result_node = cheapest_node
                break

            open_list = np.delete(open_list, np.where(open_list == cheapest_node))

            connected_nodes = find_connected_nodes(cheapest_node, nodes, edges)
            for node in connected_nodes:
                if ((not node.has_been_visited and node not in open_list) or
                        node.g > cheapest_node.g + node.time_from_previous_node):
                    node.g = cheapest_node.g + node.time_from_previous_node
                    node.f = node.g + node.h
                    node.previous_node = cheapest_node
                    open_list = np.append(open_list, node)
        shortest_route = recreate_route(result_node)

        print("Done")

        return G, shortest_route
