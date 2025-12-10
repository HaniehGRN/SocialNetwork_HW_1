#--------------------- import libraries ---------------------

import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from generate_graph import Graph

#--------------------- define parameters ---------------------

# N = 100   # number of nodes
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

def calculate_probability(k, N):
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

def get_S(instance_graph, k, N):
    average_degree.append(k)
    S = []
    for i in range(50):  # must be 50
        print(f'k : {k}, i : {i}')
        G, pos = instance_graph.random_network(N, k)
        connected_components = identify_connected_components(G)
        giant_component, giant_component_size = get_giant_component(G)
        small_clusters_subgraph = get_small_clusters_subgraph(G)
        S.append(get_relative_giant_component_size(giant_component_size, N))

    S_relative_giant_component_size.append(np.average(S))


# average_degree = []
# S_relative_giant_component_size = []
instance_graph = Graph()
N = 1000

for k in np.arange(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_regions):
    k = round(k, 2)
    get_S(instance_graph, k, N)
    print("------------------------------------------------------------------------")

for k in np.arange(non_critical_region_upper_bound, critical_region_upper_bound, step_size_critical_region):
    k = round(k, 2)
    get_S(instance_graph, k, N)
    print("------------------------------------------------------------------------")

for k in np.arange(critical_region_upper_bound, average_degree_upper_bound, step_size_non_critical_regions):
    k = round(k, 2)
    get_S(instance_graph, k, N)
    print("------------------------------------------------------------------------")

S_relative_giant_component_size = np.array(S_relative_giant_component_size)
average_degree = np.array(average_degree)
print("S_relative_giant_component_size : ", S_relative_giant_component_size)
print("average_degree : ", average_degree)
# plt.plot(average_degree, S_relative_giant_component_size, label=f'N = {N}')
# plt.legend(loc='upper right')

# S_relative_giant_component_size :  [0.01   0.0246 0.032  0.041  0.0472 0.0658 0.0824 0.0948 0.1162 0.1288
#  0.1488 0.1498 0.141  0.1694 0.172  0.1758 0.1982 0.1846 0.2114 0.179
#  0.2206 0.2242 0.277  0.2634 0.2594 0.2976 0.281  0.3014 0.336  0.3482
#  0.3498 0.38   0.3808 0.3778 0.471  0.5662 0.6194 0.6908 0.7202 0.7786
#  0.7996 0.8008 0.8408 0.8532 0.893  0.9008 0.9056 0.9184 0.9286 0.9356
#  0.939  0.9556 0.9582 0.9602 0.965  0.9668 0.9736 0.9772 0.976  0.9784
#  0.9826 0.985  0.9868 0.9864 0.99   0.9882 0.991  0.9908 0.9928 0.9954]
# average_degree :  [0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.82 0.84 0.86 0.88 0.9
#  0.92 0.94 0.96 0.98 1.   1.02 1.04 1.06 1.08 1.1  1.12 1.14 1.16 1.18
#  1.2  1.22 1.24 1.26 1.28 1.3  1.4  1.5  1.6  1.7  1.8  1.9  2.   2.1
#  2.2  2.3  2.4  2.5  2.6  2.7  2.8  2.9  3.   3.1  3.2  3.3  3.4  3.5
#  3.6  3.7  3.8  3.9  4.   4.1  4.2  4.3  4.4  4.5  4.6  4.7  4.8  4.9 ]

