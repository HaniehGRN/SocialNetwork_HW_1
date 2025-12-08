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

    @staticmethod
    def square_Lattice(Lx, Ly):
        G = nx.grid_2d_graph(Lx, Ly, periodic=True)
        pos = {(i, j): np.array([i, j]) for i, j in G.nodes()}
        return G, pos