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
    if len(G) <= 50:
        c_budg, k_budg = 3, 50
    else:
        c_budg, k_budg = 5, 100

    c = []
    k = []
    
    target = G.number_of_nodes() - 1
    while c_budg > 0 or k_budg > 0:
        sp = nx.shortest_path(G, source=0, target=target, "weight")
        max_vitality = float('-inf')
        max_node = 0 # what if sp = [0, target] (see checks below)
        for node in sp:
            if node != 0 and node != target:
                v = vitality(G, node)
                if v > max_vitality:
                    max_node = node
                    max_vitality = v
        if c_budg > 0:
            if len(sp) == 2: # sp = [0, target]
                if k_budg > 0:
                    G.remove_edge(0, target)
                    k.append((0,target))
                    # check that G isn't disconnected, if yes: ctrl+z
                else:
                    pass
                    # do nothing
            else:
                G.remove_node(max_node)
                c.append(max_node)
                # check that G isn't disconnected, if yes: ctrl+z
                c_budg -= 1
        else:
            sp.index(max_node)
            G.remove_edge() # remove one (smaller one) of two edges connected to max_node in sp
            k.append()
            # check that G isn't disconnected, if yes: ctrl+z
            k_budg -= 1
            

    # until graph disconnected/c,k quota met:
    # find shortest path:

    pass


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
    return closeness_vitality(G, node=x, weight="weight", wiener_index=None)
        
        
    

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
