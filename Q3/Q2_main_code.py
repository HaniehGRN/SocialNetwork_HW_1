#--------------------- import libraries ---------------------

import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from Q1.Q1_main_code import instance_graph
from generate_graph import Graph

#--------------------- define parameters ---------------------

N = 1000   # number of nodes
average_degree_lower_bound = 0   # <k> lower bound
average_degree_upper_bound = 5   # <k> upper bound
step_size_non_critical_region = 0.1
step_size_critical_region = 0.02
non_critical_region_upper_bound = 0.8
critical_region_upper_bound = 1.2

#--------------------- define variables ---------------------

average_degree = []
S_relative_giant_component_size = []
s_average_size_small_clusters = []

#--------------------- define functions ---------------------

def calculate_probability(k):
    p = k / (N - 1)
    return p

def identify_connected_components(G):
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
    small_clusters = identify_connected_components(small_clusters_subgraph)
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
    for i in range(5):  # must be 50
        G, pos = instance_graph.random_network(N, k)
        connected_components = identify_connected_components(G)
        giant_component, giant_component_size = get_giant_component(G)
        small_clusters_subgraph = get_small_clusters_subgraph(G)
        S.append(get_relative_giant_component_size(giant_component_size, N))
        s.append(get_average_size_small_clusters(small_clusters_subgraph))

    S_relative_giant_component_size.append(np.average(S))
    s_average_size_small_clusters.append(np.average(s))

instance_graph = Graph()
for k in np.arange(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_region):
    get_S_and_s(instance_graph, k)
for k in np.arange(non_critical_region_upper_bound, critical_region_upper_bound, step_size_critical_region):
    get_S_and_s(instance_graph, k)
print(S_relative_giant_component_size)
print(s_average_size_small_clusters)
print(average_degree)
plot_S_and_s(S_relative_giant_component_size, s_average_size_small_clusters, average_degree)


# plot_components(G, pos, giant_component, small_clusters)




