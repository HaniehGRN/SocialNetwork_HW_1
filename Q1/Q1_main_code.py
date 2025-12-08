#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx
import math

#--------------------- define parameters ---------------------

start_node_num = 500
end_node_num = 5000
point_num = 200

#--------------------- define variables ---------------------

average_distance = {
    "d_ring_lattice" : [],
    "d_square_lattice" : [],
    "d_cubic_lattice" : [],
    "d_random_network": []
}

#--------------------- define functions ---------------------

def calculate_average_shortest_path(G, shortest_path_sample):

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

def calculate_average_distance_per_node_num_ring_lattice(G, node_num, graph_sample_size):
    G_ring_lattice, pos = G.ring_lattice(node_num)
    average_distance["d_ring_lattice"].append(calculate_average_shortest_path(G_ring_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_square_lattice(G, node_num, graph_sample_size):
    Lx = int(math.floor(math.sqrt(node_num)))
    Ly = int(math.ceil(node_num / Lx))
    G_square_lattice, pos = G.square_lattice(Lx, Ly)
    average_distance["d_square_lattice"].append(calculate_average_shortest_path(G_square_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_cubic_lattice(G, node_num, graph_sample_size):
    Lx = int(node_num ** (1 / 3))
    Ly = int(math.sqrt(node_num / Lx))
    Lz = int(math.ceil(node_num / (Lx * Ly)))
    G_cubic_lattice = G.cubic_lattice(Lx, Ly, Lz)
    average_distance["d_cubic_lattice"].append(calculate_average_shortest_path(G_cubic_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_random_network(G, node_num, graph_sample_size):


#--------------------- generate N logarithmically ---------------------

node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_num))).astype(int))
print(f"Testing N values (log base 10): {node_num_vector}")

graph_sample = Graph()
# G, pos = graph.random_network(2000, 4)
# # G, pos = graph.ring_lattice(1000, 2)
# # G, pos = graph.square_Lattice(100, 20)
# # G, pos = graph.cubic_grid_Lattice(10, 20, 30, False)
# print(calculate_average_shortest_path(G, sample_size=200))

for node_num in node_num_vector:
    graph_sample_size = 0.7 * node_num  # to keep runtime low
    G_ring_lattice, pos = graph_sample.ring_lattice(node_num)
    average_distance["d_ring_lattice"].append(calculate_average_shortest_path(G_ring_lattice, graph_sample_size))





