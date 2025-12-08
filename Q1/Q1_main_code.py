#--------------------- import libraries ---------------------

from generate_graph import Graph
import numpy as np

#--------------------- define parameters ---------------------

# G1, pos1 = Graph.ring_lattice(1000, 2)
start_node_num = 500
end_node_num = 5000
point_num = 200

#--------------------- generate N logarithmically ---------------------

node_num_vector = np.unique(np.round(np.logspace(np.log10(start_node_num), np.log10(end_node_num), point_num))).astype(int)
print(f"Testing N values (log base 10): {node_num_vector}")


