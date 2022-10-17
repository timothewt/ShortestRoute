import networkx
from utils import *
from graph_elements import *


def find_shortest_path_a_star(start_coords: Coordinates, end_coords: Coordinates) -> (networkx.MultiDiGraph, Route):
    """
    Finds the shortest route between two points in the graph
    :param start_coords: Coordinate object, starting point
    :param end_coords: Coordinate object, ending point
    :return: a Route object, the shortest on in the graph between the two points
    """

    # Fetching the graph with OSMNX

    print('Downloading graph data...')

    G = ox.graph_from_bbox(min(start.lat, end.lat) - .01,
                           max(start.lat, end.lat) + .01,
                           max(start.lon, end.lon) + .01,
                           min(start.lon, end.lon) - .01,
                           network_type='drive',
                           truncate_by_edge=True)
    print('Done')
    # Setup

    nodes = get_nodes(G)
    edges = get_edges(G)

    start_node = find_nearest_node(start_coords, nodes)
    end_node = find_nearest_node(end_coords, nodes)
    start_node.h = get_geo_distance(start_node.coordinates, end_node.coordinates)
    start_node.f = start_node.g + start_node.h
    add_h_to_nodes(nodes, end_node.coordinates)
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

        connected_nodes = find_connected_nodes(cheapest_node.id, nodes, edges)
        for node in connected_nodes:
            if ((not node.has_been_visited and node not in open_list) or
                    node.g > cheapest_node.g + node.distance_from_previous_node):
                node.g = cheapest_node.g + node.distance_from_previous_node
                node.f = node.g + node.h
                node.previous_node = cheapest_node
                open_list = np.append(open_list, node)
    shortest_route = recreate_route(result_node)

    print("Done")

    return G, shortest_route


if __name__ == "__main__":
    
    start = Coordinates(47.6410128490741, 6.840331318378322)
    end = Coordinates(47.622006728330945, 6.862548058433361)

    graph, route = find_shortest_path_a_star(start, end)
    draw_graph(graph)
    draw_route(route)
    draw_node(Node(0, start.lat, start.lon), color="g")
    draw_node(Node(0, end.lat, end.lon), color="b")
    plt.show()
