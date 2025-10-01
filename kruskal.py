def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x]) 
    return parent[x]

def kruskal(edgelist,n):
    shortenidx = 0
    edgeselected = []
    edgesorted = sorted(edgelist, key = lambda e: e[2])
    parent = [i for i in range(n+1)]
    while len(edgeselected) < n-1 and shortenidx < len(edgesorted):
        edge = edgesorted[shortenidx]
        shortenidx += 1
        if(find(parent,edge[0]) != find(parent,edge[1])):
            edgeselected.append(edge)
            parent[find(parent,edge[1])] = find(parent,edge[0])
    return edgeselected

edgelist = []
n,m = tuple(map(int, input().split()))
for _ in range(m):
    line = list(map(int, input().split()))
    edgelist.append(line)

edgeselected = kruskal(edgelist,n)
numlist = [edgeselected[i][2] for i in range(n-1)]
total = sum(numlist)
for i in range(n-1):
    print(" ".join(map(str,edgeselected[i])))
print(total)
