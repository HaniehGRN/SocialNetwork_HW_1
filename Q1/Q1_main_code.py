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

#--------------------- define variables ---------------------

# average_distance_ring_lattice = []
# average_distance_square_lattice = []
# average_distance_cubic_lattice = []
# average_distance_random_network = []

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
    ax2.loglog(node_num_vector, average_distance_ring_lattice, color='black', base=10)
    ax2.loglog(node_num_vector, average_distance_square_lattice, color='blue', base=10)
    ax2.loglog(node_num_vector, average_distance_cubic_lattice, color='green', base=10)
    ax2.loglog(node_num_vector, average_distance_random_network, color='red', base=10)
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
        np.log10(node_num_vector.reshape(-1, 1)),
        np.log10(average_distance
        ))
    slope = model.coef_[0]
    return slope

def get_theoretical_exponent(node_num_vector):

    sqrt_node_num_vector = np.sqrt(node_num_vector)
    # print(f'sqrt N : {sqrt_node_num_vector}\n,<d> : {average_distance_square_lattice}')

    sqrt3_node_num_vector = np.pow(node_num_vector, (1/3))
    # print(f'N^1/3 : {sqrt3_node_num_vector}\n,<d> : {average_distance_cubic_lattice}')

    ln_node_num_vector = np.log(node_num_vector)
    # print(f'lnN : {ln_node_num_vector}\n,<d> : {average_distance_random_network}')

    return sqrt_node_num_vector, sqrt3_node_num_vector, ln_node_num_vector

def Q1_a(start_node_num, end_node_num, points_count):

    average_distance_ring_lattice = []
    average_distance_square_lattice = []
    average_distance_cubic_lattice = []
    average_distance_random_network = []
    k_avg = 4

    #--------------------- generate N logarithmically ---------------------

    node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), points_count))).astype(int))
    # print(f"Testing N values (log base 10): {node_num_vector}")

    #--------------------- instantiate graph ---------------------
    instance_graph = Graph()

    #--------------------- calculate <d> per node number and topology ---------------------

    for node_num in node_num_vector:
        graph_sample_size = node_num
        average_distance_ring_lattice.append(get_average_distances_1DLattice(instance_graph, node_num, graph_sample_size))
        average_distance_square_lattice.append(get_average_distances_2DLattice(instance_graph, node_num, graph_sample_size))
        average_distance_cubic_lattice.append(get_average_distances_3DLattice(instance_graph, node_num, graph_sample_size))
        average_distance_random_network.append(get_average_distances_random_network(instance_graph, node_num, graph_sample_size, k_avg))

    # --------------------- save results to improve plots in implementation ---------------------
    #
    # print(average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network, node_num_vector)
    # np.savetxt('average_distance_ring_lattice_array2.txt', average_distance_ring_lattice, fmt='%d', delimiter=',')
    # np.savetxt('average_distance_square_lattice_array2.txt', average_distance_square_lattice, fmt='%d', delimiter=',')
    # np.savetxt('average_distance_cubic_lattice_array2.txt', average_distance_cubic_lattice, fmt='%d', delimiter=',')
    # np.savetxt('average_distance_random_network2.txt', average_distance_random_network, fmt='%d', delimiter=',')
    # np.savetxt('node_num_vector.txt', node_num_vector, fmt='%d', delimiter=',')


    return node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network

def Q1_b(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network):

    plot_average_distance_node_num(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network)
    average_distances = [average_distance_ring_lattice,
                         average_distance_square_lattice,
                         average_distance_cubic_lattice,
                         average_distance_random_network]
    print(average_distances)
    slopes_list = [extract_scaling_exponent(node_num_vector, average_distances[i]) for i in len(average_distances) ]
    print(slopes_list)
    print( node_num_vector,get_theoretical_exponent(node_num_vector))

# average_distance_ring_lattice = np.array([125, 130, 135, 140, 146, 152, 158, 164, 171, 177, 185, 192, 200, 207, 216, 224, 233, 243, 252, 262, 273, 284, 295, 307, 319, 331, 345, 358, 373, 388, 403, 419, 436, 453, 471, 490, 509, 530, 551, 573, 595, 619, 644, 669, 696, 724, 752, 782, 814, 846, 880, 915, 951, 989, 1028, 1069, 1112, 1156, 1202, 1250])
# average_distance_square_lattice = np.array([11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 21, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 31, 31, 32, 32, 33, 34, 34, 35])
# average_distance_cubic_lattice = np.array([7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17])
# average_distance_random_network = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 5, 6, 6, 6, 6, 6, 6, 6])
# node_num_vector = [500, 520, 541, 562, 584, 608, 632, 657, 683, 710, 739, 768, 799, 830, 863, 898, 934, 971, 1009, 1050, 1091, 1135, 1180, 1227, 1276, 1326, 1379, 1434, 1491, 1551, 1612, 1676, 1743, 1813, 1885, 1960, 2038, 2119, 2203, 2291, 2382, 2477, 2575, 2678, 2784, 2895, 3010, 3130, 3255, 3384, 3519, 3659, 3805, 3956, 4114, 4277, 4448, 4625, 4809, 5000]
# plot_average_distance_node_num(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network)
node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network = Q1_a(start_node_num, end_node_num, points_count)
Q1_b(node_num_vector, average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network)

