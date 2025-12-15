#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx
import math
import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#--------------------- define parameters ---------------------

start_node_num = 500
end_node_num = 5000
points_count = 60

#--------------------- define functions ---------------------

def get_average_shortest_path(G, sample_size):
    # ensure calculating shortest path on a connected graph
    giant_component = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    N = giant_component.number_of_nodes()
    if N == 0:
        return np.nan
    if N < sample_size:
        sample_size = N

    nodes = list(giant_component.nodes())
    sources = random.sample(nodes, sample_size)
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

def get_average_distances_1DLattice(G, node_num, graph_sample_size):

    ring_lattice, pos = G.ring_lattice(node_num)
    average_distance_ring_lattice = get_average_shortest_path(ring_lattice, graph_sample_size)
    return average_distance_ring_lattice

def get_average_distances_2DLattice(G, node_num, graph_sample_size):
    Lx = int(math.floor(math.sqrt(node_num)))
    Ly = int(math.ceil(node_num / Lx))
    square_lattice, pos = G.square_Lattice(Lx, Ly)
    average_distance_square_lattice = get_average_shortest_path(square_lattice, graph_sample_size)
    return average_distance_square_lattice

def get_average_distances_3DLattice(G, node_num, graph_sample_size):
    Lx = int(node_num ** (1 / 3))
    Ly = int(math.sqrt(node_num / Lx))
    Lz = int(math.ceil(node_num / (Lx * Ly)))
    cubic_lattice, pos = G.cubic_grid_Lattice(Lx, Ly, Lz, False)
    average_distance_cubic_lattice = get_average_shortest_path(cubic_lattice, graph_sample_size)
    return average_distance_cubic_lattice

def get_average_distances_random_network(G, node_num, graph_sample_size, k_avg):
    G_random_network, pos = G.random_network(node_num, k_avg)
    average_distance_random_network = get_average_shortest_path(G_random_network, graph_sample_size)
    return average_distance_random_network

def plot_average_distance_node_num(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    l1, = ax1.plot(node_num_vector, average_distance_ring_lattice, label="Ring Lattice", color='black')
    l2, = ax1.plot(node_num_vector, average_distance_square_lattice, label="Square Lattice", color='blue')
    l3, = ax1.plot(node_num_vector, average_distance_cubic_lattice, label="Cubic Lattice", color='green')
    l4, = ax1.plot(node_num_vector, average_distance_random_network, label="Random Network", color='red')
    ax2.plot(np.log10(node_num_vector), np.log10(average_distance_ring_lattice), color='black')
    ax2.plot(np.log10(node_num_vector), np.log10(average_distance_square_lattice), color='blue')
    ax2.plot(np.log10(node_num_vector), np.log10(average_distance_cubic_lattice), color='green')
    ax2.plot(np.log10(node_num_vector), np.log10(average_distance_random_network), color='red')
    ax1.set_title("Linear Plot", fontweight="bold")
    ax2.set_title("Log-log Plot", fontweight="bold")
    fig.supxlabel("N", fontweight='bold')
    fig.supylabel("<d>", fontsize=10, fontweight='bold')
    fig.suptitle("\nN vs. <d>\n", fontweight='bold')
    fig.legend(
        handles=[l1, l2, l3, l4],
        labels=["Ring Lattice", "Square Lattice", "Cubic Lattice", "Random Network"],
        loc="upper center",
        ncol=4,
        frameon=True,
        bbox_to_anchor=(0.5, 0.89)
    )
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.show()

def extract_scaling_exponent(node_num_vector, average_distance):
    model = LinearRegression()
    model.fit(
        np.log10(np.array(node_num_vector).reshape(-1, 1)),
        np.log10(average_distance
        ))
    slope = model.coef_[0]
    return slope

def get_theoretical_exponent(N):

    sqrt_node_num_vector = np.sqrt(N)

    sqrt3_node_num_vector = np.pow(N, (1/3))

    ln_node_num_vector = np.log(N)

    return N, sqrt_node_num_vector, sqrt3_node_num_vector, ln_node_num_vector

def Q1_Network_Construction_and_Simulation(start_node_num, end_node_num, points_count):

    average_distance_ring_lattice = []
    average_distance_square_lattice = []
    average_distance_cubic_lattice = []
    average_distance_random_network = []
    k_avg = 4

    #--------------------- generate N logarithmically ---------------------

    node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), points_count))).astype(int))

    #--------------------- instantiate graph ---------------------
    instance_graph = Graph()

    #--------------------- calculate <d> per node number and topology ---------------------

    for node_num in node_num_vector:
        graph_sample_size = node_num
        average_distance_ring_lattice.append(get_average_distances_1DLattice(instance_graph, node_num, graph_sample_size))
        average_distance_square_lattice.append(get_average_distances_2DLattice(instance_graph, node_num, graph_sample_size))
        average_distance_cubic_lattice.append(get_average_distances_3DLattice(instance_graph, node_num, graph_sample_size))
        average_distance_random_network.append(get_average_distances_random_network(instance_graph, node_num, graph_sample_size, k_avg))


    return node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network

def Q1_Scaling_Analysis(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network):

    plot_average_distance_node_num(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network)
    average_distances = [average_distance_ring_lattice,
                         average_distance_square_lattice,
                         average_distance_cubic_lattice,
                         average_distance_random_network]
    slopes_list = [extract_scaling_exponent(node_num_vector, average_distances[i]) for i in range(len(average_distances)) ]
    print("Simulated networks exponents : ", slopes_list)
    print("Theoretical exponents(1/D for lattices and log(N) for RN) : ",get_theoretical_exponent(len(node_num_vector)))


#--------------------- main code ---------------------

node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network = Q1_Network_Construction_and_Simulation(start_node_num, end_node_num, points_count)
Q1_Scaling_Analysis(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network)
