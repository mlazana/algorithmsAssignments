import sys
import pprint

def adjacencyList(input_file):
    g = {}
    with open(input_file) as graph_input:
        for line in graph_input:
            # Split line and convert line parts to integers.
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            # If a node is not already in the graph
            # we must create a new empty list.
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            # We need to append the "to" node
            # to the existing list for the "from" node.
            g[nodes[0]].append(nodes[1])
            # And also the other way round.
            g[nodes[1]].append(nodes[0])
    return g

def add_last(pq, c):
    pq.append(c)

def root(pq):
    return 0

def set_root(pq, c):
    if len(pq) == 0:
        pq = [c]
    else:
        pq[0] = c

def get_data(pq, p):
    return pq[p]

def children(pq, p):
    if 2*p + 2 < len(pq):
        return [2*p + 1, 2*p + 2]
    else:
        return [2*p + 1]

def parent(p):
    return (p - 1) // 2

def exchange(pq, p1, p2):
    pq[p1], pq[p2] = pq[p2], pq[p1]

def insert_in_pq(pq, c):
    add_last(pq, c)
    i = len(pq) - 1
    while i != root(pq) and get_data(pq, i) < get_data(pq, parent(i)):
        p = parent(i)
        exchange(pq, i, p)
        i = p

def extract_last_from_pq(pq):
    return pq.pop()

def has_children(pq, p):
    return 2*p + 1 < len(pq)

def extract_min_from_pq(pq):
    c = pq[root(pq)]
    set_root(pq, extract_last_from_pq(pq))
    i = root(pq)
    while has_children(pq, i):
        # Use the data stored at each child as the comparison key
        # for finding the minimum.
        j = min(children(pq, i), key=lambda x: get_data(pq, x))
        if get_data(pq, i) < get_data(pq, j):
            return c        
        exchange(pq, i, j)
        i = j
    return c

def update(pq,opn,npn):
    if opn not in pq:
        return 
    else:
        mh_position = mh.index(opn)
        pq[mh_position] = npn
        i = mh_position
        while i != root(pq) and get_data(pq, i) < get_data(pq, parent(i)):
            p = parent(i)
            exchange(pq, i, p)
            i = p
        return pq

input_file = sys.argv[1]
adjacency_List = adjacencyList(input_file)

d = [len(adjacency_List[v]) for v in range(0, len(adjacency_List)) ]   
p = [d[v] for v in range(0, len(adjacency_List)) ] 
core = [0 for i in range(0, len(adjacency_List))] 
pn= [[p[v],v] for v in range(0, len(adjacency_List)) ] 
mh = []

for v in range(0, len(adjacency_List)) :
    insert_in_pq(mh,pn[v])

while len(mh) > 0 : 
    t = extract_min_from_pq(mh)
    core[t[1]] = t[0]
    if len(mh) != 0 :
        for v  in adjacency_List[t[1]]:
            d[v] = d[v] -1
            opn = [p[v],v]
            p[v] = max(t[0],d[v])
            npn = [p[v],v]
            update(mh,opn,npn)

for i in range(0,len(core)):
    print(i,core[i])











