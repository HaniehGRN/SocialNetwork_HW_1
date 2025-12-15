#--------------------- import libraries ---------------------

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from generate_graph import Graph
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

#--------------------- define parameters ---------------------

average_degree_lower_bound = 0   # <k> lower bound
average_degree_upper_bound = 5   # <k> upper bound
step_size_non_critical_regions = 0.1
step_size_critical_region = 0.02
non_critical_region_upper_bound = 0.8
critical_region_upper_bound = 1.3

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

def get_s(instance_graph, k, N):
    s = []
    for i in range(50):  # must be 50
        print(f'k : {k}, i : {i}')
        G, pos = instance_graph.random_network(N, k)
        small_clusters_subgraph = get_small_clusters_subgraph(G)
        s.append(get_average_size_small_clusters(small_clusters_subgraph))

    return np.average(s)

def get_small_clusters_subgraph(G):
    giant_component, giant_component_size = get_giant_component(G)
    all_nodes = set(G.nodes)
    remaining_nodes = all_nodes.difference(giant_component)
    remaining_nodes_subgraph = G.subgraph(remaining_nodes)
    return remaining_nodes_subgraph

def get_S(instance_graph, k, N):
    S = []
    for i in range(50):  # must be 50
        print(f'k : {k}, i : {i}')
        G, pos = instance_graph.random_network(N, k)
        connected_components = get_connected_components(G)
        giant_component, giant_component_size = get_giant_component(G)
        small_clusters_subgraph = get_small_clusters_subgraph(G)
        S.append(get_relative_giant_component_size(giant_component_size, N))

    return np.average(S)

def S_k_plot(S, k, N):
    iters = len(S)
    colors = ["pink", "orange", "red"]
    thik = [5.5, 3.5, 1]
    fig = plt.figure(figsize=(10, 6))
    for i in range(iters):
        print(S)
        plt.plot(k,S[i], label=f'N={N[i]}', color=colors[i], linewidth=thik[i])
    plt.legend()
    plt.xlabel('<k>')
    plt.ylabel('S')
    plt.title('\nS vs. k\n', fontweight='bold')
    plt.show()

def get_slope_near_critical_point(x, y):
    print(f'x : {x}, y : {y}')
    model = LinearRegression()
    model.fit(np.log(x.reshape(-1, 1)),
              np.log(y))
    return model.coef_

def compare_theoretical_practical_giant_component_size_critical(instance_graph, k, N):
    G, pos = instance_graph.random_network(N, k)
    giant_component, giant_component_size = get_giant_component(G)
    print(f"Compare Giant Component Size with N^(2/3) - N = {N}")
    print("NG : ", giant_component_size)
    print("N^ (2/3) : ", np.power(N, (2/3)))

def S_k_plot(S, k, N):
    iters = len(S)
    colors = ["pink", "orange", "red"]
    thik = [5.5, 3.5, 1]
    fig = plt.figure(figsize=(10, 6))
    for i in range(iters):
        print(S)
        plt.plot(k,S[i], label=f'N={N[i]}', color=colors[i], linewidth=thik[i])
    plt.legend()
    plt.xlabel('<k>')
    plt.ylabel('S')
    plt.title('\nS vs. k\n', fontweight='bold')
    plt.show()

def logarithmic_binning(connected_components_sizes):
    if len(connected_components_sizes) > 0:
        min_size = max(1, np.min(connected_components_sizes))
        max_size = np.max(connected_components_sizes)
        bins = np.geomspace(min_size, max_size, num=50)
        s, bin_edges = np.histogram(connected_components_sizes, bins=bins, density=True)
        bins_center = (bin_edges[:-1] + bin_edges[1:]) / 2
    else:
        bins_center, s = np.array(), np.array()
    print("bins_center : ", bins_center)
    print("bins : ", s)
    return bins_center, s

def fit_linear_regression(p_of_s, s):

    # Filter out s=0 , as log(0) is undefined
    mask = s > 0
    print(s)
    print(p_of_s)
    filtered_p_of_s = p_of_s[mask]
    filtered_s = s[mask]
    slope, intercept, r_value, p_value, std_err = linregress(
        filtered_s,
        filtered_p_of_s
    )

    # The slope of the line is the negative of the power law exponent (alpha)
    alpha = -slope
    return alpha

def plot_Ps_s(G, pos, p_of_s, s, k_avg, N):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.plot(np.log(s),np.log(p_of_s), 'o', markersize=5)
    ax1.set_xlabel('s')
    ax1.set_ylabel('P(s)')
    ax1.set_title(f'\nComponent Size Distribution at Critical Point (N={N}, $\\langle k \\rangle = {k_avg}$)\n',
                  fontsize=12, fontweight="bold")
    nx.draw(
        G,
        pos,
        ax=ax2,
        with_labels=False,  # Don't show node labels for clarity
        node_size=20,  # Smaller nodes
        width=0.3,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
    ax2.set_title("\nG(N, p)\n", fontsize=12, fontweight="bold")
    ax2.set_aspect('equal', adjustable='box')
    fig.tight_layout()
    plt.show()

def Simulating_Network_Evolution(N):

    average_degree = []
    S_relative_giant_component_size = []
    s_average_size_small_clusters = []
    instance_graph = Graph()

    for k in np.arange(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_regions):
        average_degree.append(k)
        k = round(k, 2)
        S = get_S(instance_graph, k, N)
        s = get_s(instance_graph, k, N)
        S_relative_giant_component_size.append(S)
        s_average_size_small_clusters.append(s)
        print("------------------------------------------------------------------------")

    for k in np.arange(non_critical_region_upper_bound, critical_region_upper_bound, step_size_critical_region):
        average_degree.append(k)
        k = round(k, 2)
        S = get_S(instance_graph, k, N)
        s = get_s(instance_graph, k, N)
        S_relative_giant_component_size.append(S)
        s_average_size_small_clusters.append(s)
        print("------------------------------------------------------------------------")

    for k in np.arange(critical_region_upper_bound, average_degree_upper_bound, step_size_non_critical_regions):
        average_degree.append(k)
        k = round(k, 2)
        S = get_S(instance_graph, k, N)
        s = get_s(instance_graph, k, N)
        S_relative_giant_component_size.append(S)
        s_average_size_small_clusters.append(s)
        print("------------------------------------------------------------------------")

    return np.array(S_relative_giant_component_size), np.array(s_average_size_small_clusters), np.array(average_degree)

def Analyzing_the_Critical_Threshold(S_relative_giant_component_size, s_average_size_small_clusters, average_degree):
    plot_S_and_s(S_relative_giant_component_size, s_average_size_small_clusters, average_degree)

def Finite_Size_Effects(N_list, N):

    average_degree = [[], [], []]
    S_relative_giant_component_size = [[], [], []]
    instance_graph = Graph()

    for i in N_list:
        for k in np.arange(average_degree_lower_bound, non_critical_region_upper_bound, step_size_non_critical_regions):
            average_degree[i].append(k)
            k = round(k, 2)
            S = get_S(instance_graph, k, N[i])
            S_relative_giant_component_size[i].append(S)
            print("------------------------------------------------------------------------")

        for k in np.arange(non_critical_region_upper_bound, critical_region_upper_bound, step_size_critical_region):
            average_degree[i].append(k)
            k = round(k, 2)
            S = get_S(instance_graph, k, N[i])
            S_relative_giant_component_size[i].append(S)
            print("------------------------------------------------------------------------")

        for k in np.arange(critical_region_upper_bound, average_degree_upper_bound, step_size_non_critical_regions):
            average_degree[i].append(k)
            k = round(k, 2)
            S = get_S(instance_graph, k, N[i])
            S_relative_giant_component_size[i].append(S)
            print("------------------------------------------------------------------------")

    S_k_plot(S_relative_giant_component_size, average_degree[0], N_list)

    # k_start = 0.9
    i_start = 13
    # k_end = 1.1
    i_end = 23

    print(get_slope_near_critical_point(k[i_start:i_end], S_relative_giant_component_size[0][i_start:i_end]))
    print(get_slope_near_critical_point(k[i_start:i_end], S_relative_giant_component_size[1][i_start:i_end]))
    print(get_slope_near_critical_point(k[i_start:i_end], S_relative_giant_component_size[2][i_start:i_end]))

def The_Critical_State(N, k_avg):

    instance_graph = Graph()
    G, pos = instance_graph.random_network(N, k_avg)
    connected_components = get_connected_components(G)
    connected_components_sizes = np.array([len(connected_component) for connected_component in connected_components])
    p_of_s, s = logarithmic_binning(connected_components_sizes)
    print(fit_linear_regression(p_of_s, s))
    plot_Ps_s(G, pos, p_of_s, s, k_avg, N)


#--------------------- main code ---------------------

# S_relative_giant_component_size, s_average_size_small_clusters, average_degree = Simulating_Network_Evolution(N)
# Analyzing_the_Critical_Threshold(S_relative_giant_component_size, s_average_size_small_clusters)
# Finite_Size_Effects()
The_Critical_State(10000, 1)


