# --------------------- import libraries ---------------------

import networkx as nx
import numpy as np
import re

from networkx.classes import edges


# --------------------- generate graph ---------------------

def generate_pattern(b):
    source_pattern = [(r'^' + (i * '0') + ((b - i) * '.')) for i in range(0, b)]
    destination_pattern = [(r'' + (i * '.') + ((b - i) * '1')) for i in range(0, b)]
    return source_pattern, destination_pattern


def detect_matching(source_pattern, destination_pattern, nodes_list):
    destination_set = [[node for node in nodes_list if re.match(pattern, node)] for
                                 pattern in destination_pattern]
    source_set = [[node for node in nodes_list if re.match(pattern, node)] for pattern in
                            source_pattern]
    return destination_set, source_set


def generate_network(N, b):
    nodes_list = [f'{i:0{b}b}' for i in range(0, N)]
    source_pattern, destination_pattern = generate_pattern(b)
    source_set, destination_set = detect_matching(source_pattern, destination_pattern, nodes_list)
    edges_list = []
    for i in range(b):
        for source_node in source_set[i]:
            for destination_node in destination_set[i]:
                edges_list.append([source_node, destination_node])

    return nodes_list, edges_list

b = 3
N = 8
nodes_list, edges_list = generate_network(N, b)
# print(nodes_list)
# print(edges_list)