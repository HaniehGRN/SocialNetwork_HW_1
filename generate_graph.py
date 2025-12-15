#--------------------- import libraries ---------------------

import networkx as nx
import numpy as np


#--------------------- define graph class ---------------------

class Graph:

    @staticmethod
    def ring_lattice(N, k=2):
        G = nx.watts_strogatz_graph(N, k, p=0) # p=0 not to rewire
        pos = nx.circular_layout(G)
        return G, pos

    @staticmethod
    def square_Lattice(Lx, Ly):
        G = nx.grid_2d_graph(Lx, Ly, periodic=True)
        pos = {(i, j): np.array([i, j]) for i, j in G.nodes()}
        return G, pos

    @staticmethod
    def cubic_grid_Lattice(Lx, Ly, Lz, PERIODIC):
        G = nx.grid_graph(dim=[range(Lx), range(Ly), range(Lz)], periodic=PERIODIC)
        pos = {n: np.array(n) for n in G.nodes()}
        return G, pos

    @staticmethod
    def random_network(N, k_avg):
        p = k_avg / (N - 1)
        G = nx.fast_gnp_random_graph(N, p, directed=False)
        pos = nx.spring_layout(G, seed=42)
        return G, pos