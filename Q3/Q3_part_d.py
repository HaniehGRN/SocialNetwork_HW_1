
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from generate_graph import Graph
from scipy.stats import linregress


def calculate_probability(k, N):
    p = k / (N - 1)
    return p

def get_connected_components(G):
    connected_components = nx.connected_components(G)
    return connected_components

def logarithmic_binning(connected_components_sizes):
    if len(connected_components_sizes) > 0:
        min_size = max(1, np.min(connected_components_sizes))
        max_size = np.max(connected_components_sizes)
        bins = np.geomspace(min_size, max_size, num=50)

        # Calculate histogram s and bin edges with density normalization
        s, bin_edges = np.histogram(connected_components_sizes, bins=bins, density=True)

        # Calculate the center of each bin for plotting the x-value (s)
        bins_center = (bin_edges[:-1] + bin_edges[1:]) / 2
    else:
        # Handle edge case where no components exist
        bins_center, s = np.array(), np.array()

    return bins_center, s

def fit_linear_regression(p_of_s, s):

    # Filter out s=0 , as log(0) is undefined
    mask = s > 0
    filtered_p_of_s = p_of_s[mask]
    filtered_s = s[mask]
    tail_mask = filtered_p_of_s > 5
    p_of_s_tail = filtered_p_of_s[tail_mask]
    s_tail = filtered_s[tail_mask]
    slope, intercept, r_value, p_value, std_err = linregress(
        np.log(s_tail),
        np.log(p_of_s_tail)
    )

    # The slope of the line is the negative of the power law exponent (alpha)
    alpha = -slope
    return alpha

instance_graph = Graph()
k_avg = 1
N = 10000 # must be 10000
G, pos = instance_graph.random_network(N, k_avg)
connected_components = get_connected_components(G)
connected_components_sizes = np.array([len(connected_component) for connected_component in connected_components])
p_of_s , s = logarithmic_binning(connected_components_sizes)

print(p_of_s)
print(s)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.plot(np.log10(p_of_s), np.log10(s), 'o', markersize=5)
ax1.set_xlabel('s')
ax1.set_ylabel('P(s)')
ax1.set_title(f'\nComponent Size Distribution at Critical Point (N={N}, $\\langle k \\rangle = {k_avg}$)\n', fontsize=12, fontweight="bold")


alpha, r_value = fit_linear_regression(p_of_s, s)

print(f"Calculated exponent (alpha): {alpha:.4f}")
print(f"R-squared value (goodness of fit): {r_value ** 2:.4f}")

nx.draw(
        G,
        pos,
        ax=ax2,
        with_labels=False,  # Don't show node labels for clarity
        node_size=20,  # Smaller nodes
        width=0.3,  # Thinner edges
        edge_color="black",
        node_color="red",
    )
ax2.set_title("\nG(N, p)\n", fontsize=12, fontweight="bold")
ax2.set_aspect('equal', adjustable='box')
fig.tight_layout()


# print(G.nodes())
# print(pos)
# print(G.edges())

#
# p_of_s = [  1.06253654   1.19543125   1.34494752   1.51316424   1.70242035
#    1.9153473    2.15490568   2.42442636   2.72765683   3.06881326
#    3.45263918   3.88447138   4.37031417   4.91692281   5.53189747
#    6.22378891   7.00221734   7.87800621   8.86333268   9.97189697
#   11.21911281  12.62232177  14.20103439  15.97720145  17.9755192
#   20.22377269  22.75322217  25.59903767  28.80078808  32.40299126
#   36.45573307  41.01536378  46.14528152  51.91681386  58.41020951
#   65.71575413  73.9350257   83.18230685  93.58617391 105.29128462
#  118.46038955 133.27659496 149.94590876 168.70010492 189.79994611
#  213.53880935 240.24676526 270.29516738 304.10181562]

# s = [5.94982277e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
#  0.00000000e+00 5.77637260e-01 0.00000000e+00 0.00000000e+00
#  0.00000000e+00 1.34290420e-01 0.00000000e+00 5.32662222e-02
#  0.00000000e+00 2.50401865e-02 0.00000000e+00 1.15396567e-02
#  6.10524188e-03 4.34122334e-03 1.92930727e-03 1.71482841e-03
#  1.82903149e-03 1.62570017e-03 1.56538737e-03 1.07028082e-04
#  4.75649466e-04 5.07326476e-04 4.50927577e-04 4.00798478e-04
#  1.18747391e-04 5.27731902e-05 2.34532278e-04 1.25075757e-04
#  3.70570764e-05 6.58749679e-05 2.92758618e-05 2.60212980e-05
#  0.00000000e+00 4.11147343e-05 0.00000000e+00 0.00000000e+00
#  0.00000000e+00 0.00000000e+00 0.00000000e+00 2.02727701e-05
#  9.00953481e-06 0.00000000e+00 0.00000000e+00 0.00000000e+00
#  5.62314703e-06]
#
# Calculated exponent (alpha): 2.3894
# R-squared value (goodness of fit): 0.9208

print("bins center : ", p_of_s)
print("s : ", s)


#
# s = [
#     5.94982277, 0.0, 0.0, 0.0, 0.0, 0.57763726, 0.0, 0.0, 0.0, 0.13429042,
#     0.0, 0.0532662222, 0.0, 0.0250401865, 0.0, 0.0115396567, 0.00610524188,
#     0.00434122334, 0.00192930727, 0.00171482841, 0.00182903149, 0.00162570017,
#     0.00156538737, 0.000107028082, 0.000475649466, 0.000507326476,
#     0.000450927577, 0.000400798478, 0.000118747391, 5.27731902e-05,
#     0.000234532278, 0.000125075757, 3.70570764e-05, 6.58749679e-05,
#     2.92758618e-05, 2.6021298e-05, 0.0, 4.11147343e-05, 0.0, 0.0, 0.0,
#     0.0, 0.0, 2.02727701e-05, 9.00953481e-06, 0.0, 0.0, 0.0, 5.62314703e-06
# ]
#
# p_of_s = [
#     1.06253654, 1.19543125, 1.34494752, 1.51316424, 1.70242035, 1.9153473,
#     2.15490568, 2.42442636, 2.72765683, 3.06881326, 3.45263918, 3.88447138,
#     4.37031417, 4.91692281, 5.53189747, 6.22378891, 7.00221734, 7.87800621,
#     8.86333268, 9.97189697, 11.21911281, 12.62232177, 14.20103439,
#     15.97720145, 17.9755192, 20.22377269, 22.75322217, 25.59903767,
#     28.80078808, 32.40299126, 36.45573307, 41.01536378, 46.14528152,
#     51.91681386, 58.41020951, 65.71575413, 73.9350257, 83.18230685,
#     93.58617391, 105.29128462, 118.46038955, 133.27659496, 149.94590876,
#     168.70010492, 189.79994611, 213.53880935, 240.24676526, 270.29516738,
#     304.10181562
# ]