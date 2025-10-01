def find(parent, x):                        # find 함수 선언
    if parent[x] != x:                      # x 정점이 루트 노드가 아니면
        parent[x] = find(parent, parent[x]) # x 정점의 루트 노드로 parent 초기화
    return parent[x]                        # parent 반환

def kruskal(edgelist,n):                                            # kruskal 알고리즘 
    shortenidx = 0                                                  # 간선 리스트 선언
    edgeselected = []
    edgesorted = sorted(edgelist, key = lambda e: e[2])             # 간선 가중치 오름차순 정렬
    parent = [i for i in range(n+1)]                                # parent에 자기 자신으로 초기화(모든 정점이 루트노드인 상태)
    while len(edgeselected) < n-1 and shortenidx < len(edgesorted): # 간선이 n-1개가 되도록 조건 설정
        edge = edgesorted[shortenidx]                               # 최소 가중치 간선 선택
        shortenidx += 1
        if(find(parent,edge[0]) != find(parent,edge[1])):           # 간선의 양 정점의 루트노드가 다르면
            edgeselected.append(edge)                               # 간선 선택
            parent[find(parent,edge[1])] = find(parent,edge[0])     # edge[1] 정점의 루트 노드의 부모를 edge[0] 정점의 루트노드로 설정(트리 붙이기, union)
    return edgeselected                                             # 선택된 간선 리스트 반환

edgelist = []                                           # 간선 리스트 선언
n,m = tuple(map(int, input().split()))
for _ in range(m):                                      # 간선 정보 저장
    line = list(map(int, input().split()))
    edgelist.append(line)

edgeselected = kruskal(edgelist,n)                      # 크루스칼 알고리즘 실행
numlist = [edgeselected[i][2] for i in range(n-1)]      # 가중치 총합 계산
total = sum(numlist)
for i in range(n-1):
    print(" ".join(map(str,edgeselected[i])))
print(total)
