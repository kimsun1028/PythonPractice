def sqrtdist(dot1, dot2):
    return (dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2


def find_shortest_D_with_C(dot,C):
    min_d = sqrtdist(dot,C[0])
    for idx,center in C:
        d = sqrtdist(dot, center)
        min_d = min(min_d,d)
    return min_d

    

def is_center(dot,C):
    for cidx,center in C:
        if dot == center:
            return True
    return False



def clustering(N, K, dots):
    C = []
    
    C.append((0,dots[0]))
    for _ in range(1,K):
        D = []
        for i in range(N):
            if not is_center(dots[i],C):
                D.append(i,find_shortest_D_with_C(dots[i],C))
        idx = max(D, key=lambda x: x[1])[0]
        C.append((idx, dots[idx]))
    not_center = [dots[i] for i in range(N) if i not in [c[0] for c in C]]
    












N, K = map(int, input().split())
xy = []
for i in range(N):
    xy.append(tuple(map(int, input().split())))