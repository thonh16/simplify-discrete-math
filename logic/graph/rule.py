import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import shutil

def create_digraph(num_edges: int, list_edges: any):
    G = nx.DiGraph()  # Sử dụng DiGraph cho đồ thị có hướng
    num_edges = num_edges

    print(list_edges)
    for edge in list_edges:
        a = edge[0]
        b = edge[1]
        G.add_edge(a, b)
    return G

def is_reflexive(G):
    for node in G.nodes():
        if not G.has_edge(node, node):
            return False
    return True

def is_symmetric(G):
    for u, v in G.edges():
        if not G.has_edge(v, u):
            return False
    return True

def is_transitive(G):
    for u in G.nodes():
        for v in G.nodes():
            if G.has_edge(u, v):
                for w in G.nodes():
                    if G.has_edge(v, w) and not G.has_edge(u, w):
                        return False
    return True

def find_reflexive_closure(G):
    G_reflexive = G.copy()
    for node in G.nodes():
        G_reflexive.add_edge(node, node)
    return G_reflexive

def find_symmetric_closure(G):
    G_symmetric = G.copy()
    for u, v in G.edges():
        G_symmetric.add_edge(v, u)
    return G_symmetric

def find_transitive_closure(G):
    return nx.transitive_closure(G)

def visualize_graph(G, file_name):
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=10, ax=ax)
    plt.savefig(file_name)
    plt.close()

# G = create_digraph()
# visualize_graph(G)
# print("Đồ thị phản xạ:", is_reflexive(G))
# print("Đồ thị đối xứng:", is_symmetric(G))
# print("Đồ thị bắc cầu:", is_transitive(G))

# print("Bao đóng phản xạ:")
# visualize_graph(find_reflexive_closure(G))

# print("Bao đóng đối xứng:")
# visualize_graph(find_symmetric_closure(G))

# print("Bao đóng bắc cầu:")
# G_transitive = find_transitive_closure(G)
# visualize_graph(G_transitive)