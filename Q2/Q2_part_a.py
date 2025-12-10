#--------------------- import libraries ---------------------

import networkx as nx
import numpy as np
import re

#--------------------- generate graph ---------------------

def generate_pattern(b):
    source_set = [ (r'^' + (i * '0') + ((b - i) * '.')) for i in range(0, b) ]
    destination_set = [ (r'' + ((b - i) * '.') + (i * '1')) for i in range(0, b)]
    print(source_set)
    print(destination_set)
    return source_set, destination_set

def detect_matching(source_set, destination_set, b, nodes_list):
    destination_patterns_mask = [[ node for node in nodes_list if re.match(destination_pattern, node)] for destination_pattern in destination_set]
    source_patterns_mask = [[ node for node in nodes_list if re.match(source_pattern, node)] for source_pattern in source_set]
    print(destination_patterns_mask)
    print(source_patterns_mask)


def generate_network(N, b):
    nodes_list = [ f'{i:0{b}b}' for i in range(0, N) ]
    return nodes_list

nodes_list = generate_network(16, 4)
print(nodes_list)
source_set, destination_set = generate_pattern(4)
detect_matching(source_set, destination_set, 4, nodes_list)
