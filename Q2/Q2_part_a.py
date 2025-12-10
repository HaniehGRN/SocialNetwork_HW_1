# --------------------- import libraries ---------------------

import networkx as nx
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------- define functions ---------------------

def generate_pattern(b):
    source_set = [(r'^' + (i * '0') + ((b - i) * '.')) for i in range(0, b)]
    destination_set = [(r'' + (i * '.') + ((b - i) * '1')) for i in range(0, b)]
    return source_set, destination_set

def detect_matching(source_set, destination_set, b, nodes_list):
    destination_patterns_mask = [[node for node in nodes_list if re.match(destination_pattern, node)] for
                                 destination_pattern in destination_set]
    source_patterns_mask = [[node for node in nodes_list if re.match(source_pattern, node)] for source_pattern in
                            source_set]
    return source_patterns_mask, destination_patterns_mask

def generate_RG_network(N, b):
    nodes_list = [f'{i:0{b}b}' for i in range(0, N)]
    source_set, destination_set = generate_pattern(b)
    source_patterns_mask, destination_patterns_mask = detect_matching(source_set, destination_set, b, nodes_list)
    edges_list = []
    for i in range(b):
        for source_node in source_patterns_mask[i]:
            for destination_node in destination_patterns_mask[i]:
                edges_list.append([source_node, destination_node])

    return nodes_list, edges_list

def spy_plot(G, pos, adjacency_matrix):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    nx.draw(
        G,
        pos,
        ax=ax1,
        with_labels=False,
        node_size=10,
        width=0.3,
        edge_color="pink",
        node_color="gray",
    )
    ax1.set_title("Scale-Free Network G", fontweight="bold")
    ax2.spy(
        adjacency_matrix,
        markersize=22,
        color='purple',
    )
    ax2.set_title("Adjacency Matrix Spy Plot", fontweight='bold')
    ax2.set_aspect('equal', adjustable='box')
    fig.subplots_adjust(hspace=0)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

# --------------------- Q2 - part (a) ---------------------

b = 10
N = np.power(2, b)
nodes_list, edges_list = generate_RG_network(N, b)
G = nx.DiGraph()
G.add_nodes_from(nodes_list)
G.add_edges_from(edges_list)
pos = nx.spring_layout(G, seed=42)
adjacency_matrix = nx.adjacency_matrix(G).toarray()
spy_plot(G, pos, adjacency_matrix)
