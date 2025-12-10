#--------------------- import libraries ---------------------

import networkx as nx
import numpy as np

#--------------------- generate graph ---------------------

def generate_pattern(b):
    source_set = [((i * '0') + ((b - i) * 'X')) for i in range(0, b)]
    destination_set = [(((b - i) * 'X') + (i * '1')) for i in range(0, b)]
    return source_set, destination_set

# def detect_matching(source_set, destination_set, b):
#     for i in range(0, b):
#
#
#
# def generate_network(N, b):
#
#     nodes_list = [ f'{i:0{b}b}' for i in range(0, N) ]
#     edges_list = [ for in range(0, N) ]
