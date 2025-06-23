# Greedy Demo Partitioning
# Dr. Anestis Dalgkitsis | v1.54.23

# Explanation:
# - Initialize Empty Subgraphs: Create three empty subgraphs.
# - Assign Nodes Greedily: Iterate through nodes (in a shuffled order for randomness) and assign each node to the subgraph with the fewest nodes at the time of assignment.
# - Include Edges: Ensure that edges between nodes within the same subgraph are included in the respective subgraph.

# Modules
import networkx as nx
import random

def greedysplit(graph, substrate, domains=3):

    # Create empty subgraphs
    subgraphs = [nx.Graph(), nx.Graph(), nx.Graph()]
    
    # Get a list of nodes and shuffle it to ensure randomness
    nodes = list(graph.nodes())
    random.shuffle(nodes)
    
    # Track the number of nodes in each subgraph
    subgraph_sizes = [0, 0, 0]
    
    # Distribute nodes to subgraphs greedily
    for node in nodes:
        # Find the subgraph with the fewest nodes
        min_index = subgraph_sizes.index(min(subgraph_sizes))
        
        # Add the node to this subgraph
        subgraphs[min_index].add_node(node)
        subgraph_sizes[min_index] += 1
    
    # Add edges to the subgraphs
    for edge in graph.edges():
        u, v = edge
        for i, subgraph in enumerate(subgraphs):
            if u in subgraph.nodes() and v in subgraph.nodes():
                subgraph.add_edge(u, v)
    
    # return subgraphs
    # return subgraphs[0], subgraphs[1], subgraphs[2]
    return subgraphs