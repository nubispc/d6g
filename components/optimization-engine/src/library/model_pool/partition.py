# Partition Demo Automation
# Ported from Cyril Hsu's work.

# Modules
import networkx as nx
import random
import copy

# simple partition with random cut points
def partition(r, sub, n_domain=3):
    G = r
    assert len(G.nodes) >= n_domain
    valid = False
    while not valid:
      cut_point = random.sample(list(range(1, len(G.nodes))), n_domain-1)
      cut_point.sort()
      # idx = list(range(len(G.nodes)))
      idx = [str(n) for n in list(range(len(G.nodes)))]
      ##
      G0 = idx[:cut_point[0]]
      G1 = idx[cut_point[0]:cut_point[1]]
      G2 = idx[cut_point[1]:]
      if len(G0)>=2 and len(G1)>=2 and len(G2)>=2 and len(G0)<=4 and len(G1)<=4 and len(G2)<=4:
          valid=True
    ##
    H0 = nx.Graph(G.subgraph([n for n in G0]))
    # print("H0")
    # print(H0)
    H1 = nx.Graph(G.subgraph([n for n in G1]))
    # print("H1")
    # print(H1)
    H2 = nx.Graph(G.subgraph([n for n in G2]))
    # print("H2")
    # print(H2)
    ##
    r0 = copy.deepcopy(r)
    r0 = H0
    r1 = copy.deepcopy(r)
    r1 = H1
    r2 = copy.deepcopy(r)
    r2 = H2
    r = [r0, r1, r2]
    # return r0, r1, r2
    return r
