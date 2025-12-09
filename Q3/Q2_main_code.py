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
# non_critical_region_lower_bound = 0
non_critical_region_upper_bound = 0.8
# critical_region_lower_bound = 0.8
critical_region_upper_bound = 1.2

#--------------------- define functions ---------------------

def calculate_probability(k):
    p = k / (N - 1)
    return p

def identify_connected_components(G):
    connected_components = nx.connected_components(G)
    return connected_components

def get_giant_component(G):
    giant_component_nodes = max(nx.connected_components(G), key=len) # Get the iterator of all connected components (sets of nodes)
    # print(giant_component_nodes)
    giant_component = G.subgraph(giant_component_nodes).copy()
    return giant_component

def get_relative_giant_component_size(giant_component_size, N):
    # giant_component = get_giant_component(G)
    # NG = giant_component.number_of_nodes()
    NG = giant_component_size
    S = NG / N
    return S

def get_small_clusters(G, giant_component):
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

def get_average_size_non_giant_clusters(G, pos, giant_component, connected_components):
    # get_small_clusters(G, giant_component)
    # print("Remaining nodes: ", remaining_nodes)

    plt.figure(figsize=(9, 4))
    plt.subplot(1, 2, 1)
    nx.draw(
        giant_component,
        pos,
        with_labels=False,  # Don't show node labels for clarity
        node_size=50,  # Smaller nodes
        width=0.5,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
    plt.subplot(1, 2, 2)
    nx.draw(
        remaining_nodes,
        pos,
        with_labels=False,  # Don't show node labels for clarity
        node_size=50,  # Smaller nodes
        width=0.5,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
    plt.tight_layout()
    plt.show()
    # print(temp)
    # print(temp2)

instance_graph = Graph()
# for k in range(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_region):
k = 0.6

# plot the graph

G, pos = Graph.random_network(N, k)
# plt1 = plt.figure(figsize=(4.5, 4.5))
# nx.draw(
#     G,
#     pos,
#     with_labels=False,           # Don't show node labels for clarity
#     node_size=50,                # Smaller nodes
#     width=0.5,                   # Thinner edges
#     edge_color="gray",
#     node_color="skyblue",
# )
connected_components = identify_connected_components(G)
giant_component = get_giant_component(G)
giant_component_size = giant_component.number_of_nodes()
S = get_relative_giant_component_size(giant_component_size, N)
small_clusters = get_small_clusters(G, giant_component)
plot_components(G, pos, giant_component, small_clusters)
# nx.draw(
#     giant_component,
#     pos,
#     with_labels=False,           # Don't show node labels for clarity
#     node_size=50,                # Smaller nodes
#     width=0.5,                   # Thinner edges
#     edge_color="black",
#     node_color="red",
# )
# # plt1.title(f"Erdos-Rényi Random Graph")
# plt1.show()
# get_average_size_non_giant_clusters(G, pos, giant_component, connected_components)
# # print(S)
# # print(nx.nodes(connected_components), nx.nodes(giant_component))
#




