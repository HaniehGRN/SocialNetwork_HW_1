#--------------------- import libraries ---------------------

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from generate_graph import Graph

#--------------------- define parameters ---------------------

N = 1000   # number of nodes
average_degree_lower_bound = 0   # <k> lower bound
average_degree_upper_bound = 5   # <k> upper bound
step_size_non_critical_regions = 0.1
step_size_critical_region = 0.02
non_critical_region_upper_bound = 0.8
critical_region_upper_bound = 1.3

#--------------------- define variables ---------------------

average_degree = []
S_relative_giant_component_size = []
s_average_size_small_clusters = []

#--------------------- define functions ---------------------

def calculate_probability(k):
    p = k / (N - 1)
    return p

def get_connected_components(G):
    connected_components = nx.connected_components(G)
    return connected_components

def get_giant_component(G):
    giant_component_nodes = max(nx.connected_components(G), key=len) # Get the iterator of all connected components (sets of nodes)
    giant_component = G.subgraph(giant_component_nodes).copy()
    giant_component_size = giant_component.number_of_nodes()
    return giant_component, giant_component_size

def get_relative_giant_component_size(giant_component_size, N):
    NG = giant_component_size
    S = NG / N
    return S

def get_small_clusters_subgraph(G):
    giant_component, giant_component_size = get_giant_component(G)
    all_nodes = set(G.nodes)
    remaining_nodes = all_nodes.difference(giant_component)
    remaining_nodes_subgraph = G.subgraph(remaining_nodes)
    return remaining_nodes_subgraph

def plot_components(G, pos, giant_component, small_clusters):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))
    nx.draw(
        G,
        pos,
        ax=ax1,
        with_labels=False,  # Don't show node labels for clarity
        node_size=30,  # Smaller nodes
        width=0.5,  # Thinner edges
        edge_color="gray",
        node_color="skyblue",
    )
    nx.draw(
        giant_component,
        pos,
        ax=ax1,
        with_labels=False,  # Don't show node labels for clarity
        node_size=30,  # Smaller nodes
        width=0.5,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
    ax1.set_title("Erdo ̋s-Re ́nyi graph G(N, p)", fontsize=10)
    ax1.set_aspect('equal', adjustable='box')
    nx.draw(
        giant_component,
        pos,
        ax=ax2,
        with_labels=False,  # Don't show node labels for clarity
        node_size=30,  # Smaller nodes
        width=0.5,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
    ax2.set_title("Giant Component of G(N, p)", fontsize=10)
    ax2.set_aspect('equal', adjustable='box')
    nx.draw(
        small_clusters,
        pos,
        ax=ax3,
        with_labels=False,  # Don't show node labels for clarity
        node_size=30,  # Smaller nodes
        width=0.5,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
    ax3.set_title("Small Clusters of G(N, p)", fontsize=10)
    ax3.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

def get_average_size_small_clusters(small_clusters_subgraph):
    small_clusters = get_connected_components(small_clusters_subgraph)
    average_size_small_clusters = np.average([len(small_cluster) for small_cluster in small_clusters])
    # print("Average size of small clusters: ", average_size_small_clusters)
    return average_size_small_clusters

def plot_S_and_s(S, s, k):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharex=True)
    ax1.plot(k, S, color="blue")
    ax1.set_title("The Order Parameter S=NG/N")
    ax1.set_ylabel("S")
    ax2.plot(k, s, color='red')
    ax2.set_title("The Average Size Of Isolated Clusters <s>")
    ax2.set_ylabel("s")
    fig.supxlabel("<k>")
    fig.subplots_adjust(hspace=0)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

def get_S_and_s(instance_graph, k):
    average_degree.append(k)
    S = []
    s = []
    for i in range(50):  # must be 50
        print(f'k : {k}, i : {i}')
        G, pos = instance_graph.random_network(N, k)
        connected_components = get_connected_components(G)
        giant_component, giant_component_size = get_giant_component(G)
        small_clusters_subgraph = get_small_clusters_subgraph(G)
        S.append(get_relative_giant_component_size(giant_component_size, N))
        s.append(get_average_size_small_clusters(small_clusters_subgraph))

    S_relative_giant_component_size.append(np.average(S))
    s_average_size_small_clusters.append(np.average(s))

instance_graph = Graph()

for k in np.arange(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_regions):
    k = round(k, 2)
    get_S_and_s(instance_graph, k)
    print("------------------------------------------------------------------------")

for k in np.arange(non_critical_region_upper_bound, critical_region_upper_bound, step_size_critical_region):
    k = round(k, 2)
    get_S_and_s(instance_graph, k)
    print("------------------------------------------------------------------------")

for k in np.arange(critical_region_upper_bound, average_degree_upper_bound, step_size_non_critical_regions):
    k = round(k, 2)
    get_S_and_s(instance_graph, k)
    print("------------------------------------------------------------------------")

S_relative_giant_component_size = np.array(S_relative_giant_component_size)
s_average_size_small_clusters = np.array(s_average_size_small_clusters)
print(S_relative_giant_component_size)
print(s_average_size_small_clusters)
print(average_degree)
plot_S_and_s(S_relative_giant_component_size, s_average_size_small_clusters, average_degree)


# plot_components(G, pos, giant_component, small_clusters)

# S_relative_giant_component_size = [0.01, 0.0242, 0.0336, 0.044, 0.0452, 0.0542, 0.072, 0.094, 0.1316, 0.13,
#  0.1272, 0.1556, 0.1624, 0.1548, 0.17, 0.1872, 0.1976, 0.2114, 0.1908, 0.1988,
#  0.2244, 0.2224, 0.234, 0.2462, 0.2992, 0.313, 0.3274, 0.3004, 0.3546, 0.3502,
#  0.338, 0.365, 0.3932, 0.3928, 0.4792, 0.5678, 0.6054, 0.6914, 0.738, 0.7784,
#  0.8, 0.8226, 0.8396, 0.8632, 0.8808, 0.8966, 0.9028, 0.926, 0.932, 0.934,
#  0.9384, 0.9528, 0.9538, 0.958, 0.9614, 0.9712, 0.969, 0.9728, 0.9724, 0.981,
#  0.9812, 0.9862, 0.9874, 0.9864, 0.9892, 0.991, 0.9904, 0.99, 0.9904, 0.9922]
#
# s_average_size_small_clusters =[1., 1.03595176, 1.08949062, 1.15602088, 1.1888853, 1.26964067,
#  1.3401049, 1.3979683, 1.46475765, 1.4888678, 1.54516276, 1.49110346,
#  1.51538699, 1.54278021, 1.52780686, 1.57068826, 1.5531691, 1.60009146,
#  1.61433887, 1.61276146, 1.61995027, 1.63043319, 1.67678985, 1.63538764,
#  1.61513425, 1.64978976, 1.5930202, 1.67460598, 1.65782559, 1.70235188,
#  1.67690086, 1.70052091, 1.59774488, 1.61063957, 1.63602926, 1.4952551,
#  1.56364068, 1.40607316, 1.35278187, 1.27393886, 1.2251321, 1.2761949,
#  1.19780107, 1.19963581, 1.20851071, 1.10716825, 1.17843609, 1.14779043,
#  1.12995455, 1.0821801, np.nan, np.nan, 1.05081818, np.nan,
#  np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
#  np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
#  np.nan, np.nan, np.nan, np.nan]
#
# average_degree = np.array([np.float64(0.0), np.float64(0.1), np.float64(0.2), np.float64(0.3), np.float64(0.4), np.float64(0.5), np.float64(0.6), np.float64(0.7), np.float64(0.8), np.float64(0.82), np.float64(0.84), np.float64(0.86), np.float64(0.88), np.float64(0.9), np.float64(0.92), np.float64(0.94), np.float64(0.96), np.float64(0.98), np.float64(1.0), np.float64(1.02), np.float64(1.04), np.float64(1.06), np.float64(1.08), np.float64(1.1), np.float64(1.12), np.float64(1.14), np.float64(1.16), np.float64(1.18), np.float64(1.2), np.float64(1.22), np.float64(1.24), np.float64(1.26), np.float64(1.28), np.float64(1.3), np.float64(1.4), np.float64(1.5), np.float64(1.6), np.float64(1.7), np.float64(1.8), np.float64(1.9), np.float64(2.0), np.float64(2.1), np.float64(2.2), np.float64(2.3), np.float64(2.4), np.float64(2.5), np.float64(2.6), np.float64(2.7), np.float64(2.8), np.float64(2.9), np.float64(3.0), np.float64(3.1), np.float64(3.2), np.float64(3.3), np.float64(3.4), np.float64(3.5), np.float64(3.6), np.float64(3.7), np.float64(3.8), np.float64(3.9), np.float64(4.0), np.float64(4.1), np.float64(4.2), np.float64(4.3), np.float64(4.4), np.float64(4.5), np.float64(4.6), np.float64(4.7), np.float64(4.8), np.float64(4.9)])

# plot_S_and_s(S_relative_giant_component_size, s_average_size_small_clusters, average_degree)

