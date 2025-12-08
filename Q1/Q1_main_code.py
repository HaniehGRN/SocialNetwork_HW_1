#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx
import math
import random
import matplotlib.pyplot as plt

#--------------------- define parameters ---------------------

start_node_num = 500
end_node_num = 5000
point_count = 10

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

    if N < shortest_path_sample_size:
        shortest_path_sample_size = N

    nodes = list(giant_component.nodes())
    sources = random.sample(nodes, shortest_path_sample_size)
    total_distance = 0
    total_paths = 0
    for source in sources:
        lengths = nx.shortest_path_length(G, source=source)
        for dist in lengths.values():
            if dist > 0:
                total_distance += dist
                total_paths += 1
    if total_paths == 0:
        return np.nan
    return total_distance / total_paths

def calculate_average_distance_per_node_num_ring_lattice(G, node_num, graph_sample_size):
    G_ring_lattice, pos = G.ring_lattice(node_num)
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

#--------------------- instantiate graph ---------------------

instance_graph = Graph()

#--------------------- calculate <d> per node number and topology ---------------------

for node_num in node_num_vector:
    graph_sample_size = node_num
    calculate_average_distance_per_node_num_ring_lattice(instance_graph, node_num, graph_sample_size)
    calculate_average_distance_per_node_num_square_lattice(instance_graph, node_num, graph_sample_size)
    calculate_average_distance_per_node_num_cubic_lattice(instance_graph, node_num, graph_sample_size)
    calculate_average_distance_per_node_num_random_network(instance_graph, node_num, graph_sample_size, 4)

#--------------------- plot graphs ---------------------





