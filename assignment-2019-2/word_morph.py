import sys 
import jellyfish 
from collections import deque
import pprint 

dict_file = sys.argv[1]
start_word = sys.argv[2]
end_word = sys.argv[3]

def getChild(bk,node, distance):
    if node not in bk.keys():
        return None
    else:
        if distance in bk[node]:
            return bk[node][distance] 
   
def bkTreeInsertion(bk, word):
    if not bk:
        bk[word] = {}
        return
    node = next(iter(bk)) #root(bk)
    while node != None:
        distance = jellyfish.levenshtein_distance(word, node)
        parent = node
        node = getChild(bk,node,distance)
        if node == None:
            if parent not in bk:
                bk[parent] = {}
            bk[parent].update({distance:word})

def getChildren(bk,node):
    if node not in bk.keys():
        return {}
    else:
        return bk[node]

def bkSearch(bk,word):
    results = set()
    to_check = deque()
    to_check.appendleft(next(iter(bk)))
    while to_check:
        node = to_check.pop()
        distance = jellyfish.levenshtein_distance(word, node)

        if distance == 1:
            results.add(node)
        
        l = distance - 1
        h = distance + 1
        children = getChildren(bk,node)
        for child in children:
            if l <= child <= h :
                to_check.appendleft(children[child])
    return results

MAX_INT = sys.maxsize

def dijkstra(bk, start_word,end_word):

    dist = {start_word:0}
    pred = {start_word:-1}
    pq = {start_word:0}

    while len(pq) != 0:
        u = min(pq, key=pq.get)
        
        if u == end_word:
            return (pred,dist)

        del pq[u]
        neighbors = bkSearch(bk,u)
        
        for v in neighbors:
            if (dist.get(v,MAX_INT)) > dist[u] + 1 :      
                dist[v] = dist[u] +1
                pred[v] = u
                pq[v] = dist[v] + jellyfish.levenshtein_distance(v,end_word)
    return (pred, dist)

def get_path(pred, t): 
    path = []
    while t != -1:
        path.append(t)
        t = pred[t]
    return path[::-1]

bk = {}

with open (dict_file) as dictionary:
    for word in dictionary:  
        bkTreeInsertion(bk,word.strip()) 
    pred,dist = dijkstra(bk,start_word,end_word)
    if end_word not in pred:
        print(start_word)
    else:
        print(', '.join(str(x) for x in get_path(pred,end_word)))