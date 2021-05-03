import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    c_budg, k_budg = 1, 15
    if len(G) <= 30:
        c_budg, k_budg = 1, 15
    elif len(G) <= 50:
        c_budg, k_budg = 3, 50
    else:
        c_budg, k_budg = 5, 100

    c = []
    k = []
    
    target = G.number_of_nodes() - 1
    changed = True
    while c_budg > 0 or k_budg > 0:
        if not changed:
            break
        changed = False
        sp = nx.shortest_path(G, source=0, target=target, weight="weight")
        if len(sp) == 2:
            if k_budg > 0:
                wt = G.edges[0, target]["weight"]
                G.remove_edge(0, target)
                if not nx.is_connected(G):
                    G.add_edge(0, target, weight=wt)
                else:
                    k.append((0, target))
                    changed = True
                    k_budg -= 1
        else:
            vitalities = []
            for i in range(1, len(sp) - 1):
                vitalities.append((sp[i-1], sp[i], sp[i+1], vitality(G, sp[i])))
            vitalities.sort(key=lambda x: x[3], reverse=True)
            for x in vitalities:

                if c_budg > 0:
                    H = G.copy()
                    G.remove_node(x[1])
                    if not nx.is_connected(G):
                        G = H
                        #G.add_node(x[1])
                       
                    else:
                        c.append(x[1])
                        changed = True
                        c_budg -= 1
                        break
                
                if k_budg > 0:
                    weight1 = G.edges[x[0], x[1]]['weight']
                    weight2 = G.edges[x[1], x[2]]['weight']
                    if weight1 < weight2:
                        G.remove_edge(x[0], x[1])
                        if not nx.is_connected(G):
                            G.add_edge(x[0], x[1], weight=weight1)
                        else:
                            k.append((x[0], x[1]))
                            changed = True
                            k_budg -= 1
                            break
                    else:
                        G.remove_edge(x[1], x[2])
                        if not nx.is_connected(G):
                            G.add_edge(x[1], x[2], weight=weight2)
                        else:
                            k.append((x[1], x[2]))
                            changed = True
                            k_budg -= 1
                            break
    # ideas:
    # 1) edges first approach
    # 2) somehow "looking ahead"??
    return c, k

def solve2(G):
    if len(G) <= 30:
        c_budg, k_budg = 1, 15
    elif len(G) <= 50:
        c_budg, k_budg = 3, 50
    else:
        c_budg, k_budg = 5, 100

    c = []
    k = []
    limit = 50
    # limit = k_budg
    target = G.number_of_nodes() - 1
    changed = True
    while c_budg > 0 or k_budg > 0:
        if not changed:
            break
        changed = False
        k_sp = nx.shortest_simple_paths(G, source=0, target=target, weight='weight')
        sp = next(k_sp)
        paths = []
        path_graph = nx.path_graph(sp)
        common_edges = set(path_graph.edges())
        common_nodes = set(sp)
        common_nodes.remove(0)
        common_nodes.remove(target)
        i = 0
        k_disjoint = c_disjoint = 0
        edgeFreqs = {}
        nodeFreqs = {}
        for node in common_nodes:
            nodeFreqs[node] = 1
        for edge in common_edges:
            edgeFreqs[edge] = 1
        for path in k_sp:
            paths.append(path)
            path_graph = nx.path_graph(path)
            edges_to_add = set(path_graph.edges())
            nodes_to_add = set(path)
            edge_inter = edges_to_add.intersection(common_edges)
            node_inter = nodes_to_add.intersection(common_nodes)
            if len(edge_inter) == 0:
                k_disjoint += 1
            if len(node_inter) == 0:
                c_disjoint += 1
            if k_disjoint > k_budg or c_disjoint > c_budg or i >= limit:
                break
            for edge in edge_inter:
                if edge in edgeFreqs:
                    edgeFreqs[edge] += 1
                elif edge[::-1] in edgeFreqs:
                    edgeFreqs[edge] += 1
                else:
                    edgeFreqs[edge] = 1
            for node in node_inter:
                if node in nodeFreqs:
                    nodeFreqs[node] += 1
                else:
                    nodeFreqs[node] = 1
            # if len(edge_inter) == 0 or len(node_inter) == 0 or i >= limit:
            #     break
            #common_edges = edge_inter
            #common_nodes = node_inter
            i += 1
        if k_budg > 0:
            edges = list(edgeFreqs.keys())
            edges.sort(key=lambda x: edgeFreqs[x], reverse=True)
            #edge_weights = list(common_edges)
            #edge_weights.sort(key=lambda x: G.edges[x[0], x[1]]['weight'])
            j = 0
            while not changed and j < len(edges):
                edge = edges[j]
                weight = G.edges[edge[0], edge[1]]['weight']
                G.remove_edge(edge[0], edge[1])
                j += 1
                if not nx.is_connected(G):
                    G.add_edge(edge[0], edge[1], weight=weight)
                else:
                    k.append((edge[0], edge[1]))
                    changed = True
                    k_budg -= 1
                    break
        elif c_budg > 0 and not changed: #or not changed:
            nodes = list(nodeFreqs.keys())
            nodes.sort(key=lambda x: nodeFreqs[x], reverse=True)
            # node_degrees = list(G.degree(list(common_nodes)))
            # node_degrees.sort(key=lambda x: x[1], reverse=True)
            j = 0
            while not changed and j < len(nodes):
                H = G.copy()
                node = nodes[j]
                G.remove_node(node)
                j += 1
                if not nx.is_connected(G):
                    G = H
                else:
                    for edge in k:
                        if edge[0] == node or edge[1] == node:
                            k.remove(edge)
                            k_budg += 1
                    # for edge in k:
                    #     if edge[0] == node or edge[1] == node:
                    #         k.remove(edge)
                    #         k_budg += 1
                    c.append(node)
                    changed = True
                    c_budg -= 1
                    break
        # elif k_budg > 0:
        #     edge_weights = list(common_edges)
        #     edge_weights.sort(key=lambda x: G.edges[x[0], x[1]]['weight'])
        #     for edge in edge_weights:
        #         weight = G.edges[edge[0], edge[1]]['weight']
        #         G.remove_edge(edge[0], edge[1])
        #         if not nx.is_connected(G):
        #             G.add_edge(edge[0], edge[1], weight=weight)
        #         else:
        #             k.append((edge[0], edge[1]))
        #             changed = True
        #             k_budg -= 1
        #             break
    # for large-101
    for node in c:
        for edge in k:
            if edge[0] == node or edge[1] == node:
                k.remove(edge)
                sp = nx.shortest_path(G, source=0, target=target, weight="weight")
                path_graph = nx.path_graph(sp)
                vitalities = []
                for i in range(1, len(sp) - 1):
                    vitalities.append((sp[i-1], sp[i], sp[i+1], vitality(G, sp[i])))
                vitalities.sort(key=lambda x: x[3], reverse=True)
                for x in vitalities:
                    weight1 = G.edges[x[0], x[1]]['weight']
                    weight2 = G.edges[x[1], x[2]]['weight']
                    if weight1 < weight2:
                        G.remove_edge(x[0], x[1])
                        if not nx.is_connected(G):
                            G.add_edge(x[0], x[1], weight=weight1)
                        else:
                            k.append((x[0], x[1]))
                            changed = True
                            k_budg -= 1
                            break
    return c, k

def maxVertex(G, shortestPath):
    """
    Args:
        G: NetworkX graph, current graph
        shortestPath: str, current shortest path in G
    Returns:
        int, vertex in shortestPath with max degree
    """
    vertex = -1
    maxNum = 0
    for i in shortestPath:
        counter = 0
        for e in G.edges:
            counter += e.count(i)
            
        if counter >= maxNum:
            maxNum = counter
            vertex = i
    return vertex

def vitality(G, x):
    """
    Args:
        G: NetworkX graph, current graph
        x: int, vertex to compute vitality on
    Returns:
        int, closeness vitality for x
    """
    return nx.closeness_vitality(G, node=x, weight="weight", wiener_index=None)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     H = G.copy()
#     c, k = solve2(H)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/l151-200/large-101.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# Brandon: 1-100
# Instructional machine: 101-200
# Akshay: 201-250
# Cindy: 251-300
if __name__ == '__main__':
    inputs = glob.glob('inputs/inputs/medium/*')
    distances = []
    for input_path in inputs:
        output_path = 'outputs/medium/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        H = G.copy()
        c, k = solve2(H)
        assert is_valid_solution(G, c, k)
        distances.append((basename(normpath(input_path))[:-3], calculate_score(G, c, k)))
        write_output_file(G, c, k, output_path)
    with open('outputs/distances_medium_alg2.txt', "w") as fo:
        for d in distances:
            fo.write(d[0] + " " + str(d[1]) + "\n")
