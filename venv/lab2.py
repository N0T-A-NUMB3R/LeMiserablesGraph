import operator
import networkx as nx
from networkx import Graph, betweenness, closeness, clustering, connected_components, number_connected_components,average_clustering, betweenness_centrality, connected_component_subgraphs, degree
from pylab import show, hist, figure
from math import sqrt
from numpy.random import randint, normal
import matplotlib.pyplot as plt
import main
from random import choice
import numpy as np


def attack_compute(subgraphs, gcc_0, gcc_list, deg_avg_list, dm_list):
    gcc_i = subgraphs[0]
    gcc_list.append(len(gcc_i) / len(gcc_0))  # node percentage copared to original gcc, at first 100%
    deg_avg_list.append(
        np.sum([len(cluster) for cluster in subgraphs]) / len(subgraphs))  # avg numbers of nodes in all components
    dm_list.append(nx.diameter(gcc_i))  # diameter


def attack_graph(G, nodes_to_remove, step):
    my_graph = G.copy()
    N_nodes = len(nodes_to_remove)
    step = int(step * N_nodes)

    subgraphs_split = nx.strongly_connected_component_subgraphs if my_graph.is_directed() else nx.connected_component_subgraphs
    subgraphs = sorted(subgraphs_split(my_graph), key=len, reverse=True)
    # first gcc or scc
    gcc_0 = subgraphs[0]

    # init measures, initiliazed with values from not modified gcc/scc
    gcc_list = list()
    deg_avg_list = list()
    dm_list = list()
    attack_compute(subgraphs, gcc_0, gcc_list, deg_avg_list, dm_list)

    # begins attack
    for i in range(0, N_nodes, 3):

        my_graph.remove_nodes_from(nodes_to_remove[i:i + step])
        subgraphs = sorted(subgraphs_split(my_graph), key=len, reverse=True)

        if len(subgraphs) != 0:
            attack_compute(subgraphs, gcc_0, gcc_list, deg_avg_list, dm_list)

    return gcc_list, deg_avg_list, dm_list


# In[3]:


# def plot_attack(plot1, plot2, plot3, step, ylabel, xlabel, flag, plot4=[]):  # flag=1 plot gcc
#     plt.figure(figsize=(12, 12))
#     plt.plot(np.arange(0, 1, step), plot1, 'o-b', label='Random failures')
#     plt.plot(np.arange(0, 1, step), plot2, '^-r', label='Highest degree attack')
#     plt.plot(np.arange(0, 1, step), plot3, 'x-y', label='Highest clustering attack')
#     if plot4:
#         plt.plot(np.arange(0, 1, step), plot4, '+-g', label='Highest betweenness attack')
#     if flag:  # gcc
#         plt.plot(np.arange(0, 1, step), np.linspace(1, 0, len(plot1), endpoint='True'), color='black',
#                  label='Ideal case')
#     plt.ylabel(ylabel)
#     plt.xlabel(xlabel)
#     plt.legend()

#    plt.grid()
# def Attack(G):
#     G_simple = nx.Graph(G)
#     G_simple2 = nx.Graph(G)
#     between = nx.betweenness_centrality(G_simple)
#     sorted_x = sorted(between.items(), key=operator.itemgetter(1), reverse=True)
#     rand_x = list(range(0, 76))
#     random.shuffle(rand_x)
#     between_giant = []
#     between_rand = []
#     avg_degs = []
#     for x in range(76):
#         remove = sorted_x[x]
#         remove2 = sorted_x[rand_x[x]]
#         G_simple.remove_nodes_from(remove)
#         G_simple2.remove_nodes_from(remove2)
#
#         giant = len(max(nx.connected_component_subgraphs(G_simple), key=len))
#         giant2 = len(max(nx.connected_component_subgraphs(G_simple2), key=len))
#
#         between_giant.append(giant)
#         between_rand.append(giant2)
#
#         y1 = between_giant
#         y2 = between_giant
#
#         y1 = y1[:-1]
#         y2 = y2[1:]
#
#         perc = np.linspace(0, 100, len(between_giant))
#         fig = plt.figure(1, (12, 8))
#         ax = fig.add_subplot(1, 1, 1)
#
#         ax.plot(perc, between_giant)
#         ax.plot(perc, between_rand)
#
#         fmt = '%.0f%%'  # Format you want the ticks, e.g. '40%'
#         xticks = mtick.FormatStrFormatter(fmt)
#         ax.xaxis.set_major_formatter(xticks)
#         ax.set_xlabel('Fraction of Nodes Removed')
#         ax.set_ylabel('Giant Component Size')
#         ax.legend(['betweenness', 'random'])
#         plt.show()


# La più grande componente connessa
def comp_cc(g):
    if not len(g.nodes()): return False

    gc = max(connected_component_subgraphs(g), key=len)
    print(" ---- giant component stats ----")
    print("    x Number of Nodes:  {}".format(len(gc.nodes())))
    print("    x Number of Edges:  {}\n".format(len(gc.edges())))
    main.PlotMostImp(gc)
    return True

# remove node a random

def strat1_rnd(g):

    x = 22
    rand_x = list(range(0, 76))
    sorted_x = sorted(main.dist(g,77).items(), key=operator.itemgetter(1), reverse=True)
    remove2 = sorted_x[rand_x[x]]
    print("   +*+ BANG: {} will be killed +*+".format(remove2))
    g.remove_node(remove2)

    return comp_cc(g)


# remove nodo cazzuto con betweeness alta
def strat2_trg(g):

    btw = sorted([(y, x) for x, y in betweenness_centrality(g).items()], reverse=True)
    print("   +*+ BANG: {} will be killed +*+".format(btw[0][1]))
    g.remove_node(btw[0][1])

    return comp_cc(g)


# strategia in cui ammazzo quello con il più alto coefficiente di cluster.
def atk1_highcc(g):
    print()
    clust = clustering(g)
    toDelete = sorted(clust.items(), key=operator.itemgetter(1), reverse=True)
   # cc = sorted([(y, x) for x, y in clustering(g)], reverse=True)
    print("   +*+ BANG: {} will be killed +*+".format(toDelete))
    g.remove_node(toDelete)

    return comp_cc(g)


# strategia in cui ammazzo quello con il più grande grado
def atk2_highdeg(g):

    degs = sorted([(y, x) for x, y in g.degree()], reverse=True)
    print("   +*+ BANG: {} will be killed +*+".format(degs[0][1]))
    g.remove_node(degs[0][1])

    return comp_cc(g)
