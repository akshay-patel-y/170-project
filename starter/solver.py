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
#     c, k = solve(H)

#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/*')
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
