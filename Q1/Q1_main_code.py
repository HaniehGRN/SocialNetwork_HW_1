#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx
import math
import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#--------------------- define parameters ---------------------

start_node_num = 500
end_node_num = 5000
point_count = 30

#--------------------- define variables ---------------------

average_distance_ring_lattice = []
average_distance_square_lattice = []
average_distance_cubic_lattice = []
average_distance_random_network = []

#--------------------- define functions ---------------------

def calculate_average_shortest_path(G, shortest_path_sample_size):
    # ensure calculating shortest path on a connected graph
    largest_cc_nodes = max(nx.connected_components(G), key=len)
    giant_component = G.subgraph(largest_cc_nodes).copy()
    N = giant_component.number_of_nodes()

    if N == 0:
        return np.nan

    if N < shortest_path_sample_size:
        shortest_path_sample_size = N

    nodes = list(giant_component.nodes())
    sources = random.sample(nodes, shortest_path_sample_size)
    total_distance = 0
    total_paths = 0
    for source in sources:
        lengths = nx.shortest_path_length(G, source=source)
        for dist in lengths.values():
            if dist > 0:
                total_distance += dist
                total_paths += 1
    if total_paths == 0:
        return np.nan
    return total_distance / total_paths

def calculate_average_distance_per_node_num_ring_lattice(G, node_num, graph_sample_size):
    G_ring_lattice, pos = G.ring_lattice(node_num)
    average_distance_ring_lattice.append(calculate_average_shortest_path(G_ring_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_square_lattice(G, node_num, graph_sample_size):
    Lx = int(math.floor(math.sqrt(node_num)))
    Ly = int(math.ceil(node_num / Lx))
    G_square_lattice, pos = G.square_Lattice(Lx, Ly)
    average_distance_square_lattice.append(calculate_average_shortest_path(G_square_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_cubic_lattice(G, node_num, graph_sample_size):
    Lx = int(node_num ** (1 / 3))
    Ly = int(math.sqrt(node_num / Lx))
    Lz = int(math.ceil(node_num / (Lx * Ly)))
    G_cubic_lattice, pos = G.cubic_grid_Lattice(Lx, Ly, Lz, False)
    average_distance_cubic_lattice.append(calculate_average_shortest_path(G_cubic_lattice, graph_sample_size))

def calculate_average_distance_per_node_num_random_network(G, node_num, graph_sample_size, k_avg):
    G_random_network, pos = G.random_network(node_num, k_avg)
    average_distance_random_network.append(calculate_average_shortest_path(G_random_network, graph_sample_size))

#--------------------- generate N logarithmically ---------------------

node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_count))).astype(int))
# print(f"Testing N values (log base 10): {node_num_vector}")

#--------------------- instantiate graph ---------------------

instance_graph = Graph()

#--------------------- calculate <d> per node number and topology ---------------------

# for node_num in node_num_vector:
#     graph_sample_size = node_num
#     calculate_average_distance_per_node_num_ring_lattice(instance_graph, node_num, graph_sample_size)
#     calculate_average_distance_per_node_num_square_lattice(instance_graph, node_num, graph_sample_size)
#     calculate_average_distance_per_node_num_cubic_lattice(instance_graph, node_num, graph_sample_size)
#     calculate_average_distance_per_node_num_random_network(instance_graph, node_num, graph_sample_size, 4)

#--------------------- save results to improve plots in implementation ---------------------

# print(average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network)
# np.savetxt('average_distance_ring_lattice_array.txt', average_distance_ring_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_square_lattice_array.txt', average_distance_square_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_cubic_lattice_array.txt', average_distance_cubic_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_random_network.txt', average_distance_random_network, fmt='%d', delimiter=',')

#--------------------- plot graphs ---------------------

average_distance_ring_lattice = [125.25050100200401, 135.5, 146.75042735042734, 158.75039494470775, 172.0, 186.25033647375506, 201.5, 218.25028702640643, 236.25026511134678, 255.75024485798238, 276.7502262443439, 299.750208855472, 324.25019305019305, 351.2501781895937, 380.2501645819618, 411.5, 445.5, 482.2501297353399, 522.2501197891711, 565.2501106684374, 612.0, 662.5, 717.2500871991629, 776.5, 840.7500743826242, 910.0, 985.2500634678853, 1066.750058616647, 1154.750054147715, 1250.250050010002]
average_distance_square_lattice = [11.261386138613862, 11.76043557168784, 12.26043405676127, 12.759630200308166, 13.25962910128388, 13.758940397350994, 14.258939580764489, 15.0, 15.516162669447342, 16.0, 16.75735950044603, 17.51430907604252, 18.013899613899614, 18.75658362989324, 19.512837393021726, 20.512209648600358, 21.25595567867036, 22.0, 23.0, 24.0, 24.755002041649654, 25.75480950584685, 27.0, 28.0, 29.0, 30.254167805411313, 31.507940509200907, 32.753788761949174, 34.0, 35.50704504862076]
average_distance_cubic_lattice = [7.893391650099404, 8.229989552358756, 8.558252816100241, 8.558483039844393, 8.901211248843513, 9.215349495593923, 9.243226435519658, 9.571069992784249, 9.90320645747288, 10.252123884192889, 10.599791568320194, 10.581689527026557, 10.90948062037271, 11.24794767730674, 11.582496735636802, 11.914990739674073, 12.264927221868941, 12.585426726933887, 12.919696435184454, 13.263040281389737, 13.601614205368492, 13.942855154865994, 14.26873057610749, 14.59500368546898, 15.272956246773683, 15.602038972843015, 15.94148137731578, 16.277507161919008, 16.93903221103627, 17.274711632378388]
average_distance_random_network = [4.459689036808902, 4.746130863882871, 4.825472165152603, 4.727426002248033, 4.775619675192344, 4.971345232576109, 4.868854637688206, 5.036496736539618, 4.979396319250603, 5.137035109810012, 5.162861176405615, 5.194737032875421, 5.206254143673491, 5.450332066923292, 5.375780560427023, 5.433870930151257, 5.543087269468979, 5.559987227642072, 5.598147736534044, 5.648318539542655, 5.711216507010968, 5.806011192589733, 5.844643326563526, 6.0020505518529905, 5.963093544527432, 6.1047460508439855, 6.144521314669207, 6.213686231733812, 6.127935981482466, 6.3004114658297645]


base_10_log1 = np.log10(average_distance_ring_lattice)
base_10_log2 = np.log10(average_distance_square_lattice)
base_10_log3 = np.log10(average_distance_cubic_lattice)
base_10_log4 = np.log10(average_distance_random_network)
base_10_log5 = np.log10(node_num_vector)

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.plot(node_num_vector, average_distance_ring_lattice)
ax1.plot(node_num_vector, average_distance_square_lattice)
ax1.plot(node_num_vector, average_distance_cubic_lattice)
ax1.plot(node_num_vector, average_distance_random_network)
# plt.set_title('<d>')
ax2.plot(base_10_log5, base_10_log1)
ax2.plot(base_10_log5, base_10_log2)
ax2.plot(base_10_log5, base_10_log3)
ax2.plot(base_10_log5, base_10_log4)

plt.show()


#
# [125.25050100200401, 135.5, 146.75042735042734, 158.75039494470775, 172.0, 186.25033647375506, 201.5, 218.25028702640643, 236.25026511134678, 255.75024485798238, 276.7502262443439, 299.750208855472, 324.25019305019305, 351.2501781895937, 380.2501645819618, 411.5, 445.5, 482.2501297353399, 522.2501197891711, 565.2501106684374, 612.0, 662.5, 717.2500871991629, 776.5, 840.7500743826242, 910.0, 985.2500634678853, 1066.750058616647, 1154.750054147715, 1250.250050010002]
# [11.261386138613862, 11.76043557168784, 12.26043405676127, 12.759630200308166, 13.25962910128388, 13.758940397350994, 14.258939580764489, 15.0, 15.516162669447342, 16.0, 16.75735950044603, 17.51430907604252, 18.013899613899614, 18.75658362989324, 19.512837393021726, 20.512209648600358, 21.25595567867036, 22.0, 23.0, 24.0, 24.755002041649654, 25.75480950584685, 27.0, 28.0, 29.0, 30.254167805411313, 31.507940509200907, 32.753788761949174, 34.0, 35.50704504862076]
# [7.893391650099404, 8.229989552358756, 8.558252816100241, 8.558483039844393, 8.901211248843513, 9.215349495593923, 9.243226435519658, 9.571069992784249, 9.90320645747288, 10.252123884192889, 10.599791568320194, 10.581689527026557, 10.90948062037271, 11.24794767730674, 11.582496735636802, 11.914990739674073, 12.264927221868941, 12.585426726933887, 12.919696435184454, 13.263040281389737, 13.601614205368492, 13.942855154865994, 14.26873057610749, 14.59500368546898, 15.272956246773683, 15.602038972843015, 15.94148137731578, 16.277507161919008, 16.93903221103627, 17.274711632378388]
# [4.459689036808902, 4.746130863882871, 4.825472165152603, 4.727426002248033, 4.775619675192344, 4.971345232576109, 4.868854637688206, 5.036496736539618, 4.979396319250603, 5.137035109810012, 5.162861176405615, 5.194737032875421, 5.206254143673491, 5.450332066923292, 5.375780560427023, 5.433870930151257, 5.543087269468979, 5.559987227642072, 5.598147736534044, 5.648318539542655, 5.711216507010968, 5.806011192589733, 5.844643326563526, 6.0020505518529905, 5.963093544527432, 6.1047460508439855, 6.144521314669207, 6.213686231733812, 6.127935981482466, 6.3004114658297645]
#


model1 = LinearRegression()
model2 = LinearRegression()
model3 = LinearRegression()
model4 = LinearRegression()
model1.fit(base_10_log5, base_10_log1)
model2.fit(base_10_log5, base_10_log2)
model3.fit(base_10_log5, base_10_log3)
model4.fit(base_10_log5, base_10_log4)

slope = model1.coef_[0]
intercept = model1.intercept_
print(f"Slope (coefficient): {slope}")
print(f"Intercept: {intercept}")