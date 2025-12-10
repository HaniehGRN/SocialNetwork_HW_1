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
end_node_num = 600 # 5000
points_count = 10 # 60

#--------------------- define variables ---------------------

average_distance_ring_lattice = []
average_distance_square_lattice = []
average_distance_cubic_lattice = []
average_distance_random_network = []

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
    average_distance_ring_lattice.append(get_average_shortest_path(ring_lattice, graph_sample_size))

def get_average_distances_2DLattice(G, node_num, graph_sample_size):
    Lx = int(math.floor(math.sqrt(node_num)))
    Ly = int(math.ceil(node_num / Lx))
    square_lattice, pos = G.square_Lattice(Lx, Ly)
    average_distance_square_lattice.append(get_average_shortest_path(square_lattice, graph_sample_size))

def get_average_distances_3DLattice(G, node_num, graph_sample_size):
    Lx = int(node_num ** (1 / 3))
    Ly = int(math.sqrt(node_num / Lx))
    Lz = int(math.ceil(node_num / (Lx * Ly)))
    cubic_lattice, pos = G.cubic_grid_Lattice(Lx, Ly, Lz, False)
    average_distance_cubic_lattice.append(get_average_shortest_path(cubic_lattice, graph_sample_size))

def get_average_distances_random_network(G, node_num, graph_sample_size, k_avg):
    G_random_network, pos = G.random_network(node_num, k_avg)
    average_distance_random_network.append(get_average_shortest_path(G_random_network, graph_sample_size))

#--------------------- generate N logarithmically ---------------------

node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), points_count))).astype(int))
# print(f"Testing N values (log base 10): {node_num_vector}")

#--------------------- instantiate graph ---------------------

instance_graph = Graph()

#--------------------- calculate <d> per node number and topology ---------------------

for node_num in node_num_vector:
    graph_sample_size = node_num
    get_average_distances_1DLattice(instance_graph, node_num, graph_sample_size)
    get_average_distances_2DLattice(instance_graph, node_num, graph_sample_size)
    get_average_distances_3DLattice(instance_graph, node_num, graph_sample_size)
    get_average_distances_random_network(instance_graph, node_num, graph_sample_size, 4)

#--------------------- save results to improve plots in implementation ---------------------

# print(average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network, node_num_vector)
# np.savetxt('average_distance_ring_lattice_array2.txt', average_distance_ring_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_square_lattice_array2.txt', average_distance_square_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_cubic_lattice_array2.txt', average_distance_cubic_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_random_network2.txt', average_distance_random_network, fmt='%d', delimiter=',')
# np.savetxt('node_num_vector.txt', node_num_vector, fmt='%d', delimiter=',')

#--------------------- log of N & <d> ---------------------

# average_distances = np.array([average_distance_ring_lattice,
#                               average_distance_square_lattice,
#                               average_distance_cubic_lattice,
#                               average_distance_random_network])

#--------------------- log of N & <d> ---------------------

# base_10_log1 = np.log10(average_distance_ring_lattice)
# base_10_log2 = np.log10(average_distance_square_lattice)
# base_10_log3 = np.log10(average_distance_cubic_lattice)
# base_10_log4 = np.log10(average_distance_random_network)
# base_10_log5 = np.log10(node_num_vector)

#--------------------- plot graphs ---------------------

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Your plotting code
l1, = ax1.plot(node_num_vector, average_distance_ring_lattice, label="Ring Lattice")
l2, = ax1.plot(node_num_vector, average_distance_square_lattice, label="Square Lattice")
l3, = ax1.plot(node_num_vector, average_distance_cubic_lattice, label="Cubic Lattice")
l4, = ax1.plot(node_num_vector, average_distance_random_network, label="Random Network")

ax2.plot(node_num_vector, average_distance_ring_lattice)
ax2.plot(node_num_vector, average_distance_square_lattice)
ax2.plot(node_num_vector, average_distance_cubic_lattice)
ax2.plot(node_num_vector, average_distance_random_network)

# Subplot titles
ax1.set_title("Linear Plot", fontsize=10)
ax2.set_title("Log-log Plot", fontsize=10)

# Shared labels
fig.supxlabel("N", fontsize=10)
fig.supylabel("<d>", fontsize=10)

# SHARED LEGEND — working version
fig.legend(
    handles=[l1, l2, l3, l4],
    labels=["Ring Lattice", "Square Lattice", "Cubic Lattice", "Random Network"],
    loc="upper center",
    ncol=4,
    frameon=True,
    bbox_to_anchor=(0.5, 0.98)   # move legend a little lower
)

# Keep space for legend and titles
plt.tight_layout(rect=[0, 0, 1, 0.90])  # MORE SPACE on top

plt.show()


#--------------------- fit linear regression model on each curve ---------------------

# base_10_log5 = base_10_log5.reshape(-1, 1)
#
# model1 = LinearRegression()
# model2 = LinearRegression()
# model3 = LinearRegression()
# model4 = LinearRegression()
#
# model1.fit(base_10_log5, base_10_log1)
# model2.fit(base_10_log5, base_10_log2)
# model3.fit(base_10_log5, base_10_log3)
# model4.fit(base_10_log5, base_10_log4)

#--------------------- extract scaling exponent ---------------------

# slope = model1.coef_[0]
# intercept = model1.intercept_
# print(f"Slope (coefficient): {slope}")
# print(f"Intercept: {intercept}")
#
# slope = model2.coef_[0]
# intercept = model2.intercept_
# print(f"Slope (coefficient): {slope}")
# print(f"Intercept: {intercept}")
#
# slope = model3.coef_[0]
# intercept = model3.intercept_
# print(f"Slope (coefficient): {slope}")
# print(f"Intercept: {intercept}")
#
# slope = model4.coef_[0]
# intercept = model4.intercept_
# print(f"Slope (coefficient): {slope}")
# print(f"Intercept: {intercept}")

#--------------------- compare the simulated <d> with the theoretical predictions ---------------------

# sqrt_node_num_vector = np.sqrt(node_num_vector)
# print(f'sqrt N : {sqrt_node_num_vector}\n,<d> : {average_distance_square_lattice}')
#
# sqrt3_node_num_vector = np.pow(node_num_vector, (1/3))
# print(f'N^1/3 : {sqrt3_node_num_vector}\n,<d> : {average_distance_cubic_lattice}')
#
# ln_node_num_vector = np.log(node_num_vector)
# print(f'lnN : {ln_node_num_vector}\n,<d> : {average_distance_random_network}')

