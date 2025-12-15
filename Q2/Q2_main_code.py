# --------------------- import libraries ---------------------

import networkx as nx
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.stats import linregress
import random

# --------------------- define parameters ---------------------

b = 10
x_start = 1
x_end = 9
r_start = 2
r_end = 160
sample_size = 20

# --------------------- define functions ---------------------

def generate_pattern_deterministic(b):
    source_patterns_set = [(r'^' + (i * '0') + ((b - i) * '.')) for i in range(0, b)]
    destination_patterns_set = [(r'' + (i * '.') + ((b - i) * '1')) for i in range(0, b)]
    return source_patterns_set, destination_patterns_set

def random_pattern_generate(b, x, rules_num):
    rules = []
    print("rules_num : ", rules_num)
    for r in range(rules_num):
        b_list = [pos for pos in range(0, b)]
        x_positions = random.sample(b_list, x)
        for pos in x_positions:
            b_list[pos] = '.'
        for i in range(b):
            if b_list[i] != '.':
                b_list[i] = random.sample(['0', '1'], 1)[0]
        rules.append(''.join(b_list))
    return rules

def generate_pattern_stochastic(b, x, rules_num):
    source_patterns_set = random_pattern_generate(b, x, rules_num)
    destination_patterns_set = random_pattern_generate(b, x, rules_num)

    return source_patterns_set, destination_patterns_set

def detect_matching(source_set, destination_set, nodes_list):
    destination_patterns_mask = [[node for node in nodes_list if re.match(destination_pattern, node)] for
                                 destination_pattern in destination_set]
    source_patterns_mask = [[node for node in nodes_list if re.match(source_pattern, node)] for source_pattern in
                            source_set]
    return source_patterns_mask, destination_patterns_mask

def generate_RG_network(b, source_patterns_set, destination_patterns_set, rules_num):
    N = np.power(2, b)
    nodes_list = [f'{i:0{b}b}' for i in range(0, N)]
    source_patterns_mask, destination_patterns_mask = detect_matching(source_patterns_set, destination_patterns_set, nodes_list)
    edges_list = []
    for i in range(rules_num):
        for source_node in source_patterns_mask[i]:
            for destination_node in destination_patterns_mask[i]:
                edges_list.append([source_node, destination_node])

    G = nx.DiGraph()
    G.add_nodes_from(nodes_list)
    G.add_edges_from(edges_list)
    pos = nx.spring_layout(G, seed=42)
    return G, pos

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

def get_degrees_frequencies(degree_list):

    degrees, degrees_frequency = np.unique([degree for node, degree in degree_list], return_counts=True)
    return degrees, degrees_frequency

def get_probability(N, degrees_frequencies):

    probability = degrees_frequencies / N
    return probability

def degree_distribution_loglog_plot(in_degrees_probability, out_degrees_probability, in_degrees, out_degrees):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12, 6), sharey=True)
    ax1.plot(np.log10(in_degrees), np.log10(in_degrees_probability), color='red')
    ax1.set_title("In-Degree Distribution\n", fontweight='bold')
    ax1.set_xlabel("In-Degree", fontweight='bold')
    ax1.set_ylabel("P(k)", fontweight='bold')
    ax2.plot(np.log10(out_degrees), np.log10(out_degrees_probability), color='blue')
    ax2.set_title("Out-Degree Distribution\n", fontweight='bold')
    ax2.set_xlabel("Out-Degree", fontweight='bold')
    ax2.set_aspect('equal', adjustable='box')
    fig.subplots_adjust(hspace=0, wspace=0)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

def fit_linear_regression(degrees_probability, degrees):

    mask = (degrees > 0) & (degrees_probability > 0)
    masked_degrees = degrees[ mask ] # log(0) is not defined
    masked_degrees_probability = degrees_probability[ mask ]
    slope, intercept, r_value, p_value, std_err = linregress(
        np.log(masked_degrees),
        np.log(masked_degrees_probability)
    )

    return slope, r_value

def degree_distribution(G, N):

    in_degrees, in_degrees_frequency = get_degrees_frequencies(G.in_degree())
    out_degrees, out_degrees_frequency = get_degrees_frequencies(G.out_degree())
    in_degrees_probability = get_probability(N, in_degrees_frequency)
    out_degrees_probability = get_probability(N, out_degrees_frequency)
    degree_distribution_loglog_plot(in_degrees_probability, out_degrees_probability, in_degrees, out_degrees)

    in_degree_distribution_slope, r_value = fit_linear_regression(in_degrees_probability, in_degrees)
    out_degree_distribution_slope, r_value = fit_linear_regression(out_degrees_probability, out_degrees)

    return in_degree_distribution_slope, out_degree_distribution_slope

def get_nodes_in_out_degree(G):

    in_degrees = G.in_degree()
    out_degrees = G.out_degree()
    print(sorted(in_degrees, key=lambda item: item[1]))
    print(sorted(out_degrees, key=lambda item: item[1]))

def graph_density_3D_surface_plot(x_list, r_list, graphs_density_list):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x_list, r_list, graphs_density_list, cmap='viridis', edgecolor='none', shade=False)
    ax.set_xlabel('x', fontweight='bold')
    ax.set_ylabel('r', fontweight='bold')
    ax.set_zlabel('Graph Density', fontweight='bold')
    ax.set_title('3D Surface Plot Graph Density for each (x,r)', fontweight='bold')
    plt.show()

def theoretical_simulated_density_subplot(r_lists, graphs_density_list, theoretical_density):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)
    ax1.plot(r_lists, graphs_density_list, label="simulated graphs density", color="blue")
    ax1.set_title("\nSimulated Graphs Density\n", fontweight="bold")
    ax2.plot(r_lists, theoretical_density, label="theoretical graph density", color="orange")
    ax2.set_title("\nTheoretical Graphs Density\n", fontweight="bold")
    fig.supxlabel('Number of Rules\n', fontweight="bold", fontsize=10)
    fig.supylabel("Density", fontweight="bold", fontsize=10)
    fig.suptitle('\nSimulated vs. Theoretical Density\n', fontsize=16, fontweight="bold")
    fig.subplots_adjust()
    fig.subplots_adjust(hspace=0)
    plt.tight_layout()
    plt.show()

def get_theoretical_density(x_lists, r_lists, b):
    pi = np.power(2.0, (np.array(x_lists) - b))
    theoretical_density = 1 - np.power(1 - np.power(pi, 2), 2*np.array(r_lists))
    return theoretical_density

def theoretical_simulated_density_oneplot (r_lists, graphs_density_list, theoretical_density):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(r_lists, theoretical_density, label="theoretical graph density", color='orange', linewidth=4)
    ax.plot(r_lists, graphs_density_list, label="simulated graphs_density", color='blue', linewidth=1)
    ax.set_xlabel("number of rules", fontweight='bold')
    ax.set_ylabel("Density", fontweight='bold')
    ax.set_title("\nGraph Density vs. r Growth\n", fontweight='bold')
    ax.legend()
    plt.show()

def Deterministic_Construction_of_SF_Networks(b):
    source_patterns_set, destination_patterns_set = generate_pattern_deterministic(b)
    G, pos = generate_RG_network(b, source_patterns_set, destination_patterns_set, b)
    N = G.number_of_nodes()
    adjacency_matrix = nx.adjacency_matrix(G).toarray()
    spy_plot(G, pos, adjacency_matrix)
    in_degree_distribution_slope, out_degree_distribution_slope = degree_distribution(G, N)
    print("in-degree distribution slope (~gamma in power-law) : ", in_degree_distribution_slope)
    print("out-degree distribution slope (~gamma in power-law) : ", out_degree_distribution_slope)
    # get_nodes_in_out_degree(G, N)

def The_Random_Genetic_Model_Parameter_Space(b, x_start, x_end, r_start, r_end, sample_size):
    graph_density_list = []
    x_r_pair_list = []
    r_range = np.unique(np.int32(np.logspace(np.log2(r_start), np.log2(r_end), sample_size, base=2)))
    for r in r_range:
         for x in range(x_start, x_end):
            print(f'({x},{r})')
            x_r_pair_list.append([x, r])
            source_patterns_set, destination_patterns_set = generate_pattern_stochastic(b, x, r)
            print("source rules", source_patterns_set)
            print("destination rules", destination_patterns_set)
            G, pos = generate_RG_network(b, source_patterns_set, destination_patterns_set, r)
            graph_density = nx.density(G)
            print("graph density", graph_density)
            graph_density_list.append(graph_density)


    print("Graph density list : ", graph_density_list)
    print('(x,r) pairs : ', x_r_pair_list)
    graph_density_3D_surface_plot(x_r_pair_list[..., 0] ,x_r_pair_list[..., 1], graph_density_list)
    theoretical_simulated_density_oneplot(x_r_pair_list[..., 0], graph_density_list,get_theoretical_density(x_r_pair_list[..., 0], x_r_pair_list[..., 1], b))

# --------------------- main code ---------------------

Deterministic_Construction_of_SF_Networks(b)
The_Random_Genetic_Model_Parameter_Space(b, x_start, x_end, r_start, r_end, sample_size)
