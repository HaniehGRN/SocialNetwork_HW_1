# --------------------- import libraries ---------------------

import networkx as nx
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
import random
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


# --------------------- define functions ---------------------

def generate_pattern_deterministic(b):
    source_patterns_set = [(r'^' + (i * '0') + ((b - i) * '.')) for i in range(0, b)]
    destination_patterns_set = [(r'' + (i * '.') + ((b - i) * '1')) for i in range(0, b)]
    return source_patterns_set, destination_patterns_set

def random_pattern_generate(b, x, rules_num):
    rules = []
    # b --> length of rule
    print("rules_num : ", rules_num)
    for r in range(rules_num):
        # print(f'r : {r}')
        b_list = [pos for pos in range(0, b)]
        x_positions = random.sample(b_list, x)
        for pos in x_positions:
            b_list[pos] = '.'
        for i in range(b):
            if b_list[i] != '.':
                b_list[i] = random.sample(['0', '1'], 1)[0]
        # print(''.join(b_list))
        rules.append(''.join(b_list))
    # print(rules)
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
    G, pos = generate_RG_network(b, source_patterns_set, destination_patterns_set, b)
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
    for r in r_range:
         for x in range(x_start, x_end):# must be logarithmically
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

# Q2_part_b(10, 1, 9, 2, 160, 20)


graphs_density_list = np.round([7.636852394916911e-06, 3.0547409579667644e-05, 0.00012218963831867058, 0.0004887585532746823, 0.0019550342130987292, 0.007820136852394917, 0.031036168132942327, 0.12121212121212122, 1.1455278592375367e-05, 4.5821114369501466e-05, 0.00018328445747800586, 0.0007331378299120235, 0.002932551319648094, 0.011638563049853373, 0.04594330400782014, 0.17619745845552298, 1.9092130987292278e-05, 7.636852394916911e-05, 0.00030547409579667644, 0.0012218963831867058, 0.0048570381231671554, 0.019550342130987292, 0.07673509286412512, 0.2694281524926686, 2.2910557184750733e-05, 9.164222873900293e-05, 0.00036656891495601173, 0.001466275659824047, 0.005865102639296188, 0.02297165200391007, 0.09026759530791789, 0.34066471163245354, 2.672898338220919e-05, 0.00010691593352883675, 0.000427663734115347, 0.001710654936461388, 0.006842619745845552, 0.027003910068426198, 0.10679374389051809, 0.36436950146627567, 3.8184261974584555e-05, 0.00015273704789833822, 0.0006109481915933529, 0.002439974340175953, 0.009714076246334311, 0.038646291544477025, 0.14818548387096775, 0.46638257575757575, 4.5821114369501466e-05, 0.00018328445747800586, 0.0007331378299120235, 0.002932551319648094, 0.011722568426197458, 0.04573329056695992, 0.17279905913978494, 0.5403684017595308, 5.7276392961876836e-05, 0.00022910557184750734, 0.0009135584677419354, 0.0036656891495601175, 0.01451001955034213, 0.05737567204301075, 0.20883927480449657, 0.6136210899315738, 7.636852394916911e-05, 0.00030547409579667644, 0.0012209417766373412, 0.004868493401759531, 0.019473973607038123, 0.0755704728739003,
                               0.2698749083577713, 0.7348274835043989, 9.546065493646138e-05, 0.00038184261974584554, 0.0015273704789833822, 0.0060751160801564025, 0.02412481671554252, 0.0935934445259042, 0.32894309781280545, 0.8099072886119257, 0.00011837121212121212, 0.0004734848484848485, 0.0018882117546432063, 0.007563347690615836, 0.029787542766373413, 0.11563817357038123, 0.37720514112903225, 0.8573111406402737, 0.00015273704789833822, 0.0006109481915933529, 0.0024371105205278592, 0.00974080522971652, 0.03787115102639296, 0.14480235826001955, 0.4708138593597263, 0.9351841245112414, 0.00019092130987292277, 0.0007636852394916911, 0.003045194892473118, 0.01216168743890518, 0.04756613514173998, 0.1802402171920821, 0.5342025980571847, 0.9485476615957967, 0.0002405608504398827, 0.0009612887952101662, 0.003839427541544477, 0.015271795576735093, 0.05976123380987292, 0.21644176136363635, 0.6385000458211144, 0.9773328674853372, 0.00030547409579667644, 0.0012218963831867058, 0.0048828125, 0.019365148460410556, 0.0752249053030303, 0.26755807826246336, 0.7229130391617791, 0.9936175006109482, 0.00038184261974584554, 0.0015273704789833822, 0.006095162817693059, 0.02403508369990225, 0.09342256995356794, 0.32445740163734116, 0.7909554847873901, 0.9996315218719453, 0.00048494012707722385, 0.001935942082111437, 0.00773804068914956, 0.030469131842619745, 0.11643049700635386, 0.39279863911290325, 0.8655637142595308, 1.000782777370479, 0.0006109481915933529, 0.002442838159824047, 0.00972457691837732, 0.038411458333333336, 0.14467539558895406, 0.4647511531647116, 0.9177616003787878, 1.0009517427297165],
                              2)
x_r_pairs = np.array([[1, np.int32(2)], [2, np.int32(2)], [3, np.int32(2)], [4, np.int32(2)], [5, np.int32(2)], [6, np.int32(2)], [7, np.int32(2)], [8, np.int32(2)],
                      [1, np.int32(3)], [2, np.int32(3)], [3, np.int32(3)], [4, np.int32(3)], [5, np.int32(3)], [6, np.int32(3)], [7, np.int32(3)], [8, np.int32(3)], [1, np.int32(5)], [2, np.int32(5)], [3, np.int32(5)], [4, np.int32(5)], [5, np.int32(5)], [6, np.int32(5)], [7, np.int32(5)], [8, np.int32(5)], [1, np.int32(6)], [2, np.int32(6)], [3, np.int32(6)], [4, np.int32(6)], [5, np.int32(6)], [6, np.int32(6)], [7, np.int32(6)], [8, np.int32(6)], [1, np.int32(7)], [2, np.int32(7)], [3, np.int32(7)], [4, np.int32(7)], [5, np.int32(7)], [6, np.int32(7)], [7, np.int32(7)], [8, np.int32(7)], [1, np.int32(10)], [2, np.int32(10)], [3, np.int32(10)], [4, np.int32(10)], [5, np.int32(10)], [6, np.int32(10)], [7, np.int32(10)], [8, np.int32(10)], [1, np.int32(12)], [2, np.int32(12)], [3, np.int32(12)], [4, np.int32(12)], [5, np.int32(12)], [6, np.int32(12)], [7, np.int32(12)], [8, np.int32(12)], [1, np.int32(15)], [2, np.int32(15)], [3, np.int32(15)], [4, np.int32(15)], [5, np.int32(15)], [6, np.int32(15)], [7, np.int32(15)], [8, np.int32(15)], [1, np.int32(20)], [2, np.int32(20)], [3, np.int32(20)], [4, np.int32(20)], [5, np.int32(20)], [6, np.int32(20)], [7, np.int32(20)], [8, np.int32(20)], [1, np.int32(25)], [2, np.int32(25)], [3, np.int32(25)], [4, np.int32(25)], [5, np.int32(25)], [6, np.int32(25)], [7, np.int32(25)], [8, np.int32(25)], [1, np.int32(31)], [2, np.int32(31)], [3, np.int32(31)], [4, np.int32(31)], [5, np.int32(31)], [6, np.int32(31)], [7, np.int32(31)], [8, np.int32(31)], [1, np.int32(40)], [2, np.int32(40)], [3, np.int32(40)], [4, np.int32(40)], [5, np.int32(40)], [6, np.int32(40)], [7, np.int32(40)], [8, np.int32(40)], [1, np.int32(50)], [2, np.int32(50)], [3, np.int32(50)], [4, np.int32(50)], [5, np.int32(50)], [6, np.int32(50)], [7, np.int32(50)], [8, np.int32(50)], [1, np.int32(63)], [2, np.int32(63)], [3, np.int32(63)], [4, np.int32(63)], [5, np.int32(63)], [6, np.int32(63)], [7, np.int32(63)], [8, np.int32(63)], [1, np.int32(80)], [2, np.int32(80)], [3, np.int32(80)], [4, np.int32(80)], [5, np.int32(80)], [6, np.int32(80)], [7, np.int32(80)], [8, np.int32(80)], [1, np.int32(100)], [2, np.int32(100)], [3, np.int32(100)], [4, np.int32(100)], [5, np.int32(100)], [6, np.int32(100)], [7, np.int32(100)], [8, np.int32(100)], [1, np.int32(127)], [2, np.int32(127)], [3, np.int32(127)], [4, np.int32(127)], [5, np.int32(127)], [6, np.int32(127)], [7, np.int32(127)], [8, np.int32(127)], [1, np.int32(160)], [2, np.int32(160)], [3, np.int32(160)], [4, np.int32(160)], [5, np.int32(160)], [6, np.int32(160)], [7, np.int32(160)], [8, np.int32(160)]])
x_lists = x_r_pairs[..., 0]
r_lists = x_r_pairs[..., 1]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(x_lists, r_lists, graphs_density_list, cmap='viridis', edgecolor='none', shade=False)
ax.set_xlabel('x', fontweight='bold')
ax.set_ylabel('r', fontweight='bold')
ax.set_zlabel('Graph Density', fontweight='bold')
ax.set_title('3D Surface Plot Graph Density for each (x,r)', fontweight='bold')
plt.show()