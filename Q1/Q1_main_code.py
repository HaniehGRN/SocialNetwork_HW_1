#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx

#--------------------- define parameters ---------------------

# G1, pos1 = Graph.ring_lattice(1000, 2)
start_node_num = 500
end_node_num = 5000
point_num = 200

#--------------------- generate N logarithmically ---------------------

node_num_vector = np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_num))).astype(int)
# print(f"Testing N values (log base 10): {node_num_vector}")

graph = Graph()
G, pos = graph.random_network(2000, 4)
# G, pos = graph.ring_lattice(1000, 2)
# G, pos = graph.square_Lattice(100, 20)
# G, pos = graph.cubic_grid_Lattice(10, 20, 30, False)

def calculate_shortest_path(G, shortest_path_sample):

    # ensure calculating shortest path on a connected graph
    largest_cc_nodes = max(nx.connected_components(G), key=len)
    giant_component = G.subgraph(largest_cc_nodes).copy()
    N = giant_component.number_of_nodes()
    if N == 0:
        return np.nan

    nodes = list(giant_component.nodes())
    sources = np.random.choice(nodes, size=shortest_path_sample, replace=False)
    print(sources)
    average_shortest_path_length = 0
    total_distance = 0
    total_paths = 0
    for source in sources:
        lengths = nx.shortest_path_length(G, source=source)
        # print(lengths)
        for dist in lengths.values():
            if dist > 0:
                total_distance += dist
                total_paths += 1
    if total_paths == 0:
        return np.nan
    average_shortest_path_length = total_distance / total_paths
    return average_shortest_path_length


print(calculate_shortest_path(G, 400))




