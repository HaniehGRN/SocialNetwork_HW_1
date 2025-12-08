#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx
import math
import random

#--------------------- define parameters ---------------------

start_node_num = 500
end_node_num = 5000
point_count = 5

#--------------------- define variables ---------------------

average_distance_ring_lattice = []
average_distance_square_lattice = []
average_distance_cubic_lattice = []
average_distance_random_network = []

#--------------------- define functions ---------------------

def calculate_average_shortest_path(G, shortest_path_sample_size):
    # ensure calculating shortest path on a connected graph
    largest_cc_nodes = max(nx.connected_components(G), key=len)
    giant_component = G.subgraph(largest_cc_nodes).copy()
    N = giant_component.number_of_nodes()
    if N == 0:
        return np.nan
    # print(shortest_path_sample_size)
    if N < shortest_path_sample_size:
        shortest_path_sample_size = N

    nodes = list(giant_component.nodes())
    # print(nodes)
    sources = random.sample(nodes, shortest_path_sample_size)
    # print(sources)
    total_distance = 0
    total_paths = 0
    for source in sources:
        lengths = nx.shortest_path_length(G, source=source)
        # print(lengths)
        # print(lengths.values())
        for dist in lengths.values():
            if dist > 0:
                total_distance += dist
                total_paths += 1
    if total_paths == 0:
        return np.nan
    # print(average_shortest_path_length)
    return total_distance / total_paths

def calculate_average_distance_per_node_num_ring_lattice(G, node_num, graph_sample_size):
    G_ring_lattice, pos = G.ring_lattice(node_num)
    temp = calculate_average_shortest_path(G_ring_lattice, graph_sample_size)
    average_distance_ring_lattice.append(calculate_average_shortest_path(G_ring_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_square_lattice(G, node_num, graph_sample_size):
    Lx = int(math.floor(math.sqrt(node_num)))
    Ly = int(math.ceil(node_num / Lx))
    G_square_lattice, pos = G.square_Lattice(Lx, Ly)
    average_distance_square_lattice.append(calculate_average_shortest_path(G_square_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_cubic_lattice(G, node_num, graph_sample_size):
    Lx = int(node_num ** (1 / 3))
    Ly = int(math.sqrt(node_num / Lx))
    Lz = int(math.ceil(node_num / (Lx * Ly)))
    G_cubic_lattice, pos = G.cubic_grid_Lattice(Lx, Ly, Lz, False)
    average_distance_cubic_lattice.append(calculate_average_shortest_path(G_cubic_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_random_network(G, node_num, graph_sample_size, k_avg):
    G_random_network, pos = G.random_network(node_num, k_avg)
    average_distance_random_network.append(calculate_average_shortest_path(G_random_network, graph_sample_size))

#--------------------- generate N logarithmically ---------------------

node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_count))).astype(int))
# print(f"Testing N values (log base 10): {node_num_vector}")

instance_graph = Graph()

for node_num in node_num_vector:
    graph_sample_size = node_num
    if node_num > 3000:
        graph_sample_size = 0.5 * node_num # to keep runtime low
    calculate_average_distance_per_node_num_ring_lattice(instance_graph, node_num, graph_sample_size)
    calculate_average_distance_per_node_num_square_lattice(instance_graph, node_num, graph_sample_size)
    calculate_average_distance_per_node_num_cubic_lattice(instance_graph, node_num, graph_sample_size)
    calculate_average_distance_per_node_num_random_network(instance_graph, node_num, graph_sample_size, 4)


# calculate_average_distance_per_node_num_ring_lattice(instance_graph, 589, 300)
# calculate_average_distance_per_node_num_square_lattice(instance_graph, 589, 300)
# calculate_average_distance_per_node_num_cubic_lattice(instance_graph, 589, 300)
# calculate_average_distance_per_node_num_random_network(instance_graph, 589, 300, 4)
print(average_distance_random_network)
print(average_distance_square_lattice)
print(average_distance_cubic_lattice)
print(average_distance_ring_lattice)
# G_ring_lattice, pos = graph_instance.ring_lattice(1000)
# print(G_ring_lattice)
# print(calculate_average_shortest_path(G_ring_lattice, 1000))
# G_random_network, pos = graph_instance.random_network(5000, 4)
# print(G_random_network)
# print(calculate_average_shortest_path(G_random_network, 500))
#
# G_ring_lattice, pos = instance_graph.ring_lattice(1000)
# print(G_ring_lattice)
# print(calculate_average_shortest_path(G_ring_lattice, 1000))
#
# G_cubic_lattice, pos = instance_graph.cubic_grid_Lattice(10, 10, 10, False)
# print(G_cubic_lattice)
# print(calculate_average_shortest_path(G_cubic_lattice, 1000))
#
# G_square_lattice, pos = instance_graph.square_Lattice(500, 10)
# print(calculate_average_shortest_path(G_square_lattice, 500))
#





