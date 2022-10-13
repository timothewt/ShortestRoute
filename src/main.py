from utils import *
from graph_elements import *


def find_shortest_path_a_star(G, start_coords: Coordinates, end_coords: Coordinates):
    """
    Finds the shortest route between two points in the graph
    :param G: OSMNX Graph
    :param start_coords: Coordinate object, starting point
    :param end_coords: Coordinate object, ending point
    :return: a Route object, the shortest on in the graph between the two points
    """
    print("Looking for the shortest path..")
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
    return shortest_route


if __name__ == "__main__":
    ox.settings.use_cache = True

    G = ox.load_graphml('./data/sonora.graphml')

    start = Coordinates(30.57860, -100.64240)
    end = Coordinates(30.57283, -100.62984)

    draw_graph(G)
    route = find_shortest_path_a_star(G, start, end)
    draw_route(route)
    plt.show()
