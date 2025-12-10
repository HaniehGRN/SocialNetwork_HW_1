#--------------------- import libraries ---------------------

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from generate_graph import Graph


def calculate_probability(k, N):
    p = k / (N - 1)
    return p

def get_connected_components(G):
    connected_components = nx.connected_components(G)
    return connected_components

instance_graph = Graph()
k_avg = 1
N = 100
G, pos = instance_graph.random_network(N, k_avg)
connected_components = get_connected_components(G)
connected_components_sizes = np.array([len(connected_component) for connected_component in connected_components])

if len(connected_components_sizes) > 0:
    min_size = max(1, np.min(connected_components_sizes))
    max_size = np.max(connected_components_sizes)
    bins = np.geomspace(min_size, max_size, num=50)

    # Calculate histogram counts and bin edges with density normalization
    counts, bin_edges = np.histogram(connected_components_sizes, bins=bins, density=True)

    # Calculate the center of each bin for plotting the x-value (s)
    s_values = (bin_edges[:-1] + bin_edges[1:]) / 2
else:
    # Handle edge case where no components exist (should not happen with N=10000)
    s_values, counts = np.array(), np.array()

plt.figure(figsize=(8, 6))
plt.loglog(s_values, counts, 'o', markersize=4, label='$P(s)$')
plt.xlabel('Component Size ($s$)')
plt.ylabel('Probability Density ($P(s)$)')
plt.title(f'Component Size Distribution at Critical Point (N={N}, $\\langle k \\rangle = {avg_k}$)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()


