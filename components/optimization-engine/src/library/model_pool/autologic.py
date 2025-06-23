# Demo Partitioning
# Dr. Anestis Dalgkitsis | v4.64.2

# Explanation:
# - Get Nodes: list(graph.nodes()) retrieves all the nodes in the graph
# - Shuffle Nodes: random.shuffle(nodes) shuffles the list of nodes in place.
# - Partition Nodes: partition_size calculates the size of each partition. The list comprehension creates partitions. The code also handles cases where the number of nodes is not perfectly divisible by three.
# - Create Subgraphs: graph.subgraph(part) creates a new subgraph using the nodes in each partition.

# Modules
import networkx as nx
import random

# MAIN
def autologic(graph, substrate, domains=3):

    # Get the list of nodes from the original graph
    nodes = list(graph.nodes())
    
    # Shuffle the list of nodes to ensure randomness
    random.shuffle(nodes)
    
    # Determine the size of each partition
    n = len(nodes)
    partition_size = n // 3
    
    # Create three partitions of nodes
    partitions = [nodes[i:i + partition_size] for i in range(0, n, partition_size)]
    
    # If the last partition is smaller than the others, merge it with the second to last
    if len(partitions) > 3:
        partitions[-2].extend(partitions[-1])
        partitions = partitions[:-1]
    
    # Create subgraphs for each partition
    subgraphs = []
    for part in partitions:
        subgraph = graph.subgraph(part)
        subgraphs.append(subgraph)
    
    # return subgraphs
    # return subgraphs[0], subgraphs[1], subgraphs[2]
    return subgraphs