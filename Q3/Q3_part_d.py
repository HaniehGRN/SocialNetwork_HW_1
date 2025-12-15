
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

    # Filter out any bins with 0 s, as log(0) is undefined
    mask = s > 0
    filtered_p_of_s = p_of_s[mask]
    filtered_s = s[mask]
    print(filtered_p_of_s)
    print(filtered_s)

    # Optional: Further filter to only include the "tail" region you suspect is power-law
    # Example: Only consider s_values greater than 5
    tail_mask = filtered_p_of_s > 5
    s_tail = filtered_p_of_s[tail_mask]
    s_tail = filtered_s[tail_mask]

    # Perform Linear Regression on the LOG-TRANSFORMED data
    # We fit log(P(s)) against log(s)
    slope, intercept, r_value, p_value, std_err = linregress(
        np.log(filtered_p_of_s),
        np.log(filtered_s)
    )

    # The slope of the line is the negative of the power law exponent (alpha)
    alpha = -slope
    return alpha, r_value


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
# plt.figure(figsize=(12, 6))
ax1.plot(np.log10(p_of_s), np.log10(s), 'o', markersize=5)
ax1.set_xlabel('s')
ax1.set_ylabel('P(s)')
ax1.set_title(f'\nComponent Size Distribution at Critical Point (N={N}, $\\langle k \\rangle = {k_avg}$)\n', fontsize=12, fontweight="bold")


alpha, r_value = fit_linear_regression(p_of_s, s)

print(f"Calculated exponent (alpha): {alpha:.4f}")
print(f"R-squared value (goodness of fit): {r_value ** 2:.4f}")

# G_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
# # pos = {0: array([ 0.75347259, -0.0153215 ]), 1: array([ 0.09444954, -0.59704418]), 2: array([-0.90629635, -0.15051983]), 3: array([-0.0393113 ,  0.82702164]), 4: array([-0.64450894,  0.33024337]), 5: array([-0.13647361,  0.56081476]), 6: array([ 0.20828349, -0.88148394]), 7: array([ 0.16260254, -0.8708338 ]), 8: array([-0.49642303,  0.70815326]), 9: array([ 0.18974051, -0.87247935]), 10: array([-0.05440422, -0.79062113]), 11: array([-0.62772645,  0.28851656]), 12: array([-0.10560264,  0.9083667 ]), 13: array([-0.07288031, -0.00871102]), 14: array([ 0.61017551, -0.53938494]), 15: array([ 0.40191168, -0.87211174]), 16: array([-0.88271342,  0.4426374 ]), 17: array([0.56594466, 0.46864864]), 18: array([-0.13397595, -0.01177476]), 19: array([ 0.8356385 , -0.34328166]), 20: array([-0.85578892,  0.39846785]), 21: array([-0.68483469,  0.21520775]), 22: array([-0.8196818 ,  0.43213474]), 23: array([-0.03536404, -0.62098023]), 24: array([ 0.12997686, -0.94047896]), 25: array([0.93847656, 0.37297952]), 26: array([ 0.13453271, -0.060366  ]), 27: array([0.06974948, 0.96704642]), 28: array([-0.77367992, -0.65504008]), 29: array([-0.9494695 , -0.32280963]), 30: array([0.56724126, 0.42681324]), 31: array([ 0.85278697, -0.4397332 ]), 32: array([-0.64534155,  0.6089307 ]), 33: array([-0.68702649,  0.70686747]), 34: array([-0.59038471,  0.85696483]), 35: array([-0.09706405,  0.57227701]), 36: array([-0.38833725,  0.88935431]), 37: array([0.69572499, 0.6153071 ]), 38: array([ 0.52413786, -0.866291  ]), 39: array([-0.28525251, -0.92244322]), 40: array([-0.01382466, -0.14343767]), 41: array([0.0092457 , 0.04031722]), 42: array([-0.73198116,  0.20376941]), 43: array([0.35288605, 0.82465629]), 44: array([ 0.92887614, -0.18526472]), 45: array([-0.09669783, -0.01196331]), 46: array([0.88752759, 0.24905747]), 47: array([-0.03992325,  0.7813803 ]), 48: array([0.81015817, 0.16036642]), 49: array([-0.01655991, -0.69344737]), 50: array([-0.96754849,  0.22977142]), 51: array([-0.64014913, -0.58719159]), 52: array([ 0.05093926, -0.60018337]), 53: array([-0.00050372, -0.08430532]), 54: array([-0.05543552, -0.05402898]), 55: array([-0.64933437, -0.72727224]), 56: array([0.84328359, 0.54649706]), 57: array([0.26529672, 0.92088548]), 58: array([ 0.63516973, -0.75792869]), 59: array([ 0.20203782, -0.07080164]), 60: array([0.5472617 , 0.51854039]), 61: array([-0.02864903, -0.18829121]), 62: array([-0.81650202, -0.44650699]), 63: array([0.48783291, 0.85136501]), 64: array([-1.        , -0.06973734]), 65: array([-0.18014294, -0.91730296]), 66: array([-0.63901154,  0.24128925]), 67: array([ 0.77992846, -0.04290349]), 68: array([0.14966489, 0.88193266]), 69: array([-0.3600722 ,  0.91201403]), 70: array([ 0.89186361, -0.05970575]), 71: array([ 0.41956624, -0.73575025]), 72: array([-0.79664931, -0.3401737 ]), 73: array([ 0.00498391, -0.63165201]), 74: array([-0.86033975, -0.52603648]), 75: array([ 0.82490502, -0.56646045]), 76: array([-0.83502308,  0.41256869]), 77: array([0.61192766, 0.47248137]), 78: array([ 0.61279795, -0.50664228]), 79: array([-0.38614446,  0.84572259]), 80: array([-0.05642074,  0.56703457]), 81: array([0.68298803, 0.53970869]), 82: array([-0.90191261, -0.1182488 ]), 83: array([-0.55205495, -0.78292605]), 84: array([-0.98887975,  0.08387454]), 85: array([ 0.05642455, -0.05024312]), 86: array([ 0.25635466, -0.08026914]), 87: array([ 0.82125566, -0.06508661]), 88: array([ 0.82623821, -0.10692836]), 89: array([ 0.76212625, -0.69489404]), 90: array([-0.4429726 , -0.86167583]), 91: array([0.64674676, 0.78046205]), 92: array([-0.10613929,  0.61979715]), 93: array([0.7123336 , 0.58149575]), 94: array([-0.03715519, -0.74845129]), 95: array([-0.77857489, -0.31366576]), 96: array([ 0.94800591, -0.05649811]), 97: array([-0.41805751, -0.81308708]), 98: array([0.54710032, 0.5667099 ]), 99: array([-0.00137128, -0.0077788 ])}
# G_edges = [(0, 67), (1, 52), (2, 82), (3, 47), (4, 11), (5, 35), (6, 7), (10, 94), (11, 66), (13, 18), (13, 45), (13, 99), (14, 78), (16, 76), (17, 30), (17, 60), (17, 77), (20, 22), (21, 42), (21, 66), (23, 73), (26, 59), (26, 85), (35, 80), (35, 92), (36, 69), (36, 79), (37, 93), (40, 53), (40, 61), (41, 99), (45, 54), (49, 73), (49, 94), (52, 73), (53, 54), (53, 85), (59, 86), (60, 98), (67, 87), (70, 87), (70, 96), (72, 95), (81, 93), (85, 99), (87, 88), (90, 97)]

# G = nx.Graph()
# G.add_nodes_from(G_nodes)
# pos = nx.spring_layout(G, seed=42)
# G.add_edges_from(G_edges)

# plt1 = plt.figure(figsize=(12, 6))

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
temp = np.power(s, -alpha)
temp[np.isinf(temp)] = np.nan
print("s^-alpha : ", temp)

fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(12, 6))
# ax3 = fig2.add_subplot(111)
ax3.plot(p_of_s, s, color='orange', marker='o')
ax3.set_xlabel('s')
ax3.set_ylabel('P(s)')
ax3.set_title("P(s) vs. s")
ax4.plot(p_of_s, temp, color='blue', marker='x')
ax4.set_xlabel('s')
ax4.set_ylabel('s^α')
ax4.set_title("s^α vs. s")
# fig2.legend()
ax4.set_aspect('equal', adjustable='box')
plt.show()

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