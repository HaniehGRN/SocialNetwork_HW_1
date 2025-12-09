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
point_count = 60

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

# node_num_vector = np.sort(np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_count))).astype(int))
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

# print(average_distance_ring_lattice, average_distance_square_lattice, average_distance_cubic_lattice, average_distance_random_network, node_num_vector)
# np.savetxt('average_distance_ring_lattice_array2.txt', average_distance_ring_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_square_lattice_array2.txt', average_distance_square_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_cubic_lattice_array2.txt', average_distance_cubic_lattice, fmt='%d', delimiter=',')
# np.savetxt('average_distance_random_network2.txt', average_distance_random_network, fmt='%d', delimiter=',')
# np.savetxt('node_num_vector.txt', node_num_vector, fmt='%d', delimiter=',')

#--------------------- plot graphs ---------------------
#
average_distance_ring_lattice = [125.25050100200401, 130.2504816955684, 135.5, 140.75044563279857, 146.25042881646655, 152.2504118616145, 158.25039619651346, 164.5, 171.0, 177.7503526093089, 185.0, 192.2503259452412, 200.0, 207.7503015681544, 216.0, 224.75027870680046, 233.7502679528403, 243.0, 252.5, 262.75023832221166, 273.0, 284.0, 295.2502120441052, 307.0, 319.2501960784314, 331.7501886792453, 345.0, 358.75017445917655, 373.0, 388.0, 403.2501551831161, 419.25014925373137, 436.0, 453.5, 471.5, 490.25012761613067, 509.7501227295042, 530.0, 551.0, 573.0, 595.7501049979, 619.5, 644.0, 669.7500933881211, 696.2500898311175, 724.0, 752.7500830840811, 782.7500798977309, 814.0, 846.2500738989063, 880.0, 915.0, 951.5, 989.2500632111252, 1028.7500607828836, 1069.5, 1112.250056217675, 1156.5, 1202.5, 1250.250050010002]
average_distance_square_lattice = [11.261386138613862, 11.521821631878558, 11.76043557168784, 12.0, 12.26043405676127, 12.520064205457464, 12.759630200308166, 13.0, 13.25962910128388, 13.51856946354883, 13.758940397350994, 14.0, 14.258939580764489, 14.517282479141835, 14.758342922899885, 15.0, 15.516162669447342, 15.75782038345106, 16.0, 16.25781990521327, 16.75735950044603, 17.0, 17.257359125315393, 17.75694996028594, 18.0, 18.25694966190834, 18.75658362989324, 19.0, 19.512837393021726, 19.756254008980115, 20.256253813300795, 20.512209648600358, 21.0, 21.511640498105034, 21.755684822845055, 22.25568468923699, 22.755437409376512, 23.25543729754743, 23.51064793837789, 24.0, 24.510212588578575, 25.0, 25.50981146594844, 26.0, 26.509440684004275, 27.0, 27.50909692358584, 28.0, 28.754311649016643, 29.25431160479392, 29.754167844023737, 30.254167805411313, 31.0, 31.507940509200907, 32.25390718922818, 32.753788761949174, 33.50746601292623, 34.25367725431678, 34.753572168150754, 35.50704504862076]
average_distance_cubic_lattice = [7.889025844930417, 8.201792642140468, 8.225874789038013, 8.222311619990716, 8.573241580380303, 8.577464788732394, 8.57526594164141, 8.895400554211307, 8.91026865440654, 8.895719798624851, 9.226651791165358, 9.237880485166873, 9.235863432504475, 9.5895749289292, 9.579579986199175, 9.895543133958286, 9.926053829815334, 9.904403640873502, 10.23949152802214, 10.246804454265783, 10.243459390213085, 10.576684682169061, 10.572030364286624, 10.917453085213724, 10.92091710020653, 11.260465450108557, 11.243025614602017, 11.251684261419287, 11.580479057551415, 11.58628841607565, 11.917102778722265, 11.920248822338346, 12.25824363346338, 12.256635741097831, 12.583417472405237, 12.58210361067504, 12.930482985438825, 12.93817925075074, 13.26505044533737, 13.258358149316702, 13.60376031231341, 13.602570961448324, 13.922128166724182, 13.927427068159297, 14.28622557129057, 14.27221858856037, 14.59808760802641, 14.600627971322439, 14.947252332157595, 15.284434308978657, 15.269366526223184, 15.612196984337354, 15.60371868110117, 15.936699502321567, 16.270364034352152, 16.274608719642142, 16.592648347135185, 16.949494762995887, 16.94389516082269, 17.28687998461834]
average_distance_random_network = [4.5555830406174245, 4.591069472252654, 4.720702516748144, 4.627446059599879, 4.604908347220118, 4.620354181941233, 4.850728262164023, 4.905201908307454, 4.838614554404028, 4.753259993552547, 4.712956752721665, 4.783399209486166, 4.976243904191695, 4.8528864629355395, 5.156168744582972, 4.917140905395542, 5.092236362776174, 4.986407496752644, 5.146813935783253, 5.232665511452653, 5.277647128503142, 5.18765604905806, 5.234873227135852, 5.156345519979632, 5.314614660132166, 5.352664193403726, 5.354550335960062, 5.462943939548658, 5.383048263475555, 5.291741400425413, 5.558069272638103, 5.411409063377567, 5.5538370579139364, 5.665776277755142, 5.576301335225078, 5.706521040726692, 5.649348197622334, 5.606806945018984, 5.643660329134974, 5.736707942882641, 5.818604382003804, 5.724545224968672, 5.834910122841262, 5.843802595240973, 5.756509549891582, 5.845670717991689, 5.9934095653352975, 5.991317701320248, 5.9905800685283515, 5.9930765853039905, 6.002228930830406, 6.045308111292692, 5.969856741968612, 6.0372858388639, 6.1035740406829495, 6.193470732883844, 6.230759274676647, 6.230972893411472, 6.291758773904504, 6.244498527253376]
node_num_vector = [500, 520, 541, 562, 584, 608, 632, 657, 683, 710, 739, 768, 799, 830, 863, 898, 934, 971, 1009, 1050, 1091, 1135, 1180, 1227, 1276, 1326, 1379, 1434, 1491, 1551, 1612, 1676, 1743, 1813, 1885, 1960, 2038, 2119, 2203, 2291, 2382, 2477, 2575, 2678, 2784, 2895, 3010, 3130, 3255, 3384, 3519, 3659, 3805, 3956, 4114, 4277, 4448, 4625, 4809, 5000]


base_10_log1 = np.log10(average_distance_ring_lattice)
base_10_log2 = np.log10(average_distance_square_lattice)
base_10_log3 = np.log10(average_distance_cubic_lattice)
base_10_log4 = np.log10(average_distance_random_network)
base_10_log5 = np.log10(node_num_vector)

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.plot(node_num_vector, average_distance_ring_lattice, color="black")
ax1.plot(node_num_vector, average_distance_square_lattice, color="blue")
ax1.plot(node_num_vector, average_distance_cubic_lattice, color="green")
ax1.plot(node_num_vector, average_distance_random_network, color="red")
# plt.set_title('<d>')
ax2.plot(base_10_log5, base_10_log1, color="black")
ax2.plot(base_10_log5, base_10_log2, color="blue")
ax2.plot(base_10_log5, base_10_log3, color="green")
ax2.plot(base_10_log5, base_10_log4, color="red")

plt.show()


#
# [125.25050100200401, 135.5, 146.75042735042734, 158.75039494470775, 172.0, 186.25033647375506, 201.5, 218.25028702640643, 236.25026511134678, 255.75024485798238, 276.7502262443439, 299.750208855472, 324.25019305019305, 351.2501781895937, 380.2501645819618, 411.5, 445.5, 482.2501297353399, 522.2501197891711, 565.2501106684374, 612.0, 662.5, 717.2500871991629, 776.5, 840.7500743826242, 910.0, 985.2500634678853, 1066.750058616647, 1154.750054147715, 1250.250050010002]
# [11.261386138613862, 11.76043557168784, 12.26043405676127, 12.759630200308166, 13.25962910128388, 13.758940397350994, 14.258939580764489, 15.0, 15.516162669447342, 16.0, 16.75735950044603, 17.51430907604252, 18.013899613899614, 18.75658362989324, 19.512837393021726, 20.512209648600358, 21.25595567867036, 22.0, 23.0, 24.0, 24.755002041649654, 25.75480950584685, 27.0, 28.0, 29.0, 30.254167805411313, 31.507940509200907, 32.753788761949174, 34.0, 35.50704504862076]
# [7.893391650099404, 8.229989552358756, 8.558252816100241, 8.558483039844393, 8.901211248843513, 9.215349495593923, 9.243226435519658, 9.571069992784249, 9.90320645747288, 10.252123884192889, 10.599791568320194, 10.581689527026557, 10.90948062037271, 11.24794767730674, 11.582496735636802, 11.914990739674073, 12.264927221868941, 12.585426726933887, 12.919696435184454, 13.263040281389737, 13.601614205368492, 13.942855154865994, 14.26873057610749, 14.59500368546898, 15.272956246773683, 15.602038972843015, 15.94148137731578, 16.277507161919008, 16.93903221103627, 17.274711632378388]
# [4.459689036808902, 4.746130863882871, 4.825472165152603, 4.727426002248033, 4.775619675192344, 4.971345232576109, 4.868854637688206, 5.036496736539618, 4.979396319250603, 5.137035109810012, 5.162861176405615, 5.194737032875421, 5.206254143673491, 5.450332066923292, 5.375780560427023, 5.433870930151257, 5.543087269468979, 5.559987227642072, 5.598147736534044, 5.648318539542655, 5.711216507010968, 5.806011192589733, 5.844643326563526, 6.0020505518529905, 5.963093544527432, 6.1047460508439855, 6.144521314669207, 6.213686231733812, 6.127935981482466, 6.3004114658297645]
#

#
# model1 = LinearRegression()
# model2 = LinearRegression()
# model3 = LinearRegression()
# model4 = LinearRegression()
# model1.fit(base_10_log5, base_10_log1)
# model2.fit(base_10_log5, base_10_log2)
# model3.fit(base_10_log5, base_10_log3)
# model4.fit(base_10_log5, base_10_log4)
#
# slope = model1.coef_[0]
# intercept = model1.intercept_
# print(f"Slope (coefficient): {slope}")
# print(f"Intercept: {intercept}")

