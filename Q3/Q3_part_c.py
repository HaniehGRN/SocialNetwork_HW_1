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
N = 10000

for k in np.arange(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_regions):
    k = round(k, 2)
    get_S(instance_graph, k, N)
    print("------------------------------------------------------------------------")

# for k in np.arange(non_critical_region_upper_bound, critical_region_upper_bound, step_size_critical_region):
#     k = round(k, 2)
#     get_S(instance_graph, k, N)
#     print("------------------------------------------------------------------------")

# for k in np.arange(critical_region_upper_bound, average_degree_upper_bound, step_size_non_critical_regions):
#     k = round(k, 2)
#     get_S(instance_graph, k, N)
#     print("------------------------------------------------------------------------")

S_relative_giant_component_size = np.array(S_relative_giant_component_size)
average_degree = np.array(average_degree)
print("S_relative_giant_component_size : ", S_relative_giant_component_size)
print("average_degree : ", average_degree)
# plt.plot(average_degree, S_relative_giant_component_size, label=f'N = {N}')
# plt.legend(loc='upper right')

# N = 100
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

# N = 1000
# S_relative_giant_component_size :  [0.001   0.00346 0.00506 0.00628 0.00866 0.01188 0.01634 0.02106 0.03346
#  0.03568 0.03754 0.0494  0.05034 0.06226 0.05684 0.06844 0.06688 0.09706
#  0.08342 0.1023  0.12658 0.12748 0.16436 0.17498 0.19976 0.20496 0.24092
#  0.26894 0.28056 0.30166 0.33054 0.33698 0.3653  0.41524 0.5108  0.5907
#  0.64178 0.69192 0.73528 0.76462 0.80224 0.81718 0.8472  0.86348 0.88258
#  0.89188 0.90804 0.91382 0.9249  0.93216 0.9418  0.94888 0.95182 0.9591
#  0.96298 0.96622 0.97022 0.97182 0.97526 0.97762 0.98118 0.9835  0.98436
#  0.98472 0.98726 0.98862 0.98968 0.99036 0.99042 0.99178]
# average_degree :  [0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.82 0.84 0.86 0.88 0.9
#  0.92 0.94 0.96 0.98 1.   1.02 1.04 1.06 1.08 1.1  1.12 1.14 1.16 1.18
#  1.2  1.22 1.24 1.26 1.28 1.3  1.4  1.5  1.6  1.7  1.8  1.9  2.   2.1
#  2.2  2.3  2.4  2.5  2.6  2.7  2.8  2.9  3.   3.1  3.2  3.3  3.4  3.5
#  3.6  3.7  3.8  3.9  4.   4.1  4.2  4.3  4.4  4.5  4.6  4.7  4.8  4.9 ]


# N = 10000
# average degree :  [np.float64(0.0), np.float64(0.1)]
# S :  [np.float64(0.0001), np.float64(0.0006)]

# average degree :  [np.float64(0.0), np.float64(0.1), np.float64(0.2)]
# S :  [np.float64(0.0001), np.float64(0.0006), np.float64(0.0006)]

# k : 0.4, i : 0
# average degree :  [np.float64(0.3), np.float64(0.4)]
# S :  [np.float64(0.0008), np.float64(0.0011)]

# k : 0.5, i : 0
# average degree :  [np.float64(0.3), np.float64(0.4), np.float64(0.5)]
# S :  [np.float64(0.0008), np.float64(0.0011), np.float64(0.0018)]

# k : 0.6, i : 0
# average degree :  [np.float64(0.3), np.float64(0.4), np.float64(0.5), np.float64(0.6)]
# S :  [np.float64(0.0008), np.float64(0.0011), np.float64(0.0018), np.float64(0.0021)]


# k : 0.7, i : 0
# average degree :  [np.float64(0.7)]
# S :  [np.float64(0.0068)]

# k : 0.8, i : 0
# average degree :  [np.float64(0.8)]
# S :  [np.float64(0.006)]
#
# k : 0.82, i : 0
# average degree :  [np.float64(0.8), np.float64(0.82)]
# S :  [np.float64(0.006), np.float64(0.0091)]

# k : 0.84, i : 0
# average degree :  [np.float64(0.8), np.float64(0.82), np.float64(0.84)]
# S :  [np.float64(0.006), np.float64(0.0091), np.float64(0.0079)]

# k : 0.86, i : 0
# average degree :  [np.float64(0.8), np.float64(0.86)]
# S :  [np.float64(0.0068)]

# k : 0.88, i : 0
# average degree :  [np.float64(0.8), np.float64(0.86), np.float64(0.88)]
# S :  [np.float64(0.0068), np.float64(0.0137)]

# k : 0.9, i : 0
# average degree :  [np.float64(0.9)]
# S :  [np.float64(0.0097)]

# k : 0.92, i : 0
# average degree :  [np.float64(0.9), np.float64(0.92)]
# S :  [np.float64(0.0097), np.float64(0.0199)]
#
# k : 0.94, i : 0
# average degree :  [np.float64(0.9), np.float64(0.92), np.float64(0.94)]
# S :  [np.float64(0.0097), np.float64(0.0199), np.float64(0.0329)]
#\

# k : 0.96, i : 0
# average degree :  [np.float64(0.9), np.float64(0.92), np.float64(0.94), np.float64(0.96)]
# S :  [np.float64(0.0097), np.float64(0.0199), np.float64(0.0329), np.float64(0.0165)]

# k : 0.98, i : 0
# average degree :  [np.float64(0.98)]
# S :  [np.float64(0.05)]

# k : 1.0, i : 0
# average degree :  [np.float64(0.98), np.float64(1.0)]
# S :  [np.float64(0.05), np.float64(0.0347)]

# k : 1.2, i : 0
# average degree :  [np.float64(1.2)]
# S :  [np.float64(0.3462)]

# k : 1.3, i : 0
# average degree :  [np.float64(1.3)]
# S :  [np.float64(0.4174)]

# k : 1.4, i : 0
# average degree :  [np.float64(1.3), np.float64(1.4)]
# S :  [np.float64(0.4174), np.float64(0.4963)]

# k : 1.5, i : 0
# average degree :  [np.float64(1.3), np.float64(1.4), np.float64(1.5)]
# S :  [np.float64(0.4174), np.float64(0.4963), np.float64(0.5729)]

# k : 1.6, i : 0
# average degree :  [np.float64(1.3), np.float64(1.4), np.float64(1.5), np.float64(1.6)]
# S :  [np.float64(0.4174), np.float64(0.4963), np.float64(0.5729), np.float64(0.623)]

# k : 1.7, i : 0
# average degree :  [np.float64(1.3), np.float64(1.4), np.float64(1.5), np.float64(1.6), np.float64(1.7), np.float64(1.7)]
# S :  [np.float64(0.4174), np.float64(0.4963), np.float64(0.5729), np.float64(0.623), np.float64(0.7013)]

# k : 1.8, i : 0
# average degree :  [np.float64(1.8)]
# S :  [np.float64(0.7378)]

# k : 1.9, i : 0
# average degree :  [np.float64(1.8), np.float64(1.9)]
# S :  [np.float64(0.7378), np.float64(0.7624)]

# k : 2.0, i : 0
# average degree :  [np.float64(1.8), np.float64(1.9), np.float64(2.0)]
# S :  [np.float64(0.7378), np.float64(0.7624), np.float64(0.8038)]
#
# k : 2.2, i : 0
# average degree :  [np.float64(1.8), np.float64(1.9), np.float64(2.0), np.float64(2.1), np.float64(2.2)]
# S :  [np.float64(0.7378), np.float64(0.7624), np.float64(0.8038), np.float64(0.8147), np.float64(0.8398)]

# k : 2.3, i : 0
# average degree :  [np.float64(1.8), np.float64(1.9), np.float64(2.0), np.float64(2.1), np.float64(2.2), np.float64(2.3)]
# S :  [np.float64(0.7378), np.float64(0.7624), np.float64(0.8038), np.float64(0.8147), np.float64(0.8398), np.float64(0.8628)]

# k : 2.4, i : 0
# average degree :  [np.float64(2.4)]
# S :  [np.float64(0.8809)]

# k : 2.5, i : 0
# average degree :  [np.float64(2.4), np.float64(2.5)]
# S :  [np.float64(0.8809), np.float64(0.8886)]

# k : 2.7, i : 0
# average degree :  [np.float64(2.4), np.float64(2.5), np.float64(2.6), np.float64(2.7)]
# S :  [np.float64(0.8809), np.float64(0.8886), np.float64(0.9084), np.float64(0.9154)]
#
# k : 2.8, i : 0
# average degree :  [np.float64(2.8)]
# S :  [np.float64(0.9273)]
#
# k : 2.9, i : 0
# average degree :  [np.float64(2.8), np.float64(2.9)]
# S :  [np.float64(0.9273), np.float64(0.9336)]

# k : 3.0, i : 0
# average degree :  [np.float64(2.8), np.float64(2.9), np.float64(3.0)]
# S :  [np.float64(0.9273), np.float64(0.9336), np.float64(0.9417)]
# -

# k : 3.1, i : 0
# average degree :  [np.float64(3.1)]
# S :  [np.float64(0.9465)]
