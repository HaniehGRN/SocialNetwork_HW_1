# --------------------- import libraries ---------------------

import networkx as nx
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
import random


# --------------------- generate graph ---------------------

def generate_pattern_deterministic(b):
    source_patterns_set = [(r'^' + (i * '0') + ((b - i) * '.')) for i in range(0, b)]
    destination_patterns_set = [(r'' + (i * '.') + ((b - i) * '1')) for i in range(0, b)]
    return source_patterns_set, destination_patterns_set

def random_pattern_generate(rules_num, b, x):
    rules = []
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
    source_patterns_set = random_pattern_generate(rules_num, b, x)
    destination_patterns_set = random_pattern_generate(rules_num, b, x)

    return source_patterns_set, destination_patterns_set

def detect_matching(source_set, destination_set, nodes_list):
    destination_patterns_mask = [[node for node in nodes_list if re.match(destination_pattern, node)] for
                                 destination_pattern in destination_set]
    source_patterns_mask = [[node for node in nodes_list if re.match(source_pattern, node)] for source_pattern in
                            source_set]
    return source_patterns_mask, destination_patterns_mask

def generate_RG_network(b, source_patterns_set, destination_patterns_set):
    N = np.power(2, b)
    nodes_list = [f'{i:0{b}b}' for i in range(0, N)]
    # source_set, destination_set = generate_pattern(b)
    source_patterns_mask, destination_patterns_mask = detect_matching(source_patterns_set, destination_patterns_set, b, nodes_list)
    edges_list = []
    for i in range(b):
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
    ax1.loglog(in_degrees, in_degrees_probability, color='red')
    ax1.set_title("In-Degree Distribution", fontweight='bold')
    ax1.set_xlabel("In-Degree", fontweight='bold')
    ax1.set_ylabel("P(k)", fontweight='bold')
    ax2.loglog(out_degrees, out_degrees_probability, color='blue')
    ax2.set_title("Out-Degree Distribution", fontweight='bold')
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
    # gamma is the slope of the line in log log plot

    return slope, r_value


def Q2_part_a(b):
    # b = 10
    source_patterns_set, destination_patterns_set = generate_pattern_deterministic(b)
    G, pos = generate_RG_network(b, source_patterns_set, destination_patterns_set)
    N = G.number_of_nodes()
    # G = nx.DiGraph()
    # G.add_nodes_from(nodes_list)
    # G.add_edges_from(edges_list)
    # pos = nx.spring_layout(G, seed=42) must be removed

    # adjacency_matrix = nx.adjacency_matrix(G).toarray()
    # spy_plot(G, pos, adjacency_matrix)

    in_degrees, in_degrees_frequency = get_degrees_frequencies(G.in_degree())
    out_degrees, out_degrees_frequency = get_degrees_frequencies(G.out_degree())
    in_degrees_probability = get_probability(N, in_degrees_frequency)
    out_degrees_probability = get_probability(N, out_degrees_frequency)
    # degree_distribution_loglog_plot(in_degrees_probability, out_degrees_probability, in_degrees, out_degrees)

    in_degree_distribution_slope, r_value = fit_linear_regression(in_degrees_probability, in_degrees)
    out_degree_distribution_slope, r_value = fit_linear_regression(out_degrees_probability, out_degrees)

    print("in-degree distribution slope (gamma in power-law) : ", in_degree_distribution_slope)
    print("out-degree distribution slope (gamma in power-law) : ", out_degree_distribution_slope)

def Q2_part_b(b, x_start, x_end, r_start, r_end, sample_size):
    graph_density_list = []
    x_r_pair_list = []
    r_range = np.unique(np.int32(np.logspace(np.log2(r_start), np.log2(r_end), sample_size, base=2)))
    for x in range(x_start, x_end):
        for r in r_range: # must be logarithmically
            x_r_pair_list.append([x, r])
            source_patterns_set, destination_patterns_set = generate_pattern_stochastic(b, x_start, x_end)
            G, pos = generate_RG_network(b, source_patterns_set, destination_patterns_set)
            graph_density = nx.density(G)
            graph_density_list.append(graph_density)

    print("Graph density list : ", graph_density_list)
    print('(x,r) pairs : ', x_r_pair_list)
