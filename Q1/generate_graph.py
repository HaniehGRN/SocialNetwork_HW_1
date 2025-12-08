#--------------------- import libraries ---------------------

import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

#--------------------- define graph class ---------------------

class Graph:
    def ring_lattice(N, k=2):
        G = nx.watts_strogatz_graph(N, k, p=0) # p=0 not to rewire
        pos = nx.circular_layout(G)
        return G, pos