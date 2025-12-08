#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np
import networkx as nx

#--------------------- define parameters ---------------------

# G1, pos1 = Graph.ring_lattice(1000, 2)
start_node_num = 500
end_node_num = 5000
point_num = 200

#--------------------- generate N logarithmically ---------------------

node_num_vector = np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_num))).astype(int)
# print(f"Testing N values (log base 10): {node_num_vector}")

graph = Graph()
G, pos = graph.random_network(50, 4)
# giant_component = max(nx.connected_components(G), key=len)
# print(giant_component)
# G = G.subgraph(giant_component).copy()
# N = G.number_of_nodes()
# print(N)
def calculate_shortest_path(G):

    # ensure calculating shortest path on a connected graph
    largest_cc_nodes = max(nx.connected_components(G), key=len)
    giant_component = G.subgraph(largest_cc_nodes).copy()
    N = giant_component.number_of_nodes()
    if N == 0:
        return np.nan

    # print(nx.number_connected_components(G))
    # print(giant_component)


calculate_shortest_path(G)




